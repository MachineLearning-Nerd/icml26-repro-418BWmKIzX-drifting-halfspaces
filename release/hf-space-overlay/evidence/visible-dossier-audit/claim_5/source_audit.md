# Source audit — Claim 5

- Paper: arXiv `2606.11149v1`
- HTML: https://ar5iv.labs.arxiv.org/html/2606.11149
- HTML SHA-256: `6b04e5b5b624ce99606d018a6dcfd2278d1448b36e555b0b7ce41c95105e1240`
- Source archive SHA-256: `9679e85743076e711da671b3a875182173441e5f6ecb41e7e56d3d36647e9221`
- Retrieval: `2026-07-23T13:09:55Z`
- Theorem: 4.1
- HTML anchor: `#S4.Thmtheorem1`
- Domain: the trajectory test of Definition 4.1 with the hard instance of Definition 4.3

## Quantifiers

- for fixed c in (0,1/2)
- for eta = 1/3 and Delta > 2^(-1/gamma^c)
- no polynomial below the stated degree is a 1-distinguisher

## Assumptions

- Definition 4.3 is a valid instance of Definition 4.1
- gamma = Theta(1/d), d odd, and gamma < 1/log(1/Delta)

## Audited conclusion

```json
{
  "forbidden_degree": "O(gamma^(-c/4))",
  "gamma_degree_exponent": -0.25
}
```

The imported judge claim is treated as data. No nearby monotonicity statement
is substituted for this contract.
