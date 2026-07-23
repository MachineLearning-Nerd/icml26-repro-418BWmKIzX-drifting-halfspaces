"""Fail-closed static audit of the judged baseline implementation."""

from __future__ import annotations

import ast
import json
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / ".openresearch" / "artifacts" / "pseudocode_audit"
FROZEN_BASELINE_SHA = "4b976c8acfb983bb4d74d944f9a5ba25e98667e7"


def loaded_names(function: ast.FunctionDef) -> set[str]:
    return {
        node.id
        for node in ast.walk(function)
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)
    }


def functions(path: Path) -> dict[str, ast.FunctionDef]:
    tree = ast.parse(path.read_text())
    return {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
    }


def audit() -> dict[str, bool]:
    halfspace_path = ROOT / "repro/src/halfspaces.py"
    verifier_path = ROOT / "repro/src/verify_hs.py"
    baseline_verifier = subprocess.check_output(
        ["git", "show", f"{FROZEN_BASELINE_SHA}:repro/src/verify_hs.py"],
        cwd=ROOT,
        text=True,
    )
    halfspace_text = halfspace_path.read_text()
    parsed = functions(halfspace_path)
    generator = parsed["make_drifting_data"]
    learner = parsed["learn_halfspace"]
    generator_names = loaded_names(generator)
    learner_args = {argument.arg for argument in learner.args.args}

    return {
        "gamma_argument_unused": "gamma" not in generator_names,
        "examples_not_unit_normalized": "X.append(x)" in halfspace_text
        and "x /= np.linalg.norm(x)" not in halfspace_text,
        "margin_not_enforced": "margin = abs(x @ w)" in halfspace_text
        and "margin < gamma" not in halfspace_text,
        "drift_not_defined_as_tv": "w + drift * rng.standard_normal(d)" in halfspace_text,
        "learner_has_no_eta_input": "eta" not in learner_args,
        "paper_gradient_absent": "(1 - 2 * eta)" not in halfspace_text
        and "(1-2*eta)" not in halfspace_text,
        "claim4_condition_ignores_reported_min_error": "c4 = excess[-1] > 0.01"
        in baseline_verifier,
        "claim6_condition_uses_low_drift_but_reports_high_drift": (
            "c6 = errs_realizable[0] < errs_by_drift[0]" in baseline_verifier
            and "errs_realizable[-1]" in baseline_verifier
        ),
        "audited_entrypoint_exists": verifier_path.exists(),
    }


def validate(issues: dict[str, bool]) -> tuple[int, list[str]]:
    expected = {
        "gamma_argument_unused",
        "examples_not_unit_normalized",
        "margin_not_enforced",
        "drift_not_defined_as_tv",
        "learner_has_no_eta_input",
        "paper_gradient_absent",
        "claim4_condition_ignores_reported_min_error",
        "claim6_condition_uses_low_drift_but_reports_high_drift",
    }
    missing = sorted(key for key in expected if not issues.get(key))
    return (1 if missing else 0), missing


def main() -> int:
    started = time.perf_counter()
    issues = audit()
    status, missing = validate(issues)
    if status:
        print(f"AUDIT CHECKER: FAIL; missing expected findings: {missing}")
        return status

    mutant = dict(issues)
    mutant["margin_not_enforced"] = False
    mutant_status, mutant_missing = validate(mutant)
    if mutant_status == 0:
        print("NEGATIVE CONTROL: FAIL; mutated audit was accepted")
        return 1

    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    raw = {
        "git_sha": sha,
        "frozen_baseline_sha": FROZEN_BASELINE_SHA,
        "fixed_command": "uv run --frozen python repro/src/verify_hs.py",
        "runtime_seconds": round(time.perf_counter() - started, 6),
        "issues": issues,
        "negative_control": {
            "mutation": "margin_not_enforced=false",
            "exit_code": mutant_status,
            "missing": mutant_missing,
        },
        "assessment": {
            "claims_1_to_6": "BLOCKED",
            "reason": "The judged baseline does not instantiate the paper's domain or algorithms.",
        },
    }
    (ARTIFACTS / "raw_results.json").write_text(json.dumps(raw, indent=2) + "\n")
    (ARTIFACTS / "negative_control_output.txt").write_text(
        f"EXPECTED_NONZERO_EXIT=1\nOBSERVED_EXIT={mutant_status}\nMISSING={mutant_missing}\n"
    )
    (ARTIFACTS / "EVAL.md").write_text(
        "# Executable pseudocode audit\n\n"
        "The baseline fails all eight direct-fidelity checks. In particular, "
        "`gamma` is unused by the generator, no margin is enforced, drift is "
        "not bounded in total variation, and the learner is not Algorithms 1-2. "
        "Claims 4 and 6 also use conditions different from their printed evidence.\n\n"
        "Verdict for every paper claim on this branch: **BLOCKED**.\n"
    )

    print("PSEUDOCODE AUDIT: OK")
    for key, value in issues.items():
        print(f"{key}={value}")
    print(f"NEGATIVE_CONTROL_EXIT={mutant_status} (expected nonzero)")
    print("CLAIMS_1_TO_6=BLOCKED")
    return 0
