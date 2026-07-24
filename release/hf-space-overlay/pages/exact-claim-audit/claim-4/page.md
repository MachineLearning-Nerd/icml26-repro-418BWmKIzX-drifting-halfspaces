# Claim 4 — RCN information-theoretic lower bound

Verdict: **VERIFIED**

This dossier verifies the mathematical statement of Theorem 2.2 with an
independent corrected construction. It does **not** certify the printed proof:
the displayed construction in the paper contains an extra factor of \(d\) in
its threshold and is not validated here.

## Source contract

- Paper: *Efficiently Learning Drifting Halfspaces with Massart Noise*,
  arXiv `2606.11149v1`.
- Theorem 2.2, anchor `#S2.Thmtheorem2`.
- Retrieved HTML SHA-256:
  `6b04e5b5b624ce99606d018a6dcfd2278d1448b36e555b0b7ce41c95105e1240`.
- Domain: halfspaces under \(\eta\)-random classification noise (RCN).
- Claimed lower bound: no algorithm attains
  \(\operatorname{opt}_T+o(\sqrt{d\Delta/(1-2\eta)})\) with the stated
  uniform probability guarantee.

## Assumptions and quantifiers

The machine-readable contract records the assumption exactly:

> (1-2eta)^3 > d Delta

Its quantifiers are:

> for every T > 0 and Delta in (0,1)

> there exists a family of instances

> no algorithm attains the stated little-o excess error with probability 1/2 on every instance

The asymptotic little-\(o\) statement is checked for \(d\geq40\) with
\(d\Delta/(1-2\eta)^3\to0\); finitely many smaller dimensions do not affect
that asymptotic contract.

## Decisive evidence shown inline

Write \(q=1-2\eta\). Draw \(Z\) uniformly from \(\{0,1\}^d\), draw
\(I\) uniformly from \([d]\), draw \(G\) uniformly from \((0,1)\), and set
\(X=G e_I\). Define

\[
m_\star=\frac1{80}\sqrt{\frac{d}{\Delta q}},\qquad
L=\frac{\Delta m_\star}{q}.
\]

For long horizons the active threshold width is grown during the final
\(\lceil m_\star\rceil\) steps; for shorter horizons the final target is held
static. The target is
\[
h_Z(G e_i)=+1\quad\Longleftrightarrow\quad
Z_i=1\ \text{and}\ G\geq 1-L_t,
\]
and its label is independently flipped with RCN rate
\(\eta=(1-q)/2\).

The independent certificate discharges every proof obligation:

| Obligation | Exact certified basis |
|---|---|
| `halfspace_realizability` | `h_Z(x)=sign(sum_i Z_i x_i-(1-L_t)) on the support {G e_i}` |
| `rcn_contract` | `each target label is independently flipped with eta=(1-q)/2` |
| `tv_drift` | `target disagreement per step <=Delta/q and an RCN label channel contracts it by q, hence joint TV<=Delta` |
| `information_budget` | `BSC capacity C(q)<=q^2 and sum_t L_t q^2 <=2*Delta*q*m_star^2=d/3200<d/1600` |
| `probability_quantifier` | `generalized Fano with the Hamming ball of radius d/4 gives average success <1/2 for d>=40; therefore some Z has success <1/2` |
| `risk_reduction` | `a wrong majority bit forces disagreement on at least half its active interval; d/4 wrong bits imply RCN excess >=Delta*m_star/8` |
| `all_horizons` | `the drifting construction covers T>=ceil(m_star); the static construction covers shorter T with no larger information budget` |

The assumption gives \(L<1/80\). Binary-symmetric-channel capacity satisfies
\[
C(q)=\sum_{k\geq1}\frac{q^{2k}}{2k(2k-1)}
\leq q^2\log2<q^2.
\]
Consequently the long-horizon information budget is \(d/3200\), strictly
below the certified allowance `d/1600`; the static construction uses at most
\(d/6400\).

At the worst certified finite dimension \(d=40\), the generalized-Fano
success upper bound is exactly `0.13724791747815518`, below \(1/2\). A
Hamming error of \(d/4\) then yields RCN excess
\[
\frac{\Delta m_\star}{8}
=\frac{1}{640}\sqrt{\frac{d\Delta}{q}},
\]
which has the theorem's \(\sqrt{d\Delta/(1-2\eta)}\) scaling.

## Independent checker

`INDEPENDENT CHECK: OK`

The checker independently parses the source contract, recomputes the width,
capacity and information inequalities, evaluates the \(d=40\) probability
bound, and checks the Hamming-to-risk reduction and both horizon cases.

Raw paths:
`evidence/visible-dossier-audit/claim_4/claim_contract.json`,
`raw_results.json`, and `proof_certificate.json`.

## Negative control

The observed mutant replaces the certified information allowance by the
incorrect bound \(d\). The fail-closed checker rejects it:

```text
CLAIM4_OBSERVED_EXIT=1
```

Thus a materially weakened information budget cannot be relabeled as this
certificate.

## Limitations

This is a proof-level symbolic reproduction, not an empirical scaling plot.
It independently repairs the theorem, but it does not validate the paper's
printed threshold containing the extra factor \(d\). The constants are
conservative and only the asymptotic lower-bound statement is claimed.

## Verdict

**VERIFIED.** The corrected construction satisfies halfspace realizability,
RCN, TV drift, information, probability, risk, and all-horizon obligations,
establishing the exact Theorem 2.2 lower-bound scaling.
