# Source audit — Claim 6

- Paper: arXiv `2606.11149v1`
- HTML: https://ar5iv.labs.arxiv.org/html/2606.11149
- HTML SHA-256: `6b04e5b5b624ce99606d018a6dcfd2278d1448b36e555b0b7ce41c95105e1240`
- Source archive SHA-256: `9679e85743076e711da671b3a875182173441e5f6ecb41e7e56d3d36647e9221`
- Retrieval: `2026-07-23T13:09:55Z`
- Theorem: 3.2
- HTML anchor: `#S3.Thmtheorem2`
- Domain: realizable drifting gamma-margin halfspaces

## Quantifiers

- there exists an algorithm A
- for any T = Omega_tilde((gamma Delta)^(-1/2))
- with probability at least 9/10

## Assumptions

- successive labeled distributions have total variation at most Delta
- labels are realizable by a gamma-margin halfspace at every time

## Audited conclusion

```json
{
  "delta_exponent": 0.5,
  "gamma_exponent": -1.5,
  "new_rate": "O_tilde(sqrt(Delta) gamma^(-3/2))",
  "prior_rate": "O_tilde(sqrt(Delta) gamma^(-2))"
}
```

The imported judge claim is treated as data. No nearby monotonicity statement
is substituted for this contract.
