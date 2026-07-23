"""Exact source contracts audited from arXiv:2606.11149v1."""

PAPER = {
    "paper_id": "2606.11149v1",
    "html_url": "https://ar5iv.labs.arxiv.org/html/2606.11149",
    "html_sha256": "6b04e5b5b624ce99606d018a6dcfd2278d1448b36e555b0b7ce41c95105e1240",
    "source_url": "https://export.arxiv.org/e-print/2606.11149",
    "source_sha256": "9679e85743076e711da671b3a875182173441e5f6ecb41e7e56d3d36647e9221",
    "retrieved_at_utc": "2026-07-23T13:09:55Z",
}

CONTRACTS = [
    {
        "claim_id": 1,
        "anchor": "S1.Thmtheorem1",
        "theorem": "1.1",
        "domain": "online learning of gamma-margin halfspaces under eta-Massart noise",
        "quantifiers": [
            "there exists an algorithm A",
            "for any T = Omega_tilde(Delta^(-2/3))",
            "with probability at least 9/10",
        ],
        "assumptions": [
            "successive labeled distributions have total variation at most Delta",
            "each target is a homogeneous halfspace on the unit sphere",
            "all examples have margin at least gamma",
            "conditional label-flip probability is at most eta < 1/2",
        ],
        "conclusion": {
            "runtime": "poly(d, 1/gamma, 1/Delta)",
            "error_upper_bound": "eta + O_tilde(Delta^(1/3)/gamma)",
            "delta_exponent": 1 / 3,
            "gamma_exponent": -1,
        },
        "required_evidence": "proof-obligation audit of Algorithms 1-2 and every theorem dependency",
        "verdict": "BLOCKED",
        "reason": "The exact source contract is established; the proof obligations are not yet independently discharged on this branch.",
    },
    {
        "claim_id": 2,
        "anchor": "S1.Thmtheorem2",
        "theorem": "1.2",
        "domain": "gamma-margin drifting halfspaces under 1/3-RCN",
        "quantifiers": [
            "for T >= gamma^(-1/6) Delta^(-2/3)",
            "there exists a family of instances",
            "no polynomial-time algorithm succeeds on every instance, conditional on the low-degree conjecture",
        ],
        "assumptions": [
            "the informal low-degree polynomial hardness conjecture",
            "the trajectory-testing construction and reduction in Section 4",
        ],
        "conclusion": {
            "excess_error_lower_bound": "Delta^(1/3) gamma^(-1/6)",
            "delta_exponent": 1 / 3,
            "gamma_exponent": -1 / 6,
        },
        "required_evidence": "valid Theorem 4.1 certificate plus a valid testing-to-learning reduction",
        "verdict": "BLOCKED",
        "reason": "Theorem 4.1's stated instance admits a degree-one distinguisher, so the paper's supplied hardness route is invalid. The conditional conclusion about all polynomial-time algorithms is not thereby logically falsified and remains blocked.",
    },
    {
        "claim_id": 3,
        "anchor": "S2.Thmtheorem1",
        "theorem": "2.1",
        "domain": "any binary concept class of VC dimension d under eta-Massart noise",
        "quantifiers": [
            "for every drifting sequence satisfying the assumptions",
            "there exists an information-theoretic algorithm A",
            "for every t = Omega_tilde(d/((1-2eta)Delta))",
            "with probability at least 9/10",
        ],
        "assumptions": [
            "successive labeled distributions have total variation at most Delta",
            "each distribution is realized by a member of the class with eta-Massart noise",
        ],
        "conclusion": {
            "error_upper_bound": "opt_t + O_tilde(sqrt(d Delta/(1-2eta)))",
            "delta_exponent": 1 / 2,
            "d_exponent": 1 / 2,
        },
        "required_evidence": "localized VC/ERM proof certificate, not a dimension monotonicity sweep",
        "verdict": "BLOCKED",
        "reason": "The exact theorem contract is established; its localized uniform-convergence argument is not yet independently discharged on this branch.",
    },
    {
        "claim_id": 4,
        "anchor": "S2.Thmtheorem2",
        "theorem": "2.2",
        "domain": "halfspaces under eta-random classification noise",
        "quantifiers": [
            "for every T > 0 and Delta in (0,1)",
            "there exists a family of instances",
            "no algorithm attains the stated little-o excess error with probability 1/2 on every instance",
        ],
        "assumptions": ["(1-2eta)^3 > d Delta"],
        "conclusion": {
            "forbidden_error": "opt_T + o(sqrt(d Delta/(1-2eta)))",
            "delta_exponent": 1 / 2,
            "d_exponent": 1 / 2,
        },
        "required_evidence": "information-theoretic lower-bound construction and testing reduction",
        "verdict": "BLOCKED",
        "reason": "The displayed threshold in the source proof loses a factor d and yields only sqrt(Delta/(d(1-2eta))) at its endpoint. A corrected construction may prove the theorem, but that repair is a source deviation and the probability quantifier remains to be discharged.",
    },
    {
        "claim_id": 5,
        "anchor": "S4.Thmtheorem1",
        "theorem": "4.1",
        "domain": "the trajectory test of Definition 4.1 with the hard instance of Definition 4.3",
        "quantifiers": [
            "for fixed c in (0,1/2)",
            "for eta = 1/3 and Delta > 2^(-1/gamma^c)",
            "no polynomial below the stated degree is a 1-distinguisher",
        ],
        "assumptions": [
            "Definition 4.3 is a valid instance of Definition 4.1",
            "gamma = Theta(1/d), d odd, and gamma < 1/log(1/Delta)",
        ],
        "conclusion": {
            "forbidden_degree": "O(gamma^(-c/4))",
            "gamma_degree_exponent": -1 / 4,
        },
        "required_evidence": "exact likelihood-ratio projection and correlation-bound certificate",
        "verdict": "FALSIFIED",
        "reason": "Definition 4.1 has null P(y=+1)=eta, while Definition 4.3 uses P(y=+1)=1-eta under both its stated null and alternatives. At eta=1/3, p(z)=sum_i y_i is already a degree-one 1-distinguisher for every T>=2.",
    },
    {
        "claim_id": 6,
        "anchor": "S3.Thmtheorem2",
        "theorem": "3.2",
        "domain": "realizable drifting gamma-margin halfspaces",
        "quantifiers": [
            "there exists an algorithm A",
            "for any T = Omega_tilde((gamma Delta)^(-1/2))",
            "with probability at least 9/10",
        ],
        "assumptions": [
            "successive labeled distributions have total variation at most Delta",
            "labels are realizable by a gamma-margin halfspace at every time",
        ],
        "imported_claim": {
            "new_rate": "O_tilde(Delta gamma^(-3/2))",
            "prior_rate": "O_tilde(Delta gamma^(-2))",
            "delta_exponent": 1,
        },
        "conclusion": {
            "new_rate": "O_tilde(sqrt(Delta) gamma^(-3/2))",
            "prior_rate": "O_tilde(sqrt(Delta) gamma^(-2))",
            "delta_exponent": 1 / 2,
            "gamma_exponent": -3 / 2,
        },
        "required_evidence": "source comparison is sufficient to falsify the imported transcription; the actual theorem is a separate contract",
        "verdict": "FALSIFIED",
        "reason": "The judged claim changes both Delta exponents from 1/2 to 1. The exact source theorem and comparison both contain sqrt(Delta).",
    },
]
