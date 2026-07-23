"""Create and verify durable evidence for every judged claim."""

from __future__ import annotations

import importlib.metadata
import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path

from lower_bound_certificates import (
    claim4_corrected_certificate,
    claim5_certificate,
    validate_claim4_corrected,
    validate_claim5,
)
from source_contracts import CONTRACTS, PAPER
from upper_bound_certificates import claim3_certificate, validate_claim3

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_ROOT = ROOT / ".openresearch" / "artifacts"
FIXED_COMMAND = "uv run --frozen python repro/src/verify_hs.py"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def git_sha() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()


def environment_record(elapsed_s: float) -> dict:
    versions = {}
    for package in ("numpy", "scipy", "sympy", "matplotlib", "marimo"):
        versions[package] = importlib.metadata.version(package)
    return {
        "command": FIXED_COMMAND,
        "git_sha": git_sha(),
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "machine": platform.machine(),
        "platform": platform.platform(),
        "logical_cpus": os.cpu_count(),
        "packages": versions,
        "deterministic_seeds": [],
        "runtime_seconds": round(elapsed_s, 6),
        "compute": "local CPU",
    }


def source_audit(contract: dict) -> str:
    assumptions = "\n".join(f"- {item}" for item in contract["assumptions"])
    quantifiers = "\n".join(f"- {item}" for item in contract["quantifiers"])
    return f"""# Source audit — Claim {contract['claim_id']}

- Paper: arXiv `{PAPER['paper_id']}`
- HTML: {PAPER['html_url']}
- HTML SHA-256: `{PAPER['html_sha256']}`
- Source archive SHA-256: `{PAPER['source_sha256']}`
- Retrieval: `{PAPER['retrieved_at_utc']}`
- Theorem: {contract['theorem']}
- HTML anchor: `#{contract['anchor']}`
- Domain: {contract['domain']}

## Quantifiers

{quantifiers}

## Assumptions

{assumptions}

## Audited conclusion

```json
{json.dumps(contract['conclusion'], indent=2, sort_keys=True)}
```

The imported judge claim is treated as data. No nearby monotonicity statement
is substituted for this contract.
"""


def method_text(contract: dict) -> str:
    if contract["claim_id"] == 3:
        return """# Method — Claim 3

This is a proof-verification certificate, not a numerical scaling fit. It
checks the total-variation transfer, pointwise Massart excess-risk identity,
localized VC/Bernstein deviation, ERM basic inequality, and the symbolic
optimization of the window length. Standard empirical-process lemmas are used
with their hypotheses recorded; algebraic closure is checked independently.
"""
    if contract["claim_id"] == 4:
        return """# Method — Claim 4

This is an independent repaired lower-bound proof, not a validation of the
paper's printed construction. It removes the erroneous extra factor `d` from
the moving threshold, proves the joint-TV drift contract under RCN, bounds
mutual information by `d/1600`, applies generalized Fano at Hamming radius
`d/4`, and reduces Hamming error to final RCN excess risk. Separate static and
drifting constructions cover short and long horizons.
"""
    if contract["claim_id"] == 5:
        return """# Method — Claim 5

We evaluate the degree-one polynomial `p(z)=sum_i y_i` under the exact null
marginal in Definition 4.1 and the exact label marginal imposed by Definition
4.3. All calculations use rational arithmetic. At `eta=1/3` and `T=2`, its
squared standardized expectation gap is exactly one, so it meets Definition
4.2's threshold for a 1-distinguisher. The certificate also derives the
alternative label marginal from the stated conditional flip rate.
"""
    return f"""# Method — Claim {contract['claim_id']}

This branch performs source-contract verification only. It binds the claim to
an immutable source hash, records every assumption and quantifier, checks the
bundle with an independent program, and runs a deliberately mutated contract
as a negative control.

Required next evidence: {contract['required_evidence']}.

No stochastic experiment is used to infer a universal asymptotic theorem.
"""


