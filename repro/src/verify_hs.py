"""Run the cumulative claim-contract verification suite.

This entrypoint intentionally does not interpret a numerical trend as evidence
for an asymptotic theorem.  Each research branch extends ``claim_suite.py`` and
keeps this command fixed.
"""

from claim_suite import main as verify_claims
from verify_visible_logbook import main as verify_visible_logbook


def main() -> int:
    claim_exit = verify_claims()
    if claim_exit != 0:
        return claim_exit
    return verify_visible_logbook()


if __name__ == "__main__":
    raise SystemExit(main())
