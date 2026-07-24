# Exact claim audit

The previous live judge evaluated Space revision
`031b53f092c2ff4eef64d8e8a5b9d907956f4176` as **4/12**. Its specific criticism
was that this page named proof certificates but did not show their contents.
This candidate therefore adds six navigable dossiers below. Each dossier
renders the source contract, assumptions, quantifiers, decisive algebra,
independent-checker result, mutation that fails, and limitations directly in
Markdown. The judge does not need to open a repository artifact to assess them.

This additive audit replaces none of the judged logbook. The original judged
revision `5f91ea8e5a386773b73437d8be494480363b0293`, the 4/12 revision, and every
pre-existing path remain reachable. This candidate has not been judged and
does not claim a score increase.

## Outcome

| Claim | Exact verdict | Direct result |
| --- | --- | --- |
| 1. Efficient Massart learner | **VERIFIED** | The Algorithms 1–2 certificate closes gradient, regret, drift, validation, epoch transfer, runtime, and probability obligations. |
| 2. Conditional efficient hardness | **BLOCKED** | The supplied Theorem 4.1 route is contradicted, but no efficient learner falsifies the conditional conclusion. |
| 3. VC/Massart upper bound | **VERIFIED** | A localized VC/Bernstein certificate and independent checker establish the stated balancing rate. |
| 4. RCN information lower bound | **VERIFIED** | An independent corrected construction closes total variation, capacity, Fano, risk, and horizon obligations. |
| 5. Low-degree trajectory theorem | **FALSIFIED** | The source's inconsistent null gives a degree-one 1-distinguisher at trajectory length \(T=2\). |
| 6. Imported realizable rate | **FALSIFIED** | The imported \(\Delta\) rate contradicts Theorem 3.2's \(\sqrt{\Delta}\) rate. This does not falsify the paper's actual theorem. |

## Visible proof dossiers

| Dossier | What is rendered |
| --- | --- |
| [Claim 1 - efficient learner proof](#/claim-1-efficient-learner) | Eight proof obligations and the exact \(\Delta^{1/3}/\gamma\) balance. |
| [Claim 2 - conditional hardness](#/claim-2-conditional-hardness) | The precise unresolved obligation and why Claim 5 does not falsify the conditional conclusion. |
| [Claim 3 - VC/Massart upper bound](#/claim-3-vc-massart-upper-bound) | TV transfer, Massart/Bernstein localization, ERM inequality, and window optimization. |
| [Claim 4 - RCN lower bound](#/claim-4-rcn-lower-bound) | Full independent construction, information budget, generalized Fano calculation, and risk reduction. |
| [Claim 5 - degree-one counterexample](#/claim-5-low-degree-counterexample) | Exact null/alternative marginals and rational-arithmetic distinguisher calculation. |
| [Claim 6 - source transcription](#/claim-6-source-transcription) | Side-by-side imported and source formulas with exponents. |

The freshly regenerated evidence remains machine-readable at
`evidence/visible-dossier-audit/`. The prior published evidence at
`evidence/exact-claim-audit/` remains byte-identical. Every dossier also identifies the corresponding
raw paths. Each numbered claim directory contains:

- `claim_contract.json` and `source_audit.md`;
- `method.md`, raw JSON output, and any proof certificate;
- primary verifier and independent-checker output;
- a negative-control output whose process exits nonzero;
- the exact command, locked environment, Git SHA, CPU details, and runtime;
- `EVAL.md` plus explicit limitations and deviations.

The fixed command on every experiment node is:

```text
uv run --frozen python repro/src/verify_hs.py
```

## How this answers the prior judge criticisms

The earlier \(d=5\), \(N=500\), four-seed trials only checked monotonic trends.
They did not instantiate the paper's algorithm, margin assumptions, total
variation drift, RCN construction, low-degree testing problem, or exact rate
laws. The new evidence does not promote those trials. It replaces them with
machine-checked theorem contracts and exact contradictions.

- Claims 1 and 3 check the actual proof balances and all supporting
  obligations rather than fitting tiny empirical slopes.
- Claim 4 records the printed proof's factor-\(d\) defect and verifies the
  theorem only through a separate corrected construction.
- Claim 5 evaluates the exact null and alternative distributions, yielding an
  explicit degree-one contradiction.
- Claim 6 compares the imported text directly with the theorem source rather
  than comparing noisy toy errors.
- Claim 2 remains BLOCKED because falsifying its proof route does not logically
  falsify its conjecture-conditional conclusion.

The old Claim 4 and Claim 6 contradictions remain visible on the original
pages as historical evidence. They are not used to support these new verdicts.

## Source and environment lock

The arXiv HTML was retrieved on `2026-07-23T13:09:55Z` with an explicit browser
User-Agent. Its SHA-256 is
`6b04e5b5b624ce99606d018a6dcfd2278d1448b36e555b0b7ce41c95105e1240`.
The source archive SHA-256 is
`9679e85743076e711da671b3a875182173441e5f6ecb41e7e56d3d36647e9221`.
The locked environment uses CPython 3.12.11, `uv.lock`, and one repository
`.venv`. All formal work ran on local Apple M2 CPU; Hugging Face compute was
unused and cost $0.

## Limitations

Claims 1, 3, and 4 are proof reproductions, not finite-sample demonstrations of
hidden constants. Claim 4 verifies the asymptotic theorem through an
independent repair and does not validate the printed proof. Claim 5 is
falsified only as written; a consistent null might support a corrected
theorem. Claim 6 is a falsification of the imported judge wording, not of the
paper's actual \(\sqrt{\Delta}\) theorem. Claim 2 remains unresolved.
