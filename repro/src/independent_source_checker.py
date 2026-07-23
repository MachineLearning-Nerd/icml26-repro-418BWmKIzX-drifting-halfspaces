"""Independent checker for source-contract integrity and the Claim 6 mismatch."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path

EXPECTED_HTML_SHA256 = "6b04e5b5b624ce99606d018a6dcfd2278d1448b36e555b0b7ce41c95105e1240"
EXPECTED_ANCHORS = {
    1: "S1.Thmtheorem1",
    2: "S1.Thmtheorem2",
    3: "S2.Thmtheorem1",
    4: "S2.Thmtheorem2",
    5: "S4.Thmtheorem1",
    6: "S3.Thmtheorem2",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact_root", type=Path)
    parser.add_argument("--mutate-claim6-source-exponent", action="store_true")
    parser.add_argument("--mutate-claim5-null-marginal", action="store_true")
    args = parser.parse_args()

    failures: list[str] = []
    for claim_id, expected_anchor in EXPECTED_ANCHORS.items():
        path = args.artifact_root / f"claim_{claim_id}" / "claim_contract.json"
        contract = json.loads(path.read_text())
        if contract["paper"]["html_sha256"] != EXPECTED_HTML_SHA256:
            failures.append(f"claim {claim_id}: unexpected source hash")
        if contract["anchor"] != expected_anchor:
            failures.append(f"claim {claim_id}: unexpected source anchor")
        if contract["verdict"] not in {"VERIFIED", "FALSIFIED", "BLOCKED"}:
            failures.append(f"claim {claim_id}: invalid verdict vocabulary")

        if claim_id == 6:
            source_exponent = contract["conclusion"]["delta_exponent"]
            if args.mutate_claim6_source_exponent:
                source_exponent = 1
            imported_exponent = contract["imported_claim"]["delta_exponent"]
            if source_exponent != 0.5:
                failures.append("claim 6: source exponent is not 1/2")
            if imported_exponent != 1:
                failures.append("claim 6: imported exponent is not 1")
            if imported_exponent == source_exponent:
                failures.append("claim 6: expected source/import mismatch disappeared")
            if contract["verdict"] != "FALSIFIED":
                failures.append("claim 6: mismatch must yield FALSIFIED")
        if claim_id == 5:
            raw = json.loads(
                (args.artifact_root / "claim_5" / "raw_results.json").read_text()
            )
            proof = raw["observations"]
            trajectory_null = Fraction(proof["definition_4_1_null_p_y_plus"])
            if args.mutate_claim5_null_marginal:
                trajectory_null = Fraction(2, 3)
            hard_null = Fraction(proof["definition_4_3_null_p_y_plus"])
            alternative = Fraction(proof["late_step_alternative_p_y_plus"])
            eta = Fraction(proof["eta"])
            length = int(proof["trajectory_length"])
            null_mean = 2 * trajectory_null - 1
            alternative_mean = 2 * alternative - 1
            gap = length * (alternative_mean - null_mean)
            variance = length * (1 - null_mean**2)
            ratio_squared = gap**2 / variance if variance else Fraction(0)
            if trajectory_null != eta:
                failures.append("claim 5: Definition 4.1 null is not eta")
            if hard_null != 1 - eta:
                failures.append("claim 5: Definition 4.3 null is not 1-eta")
            if alternative != 1 - eta:
                failures.append("claim 5: alternative marginal is not 1-eta")
            if ratio_squared < 1:
                failures.append("claim 5: degree-one test is not a 1-distinguisher")
            if proof["polynomial_degree"] != 1:
                failures.append("claim 5: counterexample degree changed")
            if contract["verdict"] != "FALSIFIED":
                failures.append("claim 5: exact contradiction must yield FALSIFIED")

    if failures:
        print("INDEPENDENT CHECK: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("INDEPENDENT CHECK: OK")
    print(
        "All source hashes, theorem anchors, verdict tokens, and exact "
        "Claim 5/6 contradictions agree."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
