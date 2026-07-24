# Claim 6 — realizable-rate source transcription

Verdict: **FALSIFIED**

The imported judged claim changes the power of \(\Delta\) in both the new and
prior rates. This dossier compares that claim against the exact source
theorem; it does not substitute a small numerical trial.

## Source contract

- Paper: *Efficiently Learning Drifting Halfspaces with Massart Noise*,
  arXiv `2606.11149v1`.
- Theorem 3.2, anchor `#S3.Thmtheorem2`.
- Retrieved HTML SHA-256:
  `6b04e5b5b624ce99606d018a6dcfd2278d1448b36e555b0b7ce41c95105e1240`.
- Domain: realizable drifting \(\gamma\)-margin halfspaces.

## Assumptions and quantifiers

The source assumptions are:

> successive labeled distributions have total variation at most Delta

> labels are realizable by a gamma-margin halfspace at every time

The theorem quantifies:

> there exists an algorithm A

> for any T = Omega_tilde((gamma Delta)^(-1/2))

> with probability at least 9/10

## Decisive evidence shown inline

The exact side-by-side contract is:

| Quantity | Imported judged claim | Theorem 3.2 source |
|---|---:|---:|
| New rate | \(\widetilde O(\Delta\gamma^{-3/2})\) | \(\widetilde O(\sqrt{\Delta}\gamma^{-3/2})\) |
| Prior rate | \(\widetilde O(\Delta\gamma^{-2})\) | \(\widetilde O(\sqrt{\Delta}\gamma^{-2})\) |
| Recorded exponent | `imported_delta_exponent = 1` | `source_delta_exponent = 0.5` |

In literal source notation, the conflicting terms are
`\Delta\gamma^{-3/2}` and `\sqrt{\Delta}\gamma^{-3/2}`. They are not
asymptotically interchangeable: their ratio is \(\sqrt{\Delta}\), which
vanishes as \(\Delta\to0\). The same exponent mismatch occurs in the quoted
prior-best comparison.

## Independent checker

`INDEPENDENT CHECK: OK`

The checker parses the source theorem's symbolic rate and the imported claim,
extracts their \(\Delta\) exponents, and requires the exact mismatch
\(1\ne1/2\) in both formulas.

Raw paths:
`evidence/visible-dossier-audit/claim_6/claim_contract.json` and
`raw_results.json`.

## Negative control

The mutant changes the source exponent to one. The mismatch then disappears,
so falsification is correctly rejected:

```text
CLAIM6_OBSERVED_EXIT=1
```

## Limitations

This verdict applies to the **imported claim transcription**, not to the
actual Theorem 3.2. The source theorem states a
\(\widetilde O(\sqrt{\Delta}\gamma^{-3/2})\) guarantee and compares it with
\(\widetilde O(\sqrt{\Delta}\gamma^{-2})\). Verifying the proof of that actual
theorem is a different contract and is not claimed here.

## Verdict

**FALSIFIED.** The imported claim uses \(\Delta^1\), whereas the exact source
uses \(\Delta^{1/2}\) in both the new and prior rates.
