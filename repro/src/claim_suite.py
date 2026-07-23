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

from source_contracts import CONTRACTS, PAPER

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
            "proof_obligations_discharged": False,
            "exact_contradiction": claim_id == 6,
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
                else {}
            ),
        }
        write(claim_dir / "raw_results.json", json.dumps(raw, indent=2) + "\n")
        write(
            claim_dir / "verifier_output.txt",
            f"VERDICT={contract['verdict']}\nREASON={contract['reason']}\n",
        )
        write(claim_dir / "limitations.md", limitations_text(contract))

    normal_rc, normal_output = run_checker([str(ARTIFACT_ROOT)])
    mutant_rc, mutant_output = run_checker(
        [str(ARTIFACT_ROOT), "--mutate-claim6-source-exponent"]
    )
    if normal_rc != 0:
        print(normal_output)
        return 1
    if mutant_rc == 0:
        print("NEGATIVE CONTROL FAILED: mutated Claim 6 contract was accepted")
        return 1

    elapsed_s = time.perf_counter() - started
    env = environment_record(elapsed_s)
    for contract in CONTRACTS:
        claim_dir = ARTIFACT_ROOT / f"claim_{contract['claim_id']}"
        write(claim_dir / "independent_checker_output.txt", normal_output)
        write(
            claim_dir / "negative_control_output.txt",
            "EXPECTED_NONZERO_EXIT=1\n"
            f"OBSERVED_EXIT={mutant_rc}\n"
            f"{mutant_output}",
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
        "negative_control_exit": mutant_rc,
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
        + "The source-only round falsifies the imported Claim 6 transcription. "
        "Claims 1-5 remain BLOCKED pending direct proof-obligation evidence.\n",
    )

    print(verifier_output.strip())
    print("CLAIM CONTRACT SUMMARY")
    for claim_id, verdict in verdicts.items():
        print(f"CLAIM_{claim_id}_VERDICT={verdict}")
    print(f"NEGATIVE_CONTROL_EXIT={mutant_rc} (expected nonzero)")
    print(f"RUNTIME_SECONDS={env['runtime_seconds']}")
    print("wrote .openresearch/artifacts/")
    return 0
