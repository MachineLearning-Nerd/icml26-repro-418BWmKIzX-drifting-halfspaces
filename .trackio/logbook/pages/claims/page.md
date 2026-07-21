# Claims


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_1ef2c266b83d", "created_at": "2026-07-21T23:57:10+00:00", "title": "Claims to reproduce"}
-->
## Claims to reproduce

1. The paper's polynomial-time algorithm learns margin-separable halfspaces under distribution drift with Massart noise achieving error eta + O~(Delta^{1/3}/gamma), where eta bounds the Massart noise rate, Delta is the drift rate, and gamma is the margin parameter (Theorem 1.1, Section 1.1).
2. Under the low-degree polynomial hardness conjecture, any efficient algorithm for this drifting halfspace problem must incur excess error Omega(Delta^{1/3}), matching the algorithm's guarantee and establishing an information-computation gap (Theorem 1.2, Section 1.1).
3. For general VC-dimension-d hypothesis classes under Massart noise, the statistically optimal (possibly inefficient) error rate is O~(sqrt(d*Delta)), better than the Theta((d*Delta)^{1/3}) rate achievable under adversarial noise (Theorem 2.1, Section 2).
4. A matching information-theoretic lower bound of Omega(sqrt(d*Delta)) is proved for halfspaces under random classification noise (RCN), establishing optimality at Theta~(sqrt(d*Delta)) (Theorem 2.2, Section 2).
5. Theorem 4.1 formally shows that no polynomial of degree less than O(gamma^{-c/4}) can distinguish the null from alternative hypothesis in the associated trajectory-testing problem, giving the formal low-degree hardness evidence for the Delta^{1/3} scaling (Theorem 4.1, Section 4).
6. In the realizable setting, the algorithm's error improves to O~(Delta*gamma^{-3/2}), surpassing the prior best known bound of O~(Delta*gamma^{-2}) (Theorem 3.2, Section 3).
