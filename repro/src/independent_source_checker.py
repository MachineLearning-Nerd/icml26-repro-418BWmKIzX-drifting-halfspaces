"""Independent checker for source-contract integrity and the Claim 6 mismatch."""

from __future__ import annotations

import argparse
import json
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

    if failures:
        print("INDEPENDENT CHECK: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("INDEPENDENT CHECK: OK")
    print("All source hashes, theorem anchors, verdict tokens, and Claim 6 exponents agree.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
