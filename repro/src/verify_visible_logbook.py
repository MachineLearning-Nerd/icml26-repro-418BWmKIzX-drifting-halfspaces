"""Fail closed when exact-claim evidence is not visible in the logbook.

The live judge reads logbook pages, not arbitrary repository paths. This
validator cross-checks each visible dossier against the generated artifact
bundle and rejects summaries that merely point at hidden evidence.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_ROOT = ROOT / ".openresearch" / "artifacts"
SPACE_ROOT = ROOT / "release" / "hf-space-overlay"
SOURCE_HASH = "6b04e5b5b624ce99606d018a6dcfd2278d1448b36e555b0b7ce41c95105e1240"

PAGE_SPECS = {
    1: {
        "slug": "claim-1-efficient-learner",
        "file": "pages/exact-claim-audit/claim-1/page.md",
        "markers": [
            "gradient_bound",
            "projected_regret",
            "regret_to_error",
            "independent_selection",
            "Delta^{-2/3}",
            "Delta^{1/3}/\\gamma",
            "CLAIM1_OBSERVED_EXIT=1",
        ],
    },
    2: {
        "slug": "claim-2-conditional-hardness",
        "file": "pages/exact-claim-audit/claim-2/page.md",
        "markers": [
            "valid Theorem 4.1 certificate plus a valid testing-to-learning reduction",
            "degree-one",
            "does not logically falsify",
            "CLAIM2_OBSERVED_EXIT=1",
        ],
    },
    3: {
        "slug": "claim-3-vc-massart-upper-bound",
        "file": "pages/exact-claim-audit/claim-3/page.md",
        "markers": [
            "tv_telescope",
            "massart_bernstein",
            "localized_vc_deviation",
            "erm_basic_inequality",
            "\\sqrt{d\\Delta/q}",
            "CLAIM3_OBSERVED_EXIT=1",
        ],
    },
    4: {
        "slug": "claim-4-rcn-lower-bound",
        "file": "pages/exact-claim-audit/claim-4/page.md",
        "markers": [
            "halfspace_realizability",
            "tv_drift",
            "information_budget",
            "probability_quantifier",
            "risk_reduction",
            "d/1600",
            "0.13724791747815518",
            "CLAIM4_OBSERVED_EXIT=1",
        ],
    },
    5: {
        "slug": "claim-5-low-degree-counterexample",
        "file": "pages/exact-claim-audit/claim-5/page.md",
        "markers": [
            "definition_4_1_null_p_y_plus",
            "definition_4_3_null_p_y_plus",
            "standardized_gap_squared",
            "p(z)=\\sum_{i=1}^{T} y_i",
            "T=2",
            "CLAIM5_OBSERVED_EXIT=1",
        ],
    },
    6: {
        "slug": "claim-6-source-transcription",
        "file": "pages/exact-claim-audit/claim-6/page.md",
        "markers": [
            "imported_delta_exponent",
            "source_delta_exponent",
            "\\sqrt{\\Delta}\\gamma^{-3/2}",
            "\\Delta\\gamma^{-3/2}",
            "CLAIM6_OBSERVED_EXIT=1",
        ],
    },
}

REQUIRED_HEADINGS = [
    "## Source contract",
    "## Assumptions and quantifiers",
    "## Decisive evidence shown inline",
    "## Independent checker",
    "## Negative control",
    "## Limitations",
    "## Verdict",
]


def exact_audit_node(logbook: dict) -> dict | None:
    for child in logbook["root"]["children"]:
        if child["slug"] == "exact-claim-audit":
            return child
    return None


def validate(page_overrides: dict[int, str] | None = None) -> list[str]:
    failures: list[str] = []
    logbook = json.loads((SPACE_ROOT / "logbook.json").read_text())
    audit_node = exact_audit_node(logbook)
    if audit_node is None:
        return ["missing exact-claim-audit navigation node"]

    children = {child["slug"]: child for child in audit_node["children"]}
    if logbook.get("agent_view_tokens", 0) < 12000:
        failures.append("agent_view_tokens is too small for the visible dossiers")

    for claim_id, spec in PAGE_SPECS.items():
        contract = json.loads(
            (ARTIFACT_ROOT / f"claim_{claim_id}" / "claim_contract.json").read_text()
        )
        raw = json.loads(
            (ARTIFACT_ROOT / f"claim_{claim_id}" / "raw_results.json").read_text()
        )
        nav = children.get(spec["slug"])
        if nav is None:
            failures.append(f"claim {claim_id}: missing navigation child")
            continue
        if nav["file"] != spec["file"]:
            failures.append(f"claim {claim_id}: navigation file mismatch")

        page_file = SPACE_ROOT / spec["file"]
        if not page_file.exists():
            failures.append(f"claim {claim_id}: missing visible page")
            continue
        text = (
            page_overrides[claim_id]
            if page_overrides and claim_id in page_overrides
            else page_file.read_text()
        )

        required = [
            f"# Claim {claim_id}",
            f"Verdict: **{contract['verdict']}**",
            f"Theorem {contract['theorem']}",
            f"`#{contract['anchor']}`",
            SOURCE_HASH,
            "INDEPENDENT CHECK: OK",
            *REQUIRED_HEADINGS,
            *contract["assumptions"],
            *contract["quantifiers"],
            *spec["markers"],
        ]
        for marker in required:
            if marker not in text:
                failures.append(f"claim {claim_id}: missing visible marker {marker!r}")

        if raw["verdict"] != contract["verdict"]:
            failures.append(f"claim {claim_id}: artifact verdict mismatch")
        if contract["verdict"] == "VERIFIED":
            obligations = raw["observations"]["proof_obligations"]
            for name, item in obligations.items():
                if name not in text or item["basis"] not in text:
                    failures.append(
                        f"claim {claim_id}: proof obligation {name!r} is not shown"
                    )
        if contract["verdict"] == "FALSIFIED" and not raw["exact_contradiction"]:
            failures.append(f"claim {claim_id}: falsification lacks contradiction")
        if contract["verdict"] == "BLOCKED":
            blocker = raw["blocking_obligation"]
            if not blocker or blocker not in text:
                failures.append(f"claim {claim_id}: blocker is not shown")

    return failures


def main() -> int:
    failures = validate()
    if failures:
        print("VISIBLE LOGBOOK VERIFIER: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    mutation_failures: list[str] = []
    for claim_id, spec in PAGE_SPECS.items():
        page = (SPACE_ROOT / spec["file"]).read_text()
        decisive_marker = spec["markers"][0]
        mutated = page.replace(decisive_marker, "REMOVED_DECISIVE_EVIDENCE", 1)
        detected = validate({claim_id: mutated})
        if not detected:
            mutation_failures.append(
                f"claim {claim_id}: missing decisive evidence was accepted"
            )

    if mutation_failures:
        print("VISIBLE LOGBOOK NEGATIVE CONTROL: FAIL")
        for failure in mutation_failures:
            print(f"- {failure}")
        return 1

    print("VISIBLE LOGBOOK VERIFIER: OK")
    print("Six navigable claim dossiers expose contracts, decisive evidence, and limits.")
    print("VISIBLE_LOGBOOK_NEGATIVE_CONTROLS=claim1:1,claim2:1,claim3:1,claim4:1,claim5:1,claim6:1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
