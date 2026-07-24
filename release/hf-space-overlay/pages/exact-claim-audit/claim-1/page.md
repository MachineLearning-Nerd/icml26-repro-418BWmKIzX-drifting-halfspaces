# Claim 1 - Efficient learner proof

Verdict: **VERIFIED**

This page shows the certificate itself. It does not rely on the old
\(d=5,N=500\) trend experiment and does not infer an asymptotic exponent from a
fit.

## Source contract

- Paper: arXiv `2606.11149v1`
- Theorem 1.1, HTML anchor `#S1.Thmtheorem1`
- Source HTML SHA-256:
  `6b04e5b5b624ce99606d018a6dcfd2278d1448b36e555b0b7ce41c95105e1240`
- Required conclusion:
  \[
  \operatorname{err}_T(A)\le
  \eta+\widetilde O(\Delta^{1/3}/\gamma)
  \]
  in time polynomial in \(d,1/\gamma,1/\Delta\).

## Assumptions and quantifiers

Assumptions, copied from the machine contract:

- successive labeled distributions have total variation at most Delta
- each target is a homogeneous halfspace on the unit sphere
- all examples have margin at least gamma
- conditional label-flip probability is at most eta < 1/2

Quantifiers:

- there exists an algorithm A
- for any T = Omega_tilde(Delta^(-2/3))
- with probability at least 9/10

## Decisive evidence shown inline

The audited algorithm is `DriftedMassart` with the `DriftPerceptron`
subroutine. Set epoch length \(W=\widetilde\Theta(\Delta^{-2/3})\), first-half
sample size \(m=W/2\), and projected-gradient step
\(\mu=\gamma/\sqrt m\).

### Obligation table

| Machine key | Statement discharged | Basis checked |
| --- | --- | --- |
| `gradient_bound` | \(\lVert g(w;x,y)\rVert_2\le 2/\gamma\) | `||x||=1 and the numerator is in [-2,2] while max{|w dot x|,gamma}>=gamma` |
| `projected_regret` | Average population gradient regret is \(O(1/(\gamma\sqrt m))\) with high probability. | `projection nonexpansivity, telescoping potential, and Azuma-Hoeffding for the bounded martingale differences` |
| `regret_to_error` | \(\mathbb E[g_i\cdot(w-v)]\ge2(\operatorname{err}_i(w)-\eta)-F_i\), with \(\mathbb EF_i=O(m\Delta/\gamma)\). | `four sign/margin cases; on points where current and final targets agree and the final margin is at least gamma the inequality is pointwise, while the weighted exceptional terms are bounded by the joint-TV drift via its dual form` |
| `iterate_existence` | Some first-half iterate has error \(\eta+\widetilde O(\Delta^{1/3}/\gamma)\). | `minimum excess is at most average excess` |
| `independent_selection` | The independent second half selects an iterate within \(\widetilde O(\Delta^{1/3})\) of the best final-time risk. | `candidate iterates depend only on the first half; Hoeffding plus a union bound applies on the independent second half, followed by TV transfer to epoch end` |
| `all_eligible_times` | For every eligible \(T\), boundary transfer adds \(O(\Delta^{1/3})\). | `TV telescoping over at most one epoch` |
| `runtime` | Runtime is polynomial in \(d,1/\gamma,1/\Delta\). | `W projected d-dimensional updates and at most W^2 candidate-validation evaluations per epoch` |
| `success_probability` | Success probability is at least \(9/10\). | `allocate failure probability 1/20 to martingale control and 1/20 to validation; union bound gives 9/10` |

### Rate calculation

Projected regret contributes

\[
\frac{1}{\gamma\sqrt W}.
\]

The weighted total-variation exception contributes

\[
\frac{W\Delta}{\gamma}.
\]

At \(W=\Delta^{-2/3}\), both become

\[
\frac{1}{\gamma\sqrt{\Delta^{-2/3}}}
=\frac{\Delta^{1/3}}{\gamma},
\qquad
\frac{\Delta\Delta^{-2/3}}{\gamma}
=\frac{\Delta^{1/3}}{\gamma}.
\]

The independent-validation deviation is
\(\widetilde O(W^{-1/2})=\widetilde O(\Delta^{1/3})\), which is no larger than
\(\widetilde O(\Delta^{1/3}/\gamma)\) for \(0<\gamma\le1\). Thus optimization,
drift, validation, and between-epoch transfer all fit the stated rate.

### Source repairs made explicit

The checker does not silently accept notation defects:

1. the undefined update symbol \(g_t\) is read as the gradient defined one line
   earlier;
2. Azuma-Hoeffding is applied to \(\lambda\sum_t\xi_t\) with the missing
   \(\lambda\) restored;
3. the two-sided Hoeffding term uses \(\log(W/\delta)\), and the two failure
   events receive \(1/20\) each;
4. epoch and validation indices are made consistent.

## Independent checker

The separate program reloaded the JSON contract and certificate, checked the
source hash and theorem anchor, required all eight statuses to be
`discharged`, and recomputed the exponent identities.

```text
INDEPENDENT CHECK: OK
All source hashes, theorem anchors, verdict tokens, Claim 1/3/4 proof algebra,
and exact Claim 5/6 contradictions agree.
```

Raw paths:
`evidence/exact-claim-audit/claim_1/proof_certificate.json`,
`raw_results.json`, and `independent_checker_output.txt`.

## Negative control

The mutation changes the epoch exponent from \(-2/3\) to \(-1/2\). The
independent checker must reject it:

```text
CLAIM1_EXPECTED_NONZERO_EXIT=1
CLAIM1_OBSERVED_EXIT=1
INDEPENDENT CHECK: FAIL
- claim 1: epoch does not balance the error terms
```

## Limitations

- This verifies the asymptotic proof with the same polylogarithmic suppression
  as the theorem; it does not estimate hidden leading constants.
- It is a proof reproduction, not a finite-dimensional benchmark.
- The listed notation repairs are deviations from the printed presentation,
  not changes to the theorem contract.
- No random trials are used, so the deterministic seed list is empty.

## Verdict

All assumptions, quantifiers, rate terms, runtime, and the \(9/10\) probability
budget are discharged. Verdict: **VERIFIED**.
