# Source audit — Claim 1

- Paper: arXiv `2606.11149v1`
- HTML: https://ar5iv.labs.arxiv.org/html/2606.11149
- HTML SHA-256: `6b04e5b5b624ce99606d018a6dcfd2278d1448b36e555b0b7ce41c95105e1240`
- Source archive SHA-256: `9679e85743076e711da671b3a875182173441e5f6ecb41e7e56d3d36647e9221`
- Retrieval: `2026-07-23T13:09:55Z`
- Theorem: 1.1
- HTML anchor: `#S1.Thmtheorem1`
- Domain: online learning of gamma-margin halfspaces under eta-Massart noise

## Quantifiers

- there exists an algorithm A
- for any T = Omega_tilde(Delta^(-2/3))
- with probability at least 9/10

## Assumptions

- successive labeled distributions have total variation at most Delta
- each target is a homogeneous halfspace on the unit sphere
- all examples have margin at least gamma
- conditional label-flip probability is at most eta < 1/2

## Audited conclusion

```json
{
  "delta_exponent": 0.3333333333333333,
  "error_upper_bound": "eta + O_tilde(Delta^(1/3)/gamma)",
  "gamma_exponent": -1,
  "runtime": "poly(d, 1/gamma, 1/Delta)"
}
```

The imported judge claim is treated as data. No nearby monotonicity statement
is substituted for this contract.
