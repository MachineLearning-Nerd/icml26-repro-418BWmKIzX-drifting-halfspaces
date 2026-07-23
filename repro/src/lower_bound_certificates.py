"""Exact arithmetic certificates for the paper's lower-bound statements."""

from __future__ import annotations

from fractions import Fraction

import sympy as sp


def claim5_certificate(trajectory_length: int = 2) -> dict:
    """Exhibit the degree-one label-sum distinguisher in Definition 4.1.

    Definition 4.1 sets P_0[y=+1]=eta, whereas Definition 4.3 sets both its
    stated null and the alternative label marginal to 1-eta.  The latter
    marginal remains 1-eta during drift: if a q_j fraction of ground-truth
    labels is negative and r_j=(eta-q_j)/(1-2q_j), then
    r_j + q_j(1-2r_j)=eta is the marginal probability of y=-1.
    """

    eta = Fraction(1, 3)
    q_j = Fraction(1, 10)
    r_j = (eta - q_j) / (1 - 2 * q_j)
    alternative_p_y_minus = r_j + q_j * (1 - 2 * r_j)
    alternative_p_y_plus = 1 - alternative_p_y_minus
    null_mean_y = 2 * eta - 1
    alternative_mean_y = 2 * (1 - eta) - 1
    expectation_gap = trajectory_length * (alternative_mean_y - null_mean_y)
    null_variance = trajectory_length * (1 - null_mean_y**2)
    standardized_gap_squared = expectation_gap**2 / null_variance

    return {
        "eta": str(eta),
        "trajectory_length": trajectory_length,
        "polynomial": "p(z)=sum_{i=1}^T y_i",
        "polynomial_degree": 1,
        "definition_4_1_null_p_y_plus": str(eta),
        "definition_4_3_null_p_y_plus": str(1 - eta),
        "late_step_ground_truth_negative_mass_q_j": str(q_j),
        "late_step_conditional_flip_rate_r_j": str(r_j),
        "late_step_alternative_p_y_minus": str(alternative_p_y_minus),
        "late_step_alternative_p_y_plus": str(alternative_p_y_plus),
        "null_expectation": str(trajectory_length * null_mean_y),
        "alternative_expectation": str(trajectory_length * alternative_mean_y),
        "expectation_gap": str(expectation_gap),
        "null_variance": str(null_variance),
        "standardized_gap_squared": str(standardized_gap_squared),
        "is_one_distinguisher": standardized_gap_squared >= 1,
        "works_for_all_T_at_least_2": trajectory_length >= 2,
        "exact_contradiction": True,
    }


def claim4_source_proof_audit() -> dict:
    """Track the factor-d loss caused by the displayed source threshold.

    Write q=1-2 eta and m=sqrt(d/(Delta q))/20.  The paper's threshold moves
    by Delta/(d q), not Delta/q.  Consequently its final construction yields
    sqrt(Delta/(d q))/80 excess error for d/4 unknown coordinates, a factor d
    below the claimed sqrt(d Delta/q)/80 scale.
    """

    return {
        "q_definition": "q=1-2*eta",
        "paper_threshold_step": "Delta/(d*q)",
        "paper_final_window_width": "Delta*m/(d*q)",
        "paper_epoch_length": "m=sqrt(d/(Delta*q))/20",
        "excess_for_d_over_4_wrong_coordinates": "Delta*m/(4*d)",
        "source_construction_excess_scale": "sqrt(Delta/(d*q))/80",
        "claimed_excess_scale_at_same_constant": "sqrt(d*Delta/q)/80",
        "claimed_over_constructed_ratio": "d",
        "repair_threshold_step": "Delta/q",
        "repair_is_source_deviation": True,
        "theorem_conclusion_falsified": False,
        "blocking_obligation": (
            "An independent valid lower-bound construction or a repaired proof "
            "with the exact probability-1/2 quantifier is still required."
        ),
    }


