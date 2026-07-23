# Exact-claim reproduction: drifting halfspaces

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-418BWmKIzX-drifting-halfspaces/blob/master/notebooks/drifting_halfspaces_reproduction.py)

This repository reproduces the six imported claims for
[*Efficiently Learning Drifting Halfspaces with Massart Noise*](https://arxiv.org/abs/2606.11149).
Because the contributions are theoretical, the replacement evidence uses
source-locked theorem contracts, proof certificates, independent checkers, and
exact counterexamples rather than the earlier \(d=5\), \(N=500\), four-seed
monotonicity tests.

The candidate result is **3 VERIFIED, 2 FALSIFIED, and 1 BLOCKED**. It has not
been published to the Hugging Face Space or evaluated by the live judge, so
this repository does not claim a score increase. The work ran on an Apple M2
local CPU in a locked CPython 3.12/`uv` environment; Hugging Face compute was
not needed.

The strongest paper-versus-observed comparisons are:

- Claim 1 paper rate:
  \(\eta+\widetilde O(\Delta^{1/3}/\gamma)\); observed:
  every proof obligation and the balancing window were independently checked
  (**VERIFIED**).
- Claim 4 paper lower bound:
  \(\widetilde\Omega(\sqrt{d\Delta})\); observed: the printed proof loses a
  factor \(d\), while an independent corrected RCN construction establishes
  the claimed asymptotic scale (**VERIFIED with recorded deviation**).
- Claim 5 paper degree lower bound: no low-degree distinguisher in the stated
  range; observed: the null mismatch gives a degree-one 1-distinguisher at
  \(T=2\) (**FALSIFIED as written**).
- Claim 6 imported rate:
  \(\widetilde O(\Delta\gamma^{-3/2})\); observed: Theorem 3.2 actually states
  \(\widetilde O(\sqrt{\Delta}\gamma^{-3/2})\)
  (**FALSIFIED imported claim, not the paper theorem**).

Read the [illustrated technical report](reports/reproduction/report.md) or
explore the [self-contained marimo tutorial](notebooks/drifting_halfspaces_reproduction.py).
The formal evidence is under `.openresearch/artifacts/` and regenerates with:

```text
uv run --frozen python repro/src/verify_hs.py
```

## Experiment log

Every formal experiment inherited the exact same run command. Branch links
point to the immutable code that produced each recorded result.

| Branch / experiment | Purpose or change | Exact run command | Assessment / outcome | Compute |
| --- | --- | --- | --- | --- |
| [`orx/frozen-judged-baseline`](https://github.com/MachineLearning-Nerd/icml26-repro-418BWmKIzX-drifting-halfspaces/tree/orx/frozen-judged-baseline) | Freeze and reproduce the judged verifier | `uv run --frozen python repro/src/verify_hs.py` | Reproduced its contradictions; retained only as a negative control | Local Apple M2 CPU |
| [`orx/exact-source-contracts`](https://github.com/MachineLearning-Nerd/icml26-repro-418BWmKIzX-drifting-halfspaces/tree/orx/exact-source-contracts) | Bind all six claims to the hashed paper source | `uv run --frozen python repro/src/verify_hs.py` | Claim 6 falsified; Claims 1–5 initially blocked | Local Apple M2 CPU |
| [`orx/upper-bound-proof-certificates`](https://github.com/MachineLearning-Nerd/icml26-repro-418BWmKIzX-drifting-halfspaces/tree/orx/upper-bound-proof-certificates) | Add the localized VC/Massart proof certificate | `uv run --frozen python repro/src/verify_hs.py` | Claim 3 verified | Local Apple M2 CPU |
| [`orx/lower-bound-counterexample-certificates`](https://github.com/MachineLearning-Nerd/icml26-repro-418BWmKIzX-drifting-halfspaces/tree/orx/lower-bound-counterexample-certificates) | Audit the lower-bound constructions | `uv run --frozen python repro/src/verify_hs.py` | Claim 5 falsified; Claim 4 source defect isolated | Local Apple M2 CPU |
| [`orx/claim-1-regret-proof-audit`](https://github.com/MachineLearning-Nerd/icml26-repro-418BWmKIzX-drifting-halfspaces/tree/orx/claim-1-regret-proof-audit) | Certify the efficient learner proof | `uv run --frozen python repro/src/verify_hs.py` | Claim 1 verified | Local Apple M2 CPU |
| [`orx/claim-4-corrected-rcn-lower-bound`](https://github.com/MachineLearning-Nerd/icml26-repro-418BWmKIzX-drifting-halfspaces/tree/orx/claim-4-corrected-rcn-lower-bound) | Add the independent corrected RCN construction | `uv run --frozen python repro/src/verify_hs.py` | Claim 4 verified with the printed-proof deviation preserved | Local Apple M2 CPU |
| [`orx/final-five-claim-cumulative-suite`](https://github.com/MachineLearning-Nerd/icml26-repro-418BWmKIzX-drifting-halfspaces/tree/orx/final-five-claim-cumulative-suite) | Merge and regress all accepted evidence | `uv run --frozen python repro/src/verify_hs.py` | Five exact claims resolved; all five negative controls rejected | Local Apple M2 CPU |
| [`orx/release-candidate-artifacts`](https://github.com/MachineLearning-Nerd/icml26-repro-418BWmKIzX-drifting-halfspaces/tree/orx/release-candidate-artifacts) | Package the evidence, report, notebook, and additive Space overlay | `uv run --frozen python repro/src/verify_hs.py` | Release candidate; publication remains gated on explicit approval | Local Apple M2 CPU |
| `master` (default branch; the repository has no separate `main`) | Public presentation surface | Not run as an experiment (publication surface) | Pending explicit publication approval | N/A |

## Claim status

| Claim | Candidate verdict | Direct evidence |
| --- | --- | --- |
| 1. Efficient Massart learner | VERIFIED | Gradient, regret, drift, validation, runtime, and probability certificate |
| 2. Conditional efficient hardness | BLOCKED | The supplied low-degree route is contradicted; no counterexample to the conditional conclusion |
| 3. VC/Massart upper bound | VERIFIED | Localized VC/Bernstein proof and exact window optimization |
| 4. RCN information lower bound | VERIFIED | Independent construction checking TV, capacity, Fano, risk, and horizon coverage |
| 5. Low-degree trajectory theorem | FALSIFIED | Exact degree-one distinguisher at \(T=2\) |
| 6. Imported realizable rate | FALSIFIED | Imported \(\Delta\) dependence contradicts the source's \(\sqrt{\Delta}\) |

---

## Original reproduction metadata

OpenReview `418BWmKIzX`. arXiv `2606.11149`. 6 claims/12 pts. Owner: loop12pt.