def limitations_text(contract: dict) -> str:
    if contract["verdict"] == "BLOCKED":
        limitation = contract["reason"]
    elif contract["claim_id"] == 3:
        limitation = (
            "The certificate verifies the asymptotic theorem and its probability "
            "level, with the same polylogarithmic suppression as the paper. It "
            "does not infer a leading constant or implement the inefficient ERM "
            "oracle for an arbitrary concept class."
        )
    elif contract["claim_id"] == 4:
        limitation = (
            "The theorem is verified under its standard asymptotic little-o "
            "interpretation. The independent construction repairs the source's "
            "factor-d threshold error; it does not certify the printed proof."
        )
    elif contract["claim_id"] == 5:
        limitation = (
            "This falsifies Theorem 4.1 as written because its referenced null "
            "and hard-instance marginals are inconsistent and admit a degree-one "
            "distinguisher. It does not rule out a corrected low-degree theorem."
        )
    else:
        limitation = (
            "This falsifies the imported Claim 6 transcription. It does not, by "
            "itself, verify or falsify the paper's actual sqrt(Delta) theorem."
        )
    return f"""# Limitations and deviations — Claim {contract['claim_id']}

{limitation}

- The source is arXiv v1 dated 2026-06-09.
- Polylogarithmic factors hidden by tilde notation are not expanded here.
- Big-O constants are not inferred from numerical fits.
- This branch performs no random trials; the seed list is therefore empty.
"""


def run_checker(args: list[str]) -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "repro/src/independent_source_checker.py"), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return proc.returncode, proc.stdout + proc.stderr