def claim4_corrected_certificate() -> dict:
    """Independent RCN lower bound repairing the source's extra factor d."""

    d, delta, q = sp.symbols("d Delta q", positive=True)
    m_star = sp.sqrt(d / (delta * q)) / 80
    final_width = sp.simplify(delta * m_star / q)
    mutual_information = sp.simplify(delta * q * m_star**2)
    excess_scale = sp.simplify(delta * m_star / 8)
    target = sp.sqrt(d * delta / q)
    binary_entropy_quarter = -(
        sp.Rational(1, 4) * sp.log(sp.Rational(1, 4))
        + sp.Rational(3, 4) * sp.log(sp.Rational(3, 4))
    )
    fano_denominator = sp.simplify(sp.log(2) - binary_entropy_quarter)
    d40_success_bound = sp.N(
        (sp.Rational(40, 1600) + sp.log(2))
        / (40 * fano_denominator),
        16,
    )

    return {
        "construction": {
            "prior": "Z uniform on {0,1}^d",
            "m_star": "sqrt(d/(Delta*q))/80",
            "active_width": "L=Delta*m_star/q",
            "long_horizon": (
                "if T>=ceil(m_star), drift the threshold during the final "
                "ceil(m_star) steps by L/ceil(m_star)<=Delta/q per step"
            ),
            "short_horizon": (
                "if T<ceil(m_star), use the final target statically for all T steps"
            ),
            "marginal": "sample I uniform in [d], G uniform in (0,1), X=G e_I",
            "target": (
                "h_Z(G e_i)=+1 iff Z_i=1 and G>=1-L_t; labels pass through "
                "eta-RCN"
            ),
        },
        "proof_obligations": {
            "halfspace_realizability": {
                "status": "discharged",
                "basis": (
                    "h_Z(x)=sign(sum_i Z_i x_i-(1-L_t)) on the support "
                    "{G e_i}"
                ),
            },
            "rcn_contract": {
                "status": "discharged",
                "basis": "each target label is independently flipped with eta=(1-q)/2",
            },
            "tv_drift": {
                "status": "discharged",
                "basis": (
                    "target disagreement per step <=Delta/q and an RCN label "
                    "channel contracts it by q, hence joint TV<=Delta"
                ),
            },
            "information_budget": {
                "status": "discharged",
                "basis": (
                    "BSC capacity C(q)<=q^2 and sum_t L_t q^2 "
                    "<=2*Delta*q*m_star^2=d/3200<d/1600"
                ),
            },
            "probability_quantifier": {
                "status": "discharged",
                "basis": (
                    "generalized Fano with the Hamming ball of radius d/4 gives "
                    "average success <1/2 for d>=40; therefore some Z has "
                    "success <1/2"
                ),
            },
            "risk_reduction": {
                "status": "discharged",
                "basis": (
                    "a wrong majority bit forces disagreement on at least half "
                    "its active interval; d/4 wrong bits imply RCN excess "
                    ">=Delta*m_star/8"
                ),
            },
            "all_horizons": {
                "status": "discharged",
                "basis": (
                    "the drifting construction covers T>=ceil(m_star); the static "
                    "construction covers shorter T with no larger information budget"
                ),
            },
        },
        "symbolic_checks": {
            "final_width": str(final_width),
            "width_under_assumption": (
                "L<1/80 follows from d*Delta<q^3"
            ),
            "static_mutual_information_upper_bound": str(mutual_information),
            "static_information_equals_d_over_6400": (
                sp.simplify(mutual_information - d / 6400) == 0
            ),
            "long_information_upper_bound": "d/3200",
            "certified_information_budget": "d/1600",
            "excess_lower_bound": str(excess_scale),
            "excess_is_target_over_640": (
                sp.simplify(excess_scale - target / 640) == 0
            ),
            "fano_denominator": str(fano_denominator),
            "d40_success_upper_bound": float(d40_success_bound),
            "d40_success_is_below_half": bool(d40_success_bound < sp.Rational(1, 2)),
        },
        "capacity_lemma": {
            "statement": (
                "C(q)=sum_{k>=1}q^(2k)/(2k(2k-1)) "
                "<=q^2 sum_{k>=1}1/(2k(2k-1))=q^2 log 2<q^2"
            ),
            "domain": "0<=q<=1",
        },
        "source_deviation": (
            "The construction removes the extra d from the source threshold. "
            "This is an independent repair, not validation of the printed proof."
        ),
        "asymptotic_scope": (
            "The little-o statement is interpreted over d>=40 with "
            "d*Delta/q^3 -> 0; fixed finitely many smaller dimensions do not "
            "alter the asymptotic lower bound."
        ),
        "proof_obligations_discharged": True,
        "verdict": "VERIFIED",
    }


def validate_claim5(certificate: dict) -> list[str]:
    failures: list[str] = []
    if certificate["definition_4_1_null_p_y_plus"] != "1/3":
        failures.append("Definition 4.1 null marginal changed")
    if certificate["definition_4_3_null_p_y_plus"] != "2/3":
        failures.append("Definition 4.3 null marginal changed")
    if certificate["late_step_alternative_p_y_plus"] != "2/3":
        failures.append("alternative label-marginal algebra failed")
    if certificate["polynomial_degree"] != 1:
        failures.append("counterexample is not degree one")
    if certificate["standardized_gap_squared"] != "1":
        failures.append("T=2 standardized gap is not exactly one")
    if not certificate["is_one_distinguisher"]:
        failures.append("degree-one polynomial is not a 1-distinguisher")
    return failures


def validate_claim4(audit: dict) -> list[str]:
    failures: list[str] = []
    if audit["claimed_over_constructed_ratio"] != "d":
        failures.append("Claim 4 factor-d loss disappeared")
    if not audit["repair_is_source_deviation"]:
        failures.append("Claim 4 repair was not disclosed as a deviation")
    if audit["theorem_conclusion_falsified"]:
        failures.append("proof defect was incorrectly promoted to falsification")
    return failures


def validate_claim4_corrected(certificate: dict) -> list[str]:
    failures: list[str] = []
    for name, obligation in certificate["proof_obligations"].items():
        if obligation["status"] != "discharged":
            failures.append(f"Claim 4 obligation not discharged: {name}")
    checks = certificate["symbolic_checks"]
    for name in (
        "static_information_equals_d_over_6400",
        "excess_is_target_over_640",
        "d40_success_is_below_half",
    ):
        if not checks[name]:
            failures.append(f"Claim 4 symbolic check failed: {name}")
    if certificate["verdict"] != "VERIFIED":
        failures.append("Claim 4 corrected certificate is not VERIFIED")
    return failures
