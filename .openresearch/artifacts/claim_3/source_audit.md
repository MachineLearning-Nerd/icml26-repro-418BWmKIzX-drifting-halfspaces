# Source audit — Claim 3

- Paper: arXiv `2606.11149v1`
- HTML: https://ar5iv.labs.arxiv.org/html/2606.11149
- HTML SHA-256: `6b04e5b5b624ce99606d018a6dcfd2278d1448b36e555b0b7ce41c95105e1240`
- Source archive SHA-256: `9679e85743076e711da671b3a875182173441e5f6ecb41e7e56d3d36647e9221`
- Retrieval: `2026-07-23T13:09:55Z`
- Theorem: 2.1
- HTML anchor: `#S2.Thmtheorem1`
- Domain: any binary concept class of VC dimension d under eta-Massart noise

## Quantifiers

- for every drifting sequence satisfying the assumptions
- there exists an information-theoretic algorithm A
- for every t = Omega_tilde(d/((1-2eta)Delta))
- with probability at least 9/10

## Assumptions

- successive labeled distributions have total variation at most Delta
- each distribution is realized by a member of the class with eta-Massart noise

## Audited conclusion

```json
{
  "d_exponent": 0.5,
  "delta_exponent": 0.5,
  "error_upper_bound": "opt_t + O_tilde(sqrt(d Delta/(1-2eta)))"
}
```

The imported judge claim is treated as data. No nearby monotonicity statement
is substituted for this contract.
