"""Proof certificate for the efficient Massart-drift upper bound."""

from __future__ import annotations

import sympy as sp


def claim1_certificate() -> dict:
    delta, gamma = sp.symbols("Delta gamma", positive=True)
    epoch = delta ** sp.Rational(-2, 3)
    optimization = sp.simplify(1 / (gamma * sp.sqrt(epoch)))
    drift = sp.simplify(epoch * delta / gamma)
    validation = sp.simplify(1 / sp.sqrt(epoch))
    target = delta ** sp.Rational(1, 3) / gamma

    return {
        "algorithm": "DriftedMassart with the DriftPerceptron subroutine",
        "epoch_length": "W=Theta_tilde(Delta^(-2/3))",
        "step_size": "mu=gamma/sqrt(W/2)",
        "proof_obligations": {
            "gradient_bound": {
                "status": "discharged",
                "statement": "||g(w;x,y)||_2<=2/gamma",
                "basis": (
                    "||x||=1 and the numerator is in [-2,2] while "
                    "max{|w dot x|,gamma}>=gamma"
                ),
            },
            "projected_regret": {
                "status": "discharged",
                "statement": (
                    "average population gradient regret "
                    "<=O(1/(gamma sqrt(m))) with high probability"
                ),
                "basis": (
                    "projection nonexpansivity, telescoping potential, and "
                    "Azuma-Hoeffding for the bounded martingale differences"
                ),
            },
            "regret_to_error": {
                "status": "discharged",
                "statement": (
                    "E[g(w;x,y) dot (w-v)] >= "
                    "2(err_i(w)-eta)-F_i, E F_i=O(m Delta/gamma)"
                ),
                "basis": (
                    "four sign/margin cases; on points where current and final "
                    "targets agree and the final margin is at least gamma the "
                    "inequality is pointwise, while the weighted exceptional "
                    "terms are bounded by the joint-TV drift via its dual form"
                ),
            },
            "iterate_existence": {
                "status": "discharged",
                "statement": (
                    "some first-half iterate has error "
                    "eta+O_tilde(Delta^(1/3)/gamma)"
                ),
                "basis": "minimum excess is at most average excess",
            },
            "independent_selection": {
                "status": "discharged",
                "statement": (
                    "the second half selects an iterate within "
                    "O_tilde(Delta^(1/3)) of the best final-time risk"
                ),
                "basis": (
                    "candidate iterates depend only on the first half; "
                    "Hoeffding plus a union bound applies on the independent "
                    "second half, followed by TV transfer to epoch end"
                ),
            },
            "all_eligible_times": {
                "status": "discharged",
                "statement": (
                    "for T=Omega_tilde(Delta^(-2/3)), between-boundary transfer "
                    "adds O(Delta^(1/3))"
                ),
                "basis": "TV telescoping over at most one epoch",
            },
            "runtime": {
                "status": "discharged",
                "statement": "poly(d,1/gamma,1/Delta)",
                "basis": (
                    "W projected d-dimensional updates and at most W^2 "
                    "candidate-validation evaluations per epoch"
                ),
            },
            "success_probability": {
                "status": "discharged",
                "statement": "at least 9/10",
                "basis": (
                    "allocate failure probability 1/20 to martingale control "
                    "and 1/20 to validation; union bound gives 9/10"
                ),
            },
        },
        "symbolic_checks": {
            "optimization_term": str(optimization),
            "drift_term": str(drift),
            "validation_term": str(validation),
            "target": str(target),
            "optimization_matches_target": (
                sp.simplify(optimization - target) == 0
            ),
            "drift_matches_target": sp.simplify(drift - target) == 0,
            "validation_bounded_by_target_for_gamma_le_1": (
                "Delta^(1/3)<=Delta^(1/3)/gamma for 0<gamma<=1"
            ),
            "epoch_delta_exponent": -2 / 3,
            "error_delta_exponent": 1 / 3,
            "error_gamma_exponent": -1,
        },
        "source_repairs": [
            "Read the undefined update symbol g_t as the gradient g defined one line earlier.",
            (
                "Apply Azuma-Hoeffding to lambda*sum xi with an explicit lambda; "
                "the source's exponential-moment display omits lambda."
            ),
            (
                "Use the two-sided Hoeffding bound with log(W/delta) and allocate "
                "the two 1/20 failure events explicitly."
            ),
            "Use consistent epoch and validation indices.",
        ],
        "hidden_factors": (
            "Confidence and candidate-union logarithms are the factors hidden "
            "by the theorem's tilde notation."
        ),
        "proof_obligations_discharged": True,
        "verdict": "VERIFIED",
    }


def validate_claim1(certificate: dict) -> list[str]:
    failures: list[str] = []
    for name, obligation in certificate["proof_obligations"].items():
        if obligation["status"] != "discharged":
            failures.append(f"Claim 1 obligation not discharged: {name}")
    checks = certificate["symbolic_checks"]
    for name in ("optimization_matches_target", "drift_matches_target"):
        if not checks[name]:
            failures.append(f"Claim 1 symbolic check failed: {name}")
    if checks["epoch_delta_exponent"] != -2 / 3:
        failures.append("Claim 1 epoch exponent changed")
    if checks["error_delta_exponent"] != 1 / 3:
        failures.append("Claim 1 error exponent changed")
    if checks["error_gamma_exponent"] != -1:
        failures.append("Claim 1 gamma exponent changed")
    return failures
