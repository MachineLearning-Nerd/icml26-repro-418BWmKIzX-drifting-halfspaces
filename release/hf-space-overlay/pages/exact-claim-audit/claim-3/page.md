# Claim 3 - VC/Massart upper bound

Verdict: **VERIFIED**

This is a proof certificate for the specific
\(\widetilde O(\sqrt{d\Delta/(1-2\eta)})\) rate, not a claim that error merely
increases with dimension.

## Source contract

- Paper: arXiv `2606.11149v1`
- Theorem 2.1, HTML anchor `#S2.Thmtheorem1`
- Source HTML SHA-256:
  `6b04e5b5b624ce99606d018a6dcfd2278d1448b36e555b0b7ce41c95105e1240`
- Conclusion:
  \[
  R_t(\widehat h)-\operatorname{opt}_t
  =\widetilde O\!\left(\sqrt{\frac{d\Delta}{1-2\eta}}\right).
  \]

## Assumptions and quantifiers

Assumptions:

- successive labeled distributions have total variation at most Delta
- each distribution is realized by a member of the class with eta-Massart noise

Quantifiers:

- for every drifting sequence satisfying the assumptions
- there exists an information-theoretic algorithm A
- for every t = Omega_tilde(d/((1-2eta)Delta))
- with probability at least 9/10

Write \(q=1-2\eta>0\).

## Decisive evidence shown inline

The algorithm is sliding-window empirical risk minimization (`DriftedERM`) with

\[
W=\widetilde\Theta\!\left(\sqrt{\frac d{q\Delta}}\right).
\]

### Obligation table

| Machine key | Statement discharged | Basis checked |
| --- | --- | --- |
| `tv_telescope` | \(|\mathbb E_t f-\mathbb E_T f|\le(T-t)\Delta\) for \(f\in[0,1]\). | `total-variation dual characterization and triangle inequality` |
| `massart_bernstein` | \(R_T(h)-R_T(h_T^\star)\ge q\,P_T[h(X)\ne h_T^\star(X)]\). | `pointwise conditional-risk identity under eta(x)<=eta` |
| `localized_vc_deviation` | Uniform localized deviation is \(\widetilde O(\sqrt{dV(h)/W}+d/W)\). | `symmetrization, the standard VC entropy bound, Dudley's sqrt(log N) integral, Talagrand/Bernstein concentration, and dyadic peeling` |
| `erm_basic_inequality` | Excess risk is \(\widetilde O(d/(qW)+\Delta W)\). | `ERM empirical excess <=0, localized deviation, Massart variance control, and Young's inequality` |
| `between_epoch_transfer` | Transfer to the queried time adds at most \(2W\Delta\). | `TV telescope for learner risk and optimal risk` |

The ERM basic inequality follows by combining empirical optimality with the
localized deviation and using
\(\sqrt{ax}\le a/2+x/2\). The checker symbolically verifies that the slack is a
square:

\[
-\sqrt{a}\sqrt{x}+\frac a2+\frac x2
=\frac12(\sqrt a-\sqrt x)^2\ge0.
\]

### Exact window optimization

At \(W=\sqrt{d/(q\Delta)}\),

\[
\frac d{qW}
=\frac d{q\sqrt{d/(q\Delta)}}
=\sqrt{\frac{d\Delta}{q}},
\]

and

\[
\Delta W
=\Delta\sqrt{\frac d{q\Delta}}
=\sqrt{\frac{d\Delta}{q}}.
\]

Thus both estimation and drift equal the target
\(\sqrt{d\Delta/q}\). The required time
\(\widetilde\Omega(d/(q\Delta))\) is \(W^2\) up to logarithms, so the window is
available at every quantified time.

For \(x=d\Delta\in(0,1)\), \(x^{1/2}<x^{1/3}\); hence the certified Massart
dependence is strictly better in exponent than the quoted adversarial
\(\Theta((d\Delta)^{1/3})\) rate in the small-drift regime.

### Source repairs

The audit uses \(\sqrt{\log N(\epsilon)}\) in Dudley's integral; the printed
display omits the square root although its following bound uses the correct
form. It also reads `V(r)` as `H(r)` and closes a missing parenthesis in the
time condition.

## Independent checker

The independent implementation reconstructs \(W\), simplifies both rate terms
with SymPy, checks all five obligation statuses, and verifies the exact source
hash and theorem anchor.

```text
INDEPENDENT CHECK: OK
All source hashes, theorem anchors, verdict tokens, Claim 1/3/4 proof algebra,
and exact Claim 5/6 contradictions agree.
```

Raw paths:
`evidence/visible-dossier-audit/claim_3/proof_certificate.json`,
`raw_results.json`, and `independent_checker_output.txt`.

## Negative control

The mutation replaces the optimal \(\Delta^{-1/2}\) window exponent by
\(\Delta^{-1/3}\):

```text
CLAIM3_EXPECTED_NONZERO_EXIT=1
CLAIM3_OBSERVED_EXIT=1
INDEPENDENT CHECK: FAIL
- claim 3: incorrect balancing window
```

## Limitations

- This verifies the theorem's asymptotic proof and probability level, not a
  hidden leading constant.
- It uses the standard VC entropy and concentration lemmas under their stated
  hypotheses; it does not implement an inefficient ERM oracle for every class.
- The adversarial-rate comparison is an exponent comparison to the cited prior
  result, not a new reproduction of that prior paper.
- No random trials are used.

## Verdict

The TV, Massart/Bernstein, localized VC, ERM, time, and rate obligations are
all discharged. Verdict: **VERIFIED**.
