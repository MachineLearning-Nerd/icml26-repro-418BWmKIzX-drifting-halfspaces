# Claim 2 - Conditional efficient hardness

Verdict: **BLOCKED**

This page deliberately does not promote a monotonic toy trend or the Claim 5
counterexample into a universal computational lower bound.

## Source contract

- Paper: arXiv `2606.11149v1`
- Theorem 1.2, HTML anchor `#S1.Thmtheorem2`
- Source HTML SHA-256:
  `6b04e5b5b624ce99606d018a6dcfd2278d1448b36e555b0b7ce41c95105e1240`
- Conditional conclusion: no polynomial-time learner succeeds on every
  constructed instance below excess error
  \(\Delta^{1/3}\gamma^{-1/6}\), assuming the informal low-degree hardness
  conjecture and a valid Section 4 reduction.

## Assumptions and quantifiers

Assumptions:

- the informal low-degree polynomial hardness conjecture
- the trajectory-testing construction and reduction in Section 4

Quantifiers:

- for T >= gamma^(-1/6) Delta^(-2/3)
- there exists a family of instances
- no polynomial-time algorithm succeeds on every instance, conditional on the low-degree conjecture

## Decisive evidence shown inline

The supplied route has two obligations:

1. Theorem 4.1 must give a valid low-degree lower bound for the exact null and
   alternative distributions.
2. The testing-to-learning reduction must carry that lower bound to every
   polynomial-time learner in the theorem's parameter range.

Claim 5 shows that obligation 1 is not met as written: the Definition 4.1 null
has \(\Pr(y=+1)=1/3\), while the hard-instance null and alternatives have
\(\Pr(y=+1)=2/3\). The degree-one statistic
\(p=\sum_i y_i\) already distinguishes at \(T=2\).

That contradiction invalidates the paper's supplied proof route. It **does not
logically falsify** this conditional claim: falsification would require either
an efficient learner contradicting the quantified conclusion or a logical
contradiction under a corrected conjecture and reduction. Neither is present.

The exact unresolved machine obligation is:

```text
valid Theorem 4.1 certificate plus a valid testing-to-learning reduction
```

This is why the result remains BLOCKED rather than being mislabeled VERIFIED
or FALSIFIED.

## Independent checker

The independent program requires the source hash, theorem anchor, exact verdict
token, and a nonempty blocking obligation.

```text
INDEPENDENT CHECK: OK
All source hashes, theorem anchors, verdict tokens, Claim 1/3/4 proof algebra,
and exact Claim 5/6 contradictions agree.
```

Raw paths:
`evidence/exact-claim-audit/claim_2/claim_contract.json`,
`raw_results.json`, and `independent_checker_output.txt`.

## Negative control

The mutation deletes the named blocking obligation. A BLOCKED verdict without a
specific missing obligation must fail:

```text
CLAIM2_EXPECTED_NONZERO_EXIT=1
CLAIM2_OBSERVED_EXIT=1
INDEPENDENT CHECK: FAIL
- claim 2: BLOCKED without a named obligation
```

## Limitations

- No unconditional hardness result can verify a conjecture-conditional claim.
- Claim 5 attacks the supplied trajectory instance, not every possible
  low-degree construction.
- A corrected Theorem 4.1 and a re-audited testing-to-learning reduction are
  necessary before this status can change.
- The old empirical trend is irrelevant to the universal quantifier.

## Verdict

The exact missing obligation is visible and testable, but it is not discharged.
Verdict: **BLOCKED**.
