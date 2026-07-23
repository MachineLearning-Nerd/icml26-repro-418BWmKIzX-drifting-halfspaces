"""Run the cumulative claim-contract verification suite.

This entrypoint intentionally does not interpret a numerical trend as evidence
for an asymptotic theorem.  Each research branch extends ``claim_suite.py`` and
keeps this command fixed.
"""

from claim_suite import main


if __name__ == "__main__":
    raise SystemExit(main())
