"""Fail-closed verifier for the durable per-claim evidence bundle."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED = {
    "claim_contract.json",
    "source_audit.md",
    "method.md",
    "raw_results.json",
    "verifier_output.txt",
    "independent_checker_output.txt",
    "negative_control_output.txt",
    "command_environment.json",
    "EVAL.md",
    "limitations.md",
}


def main(root: Path) -> int:
    failures: list[str] = []
    for claim_id in range(1, 7):
        claim_dir = root / f"claim_{claim_id}"
        missing = sorted(REQUIRED - {path.name for path in claim_dir.glob("*")})
        if missing:
            failures.append(f"claim {claim_id}: missing {missing}")
            continue
        contract = json.loads((claim_dir / "claim_contract.json").read_text())
        raw = json.loads((claim_dir / "raw_results.json").read_text())
        if raw["claim_id"] != claim_id:
            failures.append(f"claim {claim_id}: raw claim id mismatch")
        if raw["verdict"] != contract["verdict"]:
            failures.append(f"claim {claim_id}: verdict mismatch")
        if contract["verdict"] == "VERIFIED" and not raw.get("proof_obligations_discharged"):
            failures.append(f"claim {claim_id}: VERIFIED without discharged obligations")
        if contract["verdict"] == "FALSIFIED" and not raw.get("exact_contradiction"):
            failures.append(f"claim {claim_id}: FALSIFIED without an exact contradiction")
        if contract["verdict"] == "BLOCKED" and not raw.get("blocking_obligation"):
            failures.append(f"claim {claim_id}: BLOCKED without a named obligation")

    if failures:
        print("ARTIFACT VERIFIER: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ARTIFACT VERIFIER: OK")
    print("All six fail-closed evidence bundles are complete and internally consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(Path(sys.argv[1])))
