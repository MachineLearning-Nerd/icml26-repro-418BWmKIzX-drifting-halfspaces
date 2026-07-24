# Claim 5 — low-degree theorem counterexample

Verdict: **FALSIFIED**

The counterexample below uses the definitions and quantifiers printed in the
paper. It is exact rational arithmetic, not a comparison between linear and
quadratic feature learners.

## Source contract

- Paper: *Efficiently Learning Drifting Halfspaces with Massart Noise*,
  arXiv `2606.11149v1`.
- Theorem 4.1, anchor `#S4.Thmtheorem1`.
- Retrieved HTML SHA-256:
  `6b04e5b5b624ce99606d018a6dcfd2278d1448b36e555b0b7ce41c95105e1240`.
- Domain: the trajectory test of Definition 4.1 instantiated by Definition
  4.3.
- Claimed conclusion: no polynomial of degree below
  \(O(\gamma^{-c/4})\) is a 1-distinguisher.

## Assumptions and quantifiers

The source assumptions are recorded verbatim:

> Definition 4.3 is a valid instance of Definition 4.1

> gamma = Theta(1/d), d odd, and gamma < 1/log(1/Delta)

The theorem quantifies:

> for fixed c in (0,1/2)

> for eta = 1/3 and Delta > 2^(-1/gamma^c)

> no polynomial below the stated degree is a 1-distinguisher

## Decisive evidence shown inline

Definition 4.1 specifies the null label probability
`definition_4_1_null_p_y_plus` as
\[
\Pr_0(Y=+1)=\eta=\frac13.
\]
Definition 4.3 instead specifies
`definition_4_3_null_p_y_plus` as
\[
\Pr_1(Y=+1)=1-\eta=\frac23
\]
under both its stated null and its alternatives.

Take the degree-one polynomial
\[
\texttt{p(z)=\sum_{i=1}^{T} y_i}
\]
and the allowed trajectory length `T=2`. Exact moments are
\[
\mathbb E_0p=-\frac23,\qquad
\mathbb E_1p=\frac23,\qquad
\mathbb E_1p-\mathbb E_0p=\frac43,
\]
while
\[
\operatorname{Var}_0(p)=\frac{16}{9}.
\]
Therefore the `standardized_gap_squared` is
\[
\frac{(4/3)^2}{16/9}=1.
\]
So \(p\) is already a degree-one 1-distinguisher, and the same calculation
works for every \(T\geq2\).

The alternative can simultaneously meet the displayed late-step label
probabilities: choose ground-truth negative mass \(q_j=1/10\) and conditional
flip rate \(r_j=7/24\). Then its label probabilities are exactly
\(\Pr(Y=-1)=1/3\) and \(\Pr(Y=+1)=2/3\). The contradiction is therefore within
the theorem's stated instance rather than a nearby proxy.

## Independent checker

`INDEPENDENT CHECK: OK`

The checker uses `fractions.Fraction` to recompute both null probabilities,
the alternative probabilities, expectations, variance, standardized gap,
degree, and the \(T\geq2\) quantifier. It also confirms that degree one lies
below the claimed diverging threshold in the stated asymptotic regime.

## Negative control

The mutant changes Definition 4.1's null probability from \(1/3\) to \(2/3\).
That removes the exact expectation gap, so the claimed counterexample must
fail:

```text
CLAIM5_OBSERVED_EXIT=1
```

## Limitations

This falsifies Theorem 4.1 **as written**, because Definitions 4.1 and 4.3
assign incompatible null distributions. It does not show that a corrected
low-degree conjecture or a corrected hard instance is false, and it does not
by itself falsify the separate conditional learning-hardness Claim 2.

## Verdict

**FALSIFIED.** Under the printed assumptions, a degree-one polynomial is an
exact 1-distinguisher, contradicting the asserted exclusion of all
low-degree distinguishers.