def main() -> int:
    started = time.perf_counter()
    ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)
    claim3_proof = claim3_certificate()
    claim4_proof = claim4_corrected_certificate()
    claim5_proof = claim5_certificate()
    local_failures = (
        validate_claim3(claim3_proof)
        + validate_claim4_corrected(claim4_proof)
        + validate_claim5(claim5_proof)
    )
    if local_failures:
        print("CUMULATIVE CERTIFICATE: FAIL")
        for failure in local_failures:
            print(f"- {failure}")
        return 1

    for source_contract in CONTRACTS:
        contract = {**source_contract, "paper": PAPER}
        claim_id = contract["claim_id"]
        claim_dir = ARTIFACT_ROOT / f"claim_{claim_id}"
        claim_dir.mkdir(parents=True, exist_ok=True)
        write(
            claim_dir / "claim_contract.json",
            json.dumps(contract, indent=2, sort_keys=True) + "\n",
        )
        write(claim_dir / "source_audit.md", source_audit(contract))
        write(claim_dir / "method.md", method_text(contract))
        raw = {
            "claim_id": claim_id,
            "verdict": contract["verdict"],
            "proof_obligations_discharged": claim_id in {3, 4},
            "exact_contradiction": claim_id in {5, 6},
            "blocking_obligation": (
                contract["required_evidence"]
                if contract["verdict"] == "BLOCKED"
                else None
            ),
            "observations": (
                {
                    "imported_delta_exponent": 1,
                    "source_delta_exponent": 0.5,
                    "imported_prior_delta_exponent": 1,
                    "source_prior_delta_exponent": 0.5,
                }
                if claim_id == 6
                else claim3_proof
                if claim_id == 3
                else claim5_proof
                if claim_id == 5
                else claim4_proof
                if claim_id == 4
                else {}
            ),
        }
        write(claim_dir / "raw_results.json", json.dumps(raw, indent=2) + "\n")
        write(
            claim_dir / "verifier_output.txt",
            f"VERDICT={contract['verdict']}\nREASON={contract['reason']}\n",
        )
        if claim_id == 3:
            write(
                claim_dir / "proof_certificate.json",
                json.dumps(claim3_proof, indent=2, sort_keys=True) + "\n",
            )
        if claim_id == 4:
            write(
                claim_dir / "proof_certificate.json",
                json.dumps(claim4_proof, indent=2, sort_keys=True) + "\n",
            )
        if claim_id == 5:
            write(
                claim_dir / "proof_certificate.json",
                json.dumps(claim5_proof, indent=2, sort_keys=True) + "\n",
            )
        write(claim_dir / "limitations.md", limitations_text(contract))

    normal_rc, normal_output = run_checker([str(ARTIFACT_ROOT)])
    claim6_mutant_rc, claim6_mutant_output = run_checker(
        [str(ARTIFACT_ROOT), "--mutate-claim6-source-exponent"]
    )
    claim3_mutant_rc, claim3_mutant_output = run_checker(
        [str(ARTIFACT_ROOT), "--mutate-claim3-window"]
    )
    claim5_mutant_rc, claim5_mutant_output = run_checker(
        [str(ARTIFACT_ROOT), "--mutate-claim5-null-marginal"]
    )
    claim4_mutant_rc, claim4_mutant_output = run_checker(
        [str(ARTIFACT_ROOT), "--mutate-claim4-information-budget"]
    )
    if normal_rc != 0:
        print(normal_output)
        return 1
    if 0 in {
        claim3_mutant_rc,
        claim4_mutant_rc,
        claim5_mutant_rc,
        claim6_mutant_rc,
    }:
        print("NEGATIVE CONTROL FAILED: a mutated certificate was accepted")
        return 1

    elapsed_s = time.perf_counter() - started
    env = environment_record(elapsed_s)
    for contract in CONTRACTS:
        claim_dir = ARTIFACT_ROOT / f"claim_{contract['claim_id']}"
        write(claim_dir / "independent_checker_output.txt", normal_output)
        write(
            claim_dir / "negative_control_output.txt",
            "CLAIM3_EXPECTED_NONZERO_EXIT=1\n"
            f"CLAIM3_OBSERVED_EXIT={claim3_mutant_rc}\n"
            f"{claim3_mutant_output}\n"
            "CLAIM4_EXPECTED_NONZERO_EXIT=1\n"
            f"CLAIM4_OBSERVED_EXIT={claim4_mutant_rc}\n"
            f"{claim4_mutant_output}\n"
            "CLAIM5_EXPECTED_NONZERO_EXIT=1\n"
            f"CLAIM5_OBSERVED_EXIT={claim5_mutant_rc}\n"
            f"{claim5_mutant_output}\n"
            "CLAIM6_EXPECTED_NONZERO_EXIT=1\n"
            f"CLAIM6_OBSERVED_EXIT={claim6_mutant_rc}\n"
            f"{claim6_mutant_output}",
        )
        write(
            claim_dir / "command_environment.json",
            json.dumps(env, indent=2, sort_keys=True) + "\n",
        )
        write(
            claim_dir / "EVAL.md",
            f"# Claim {contract['claim_id']}: {contract['verdict']}\n\n"
            f"{contract['reason']}\n\n"
            f"Fixed command: `{FIXED_COMMAND}`\n\n"
            "This verdict uses the exact three-token vocabulary required by the campaign.\n",
        )

    verifier = subprocess.run(
        [
            sys.executable,
            str(ROOT / "repro/src/verify_claim_artifacts.py"),
            str(ARTIFACT_ROOT),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    verifier_output = verifier.stdout + verifier.stderr
    if verifier.returncode != 0:
        print(verifier_output)
        return verifier.returncode

    verdicts = {item["claim_id"]: item["verdict"] for item in CONTRACTS}
    summary = {
        "git_sha": env["git_sha"],
        "command": FIXED_COMMAND,
        "runtime_seconds": env["runtime_seconds"],
        "verdicts": verdicts,
        "negative_control_exits": {
            "claim_3": claim3_mutant_rc,
            "claim_4": claim4_mutant_rc,
            "claim_5": claim5_mutant_rc,
            "claim_6": claim6_mutant_rc,
        },
        "artifact_verifier_exit": verifier.returncode,
    }
    write(ARTIFACT_ROOT / "summary.json", json.dumps(summary, indent=2) + "\n")
    write(
        ARTIFACT_ROOT / "EVAL.md",
        "# Claim-contract audit\n\n"
        + "\n".join(
            f"- Claim {claim_id}: **{verdict}**"
            for claim_id, verdict in verdicts.items()
        )
        + "\n\n"
        + "The localized VC/ERM certificate verifies Claim 3, and an independent "
        "corrected RCN construction verifies Claim 4. Exact arithmetic falsifies "
        "Claim 5, while the source comparison retains Claim 6's falsification. "
        "Claims 1 and 2 remain BLOCKED.\n",
    )

    print(verifier_output.strip())
    print("CLAIM CONTRACT SUMMARY")
    for claim_id, verdict in verdicts.items():
        print(f"CLAIM_{claim_id}_VERDICT={verdict}")
    print(
        "NEGATIVE_CONTROL_EXITS="
        f"claim3:{claim3_mutant_rc},claim4:{claim4_mutant_rc},"
        f"claim5:{claim5_mutant_rc},"
        f"claim6:{claim6_mutant_rc} "
        "(expected nonzero)"
    )
    print(f"RUNTIME_SECONDS={env['runtime_seconds']}")
    print("wrote .openresearch/artifacts/")
    return 0
