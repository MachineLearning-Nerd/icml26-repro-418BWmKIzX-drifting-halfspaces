"""Exact arithmetic certificates for the paper's lower-bound statements."""

from __future__ import annotations

from fractions import Fraction


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
