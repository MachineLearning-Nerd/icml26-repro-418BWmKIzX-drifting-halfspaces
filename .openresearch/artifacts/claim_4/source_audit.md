# Source audit — Claim 4

- Paper: arXiv `2606.11149v1`
- HTML: https://ar5iv.labs.arxiv.org/html/2606.11149
- HTML SHA-256: `6b04e5b5b624ce99606d018a6dcfd2278d1448b36e555b0b7ce41c95105e1240`
- Source archive SHA-256: `9679e85743076e711da671b3a875182173441e5f6ecb41e7e56d3d36647e9221`
- Retrieval: `2026-07-23T13:09:55Z`
- Theorem: 2.2
- HTML anchor: `#S2.Thmtheorem2`
- Domain: halfspaces under eta-random classification noise

## Quantifiers

- for every T > 0 and Delta in (0,1)
- there exists a family of instances
- no algorithm attains the stated little-o excess error with probability 1/2 on every instance

## Assumptions

- (1-2eta)^3 > d Delta

## Audited conclusion

```json
{
  "d_exponent": 0.5,
  "delta_exponent": 0.5,
  "forbidden_error": "opt_T + o(sqrt(d Delta/(1-2eta)))"
}
```

The imported judge claim is treated as data. No nearby monotonicity statement
is substituted for this contract.
