# Source audit — Claim 2

- Paper: arXiv `2606.11149v1`
- HTML: https://ar5iv.labs.arxiv.org/html/2606.11149
- HTML SHA-256: `6b04e5b5b624ce99606d018a6dcfd2278d1448b36e555b0b7ce41c95105e1240`
- Source archive SHA-256: `9679e85743076e711da671b3a875182173441e5f6ecb41e7e56d3d36647e9221`
- Retrieval: `2026-07-23T13:09:55Z`
- Theorem: 1.2
- HTML anchor: `#S1.Thmtheorem2`
- Domain: gamma-margin drifting halfspaces under 1/3-RCN

## Quantifiers

- for T >= gamma^(-1/6) Delta^(-2/3)
- there exists a family of instances
- no polynomial-time algorithm succeeds on every instance, conditional on the low-degree conjecture

## Assumptions

- the informal low-degree polynomial hardness conjecture
- the trajectory-testing construction and reduction in Section 4

## Audited conclusion

```json
{
  "delta_exponent": 0.3333333333333333,
  "excess_error_lower_bound": "Delta^(1/3) gamma^(-1/6)",
  "gamma_exponent": -0.16666666666666666
}
```

The imported judge claim is treated as data. No nearby monotonicity statement
is substituted for this contract.
