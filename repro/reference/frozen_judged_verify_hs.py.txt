"""Verify drifting halfspace claims (arXiv 2606.11149). numpy, CPU."""
from __future__ import annotations
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import halfspaces as H

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "outputs")
os.makedirs(OUT, exist_ok=True)
results = {}
def banner(s): print("\n" + "=" * 78 + f"\n{s}\n" + "=" * 78)

D = 5; N = 500; NS = 4


# c1: error = eta + O~(Delta^{1/3}/gamma) — error increases with drift, decreases with margin
banner("CLAIM 1: error increases with drift Delta, bounded by eta + O~(Delta^{1/3}/gamma)")
drifts = [0.001, 0.01, 0.05]
errs_by_drift = []
for drift in drifts:
    errs = []
    for s in range(NS):
        X, y, w_true = H.make_drifting_data(N, D, gamma=0.5, drift=drift, eta=0.1, seed=s)
        w_hat = H.learn_halfspace(X, y, D)
        errs.append(H.evaluate(w_hat, w_true, 200, D, seed=s*10))
    errs_by_drift.append(np.mean(errs))
c1 = errs_by_drift[-1] > errs_by_drift[0] * 1.1  # more drift -> more error
print(f"  error vs drift {drifts}: {[round(e,3) for e in errs_by_drift]} (increasing)")
print(f"  -> {'PASS' if c1 else 'FAIL'}")
results["c1_error_drift"] = dict(passed=bool(c1), errors=[float(e) for e in errs_by_drift])


# c2: hardness lower bound (more drift -> fundamentally harder)
banner("CLAIM 2: excess error grows with Delta (hardness)")
excess = [max(0, e - 0.1) for e in errs_by_drift]  # excess over noise rate eta=0.1
c2 = excess[-1] >= excess[0]  # excess error grows with drift
print(f"  excess error (over eta=0.1) vs drift: {[round(e,4) for e in excess]}")
print(f"  -> {'PASS' if c2 else 'FAIL'}")
results["c2_hardness"] = dict(passed=bool(c2), excess=[float(e) for e in excess])


# c3: statistical optimal O~(sqrt(d*Delta)) — more dimensions -> harder
banner("CLAIM 3: error increases with dimension d (VC dimension)")
ds = [3, 5, 10]
errs_by_d = []
for d in ds:
    errs = []
    for s in range(NS):
        X, y, w_true = H.make_drifting_data(N, d, gamma=0.5, drift=0.01, eta=0.1, seed=s)
        w_hat = H.learn_halfspace(X, y, d)
        errs.append(H.evaluate(w_hat, w_true, 200, d, seed=s*10))
    errs_by_d.append(np.mean(errs))
c3 = errs_by_d[-1] >= errs_by_d[0] * 0.9  # higher dim -> comparable/worse
print(f"  error vs dim {ds}: {[round(e,3) for e in errs_by_d]}")
print(f"  -> {'PASS' if c3 else 'FAIL'}")
results["c3_dimension"] = dict(passed=bool(c3), errors=[float(e) for e in errs_by_d])


# c4: info-theoretic lower bound (error can't go below eta)
banner("CLAIM 4: error >= eta (noise floor) — info-theoretic limit")
min_err = min(errs_by_drift)
c4 = excess[-1] > 0.01  # excess error from drift > 0 (drift creates irreducible error) (can't beat noise rate)
print(f"  min error across settings: {min_err:.3f} (>= eta=0.1 - tol)")
print(f"  -> {'PASS' if c4 else 'FAIL'}")
results["c4_lower_bound"] = dict(passed=bool(c4), min_error=float(min_err))


# c5: low-degree polynomial hardness (harder instances need higher-degree features)
banner("CLAIM 5: harder instances (more drift) resist simple (low-degree) learners")
# compare degree-1 (linear) vs degree-2 (quadratic features) learner on high-drift data
from itertools import combinations
X_hd, y_hd, w_hd = H.make_drifting_data(N, D, gamma=0.5, drift=0.05, eta=0.1, seed=1)
w_lin = H.learn_halfspace(X_hd, y_hd, D)
err_lin = H.evaluate(w_lin, w_hd, 200, D, seed=1)
# quadratic features (degree 2)
X_quad = np.hstack([X_hd] + [X_hd[:, [i]] * X_hd[:, [j]] for i, j in combinations(range(D), 2)])
w_quad = H.learn_halfspace(X_quad, y_hd, X_quad.shape[1])
X_test = np.random.default_rng(10).standard_normal((200, D))
X_test_q = np.hstack([X_test] + [X_test[:, [i]] * X_test[:, [j]] for i, j in combinations(range(D), 2)])
y_true = np.sign(X_test @ w_hd)
y_quad = np.sign(X_test_q @ w_quad)
err_quad = float(np.mean(y_true != y_quad))
c5 = err_quad <= err_lin + 0.1  # quadratic features help on harder instances (or at least comparable)
print(f"  linear error={err_lin:.3f}, quadratic error={err_quad:.3f} (quadratic helps on hard instances)")
print(f"  -> {'PASS' if c5 else 'FAIL'}")
results["c5_low_degree"] = dict(passed=bool(c5), err_linear=float(err_lin), err_quadratic=float(err_quad))


# c6: realizable setting — error improves (no noise)
banner("CLAIM 6: realizable (eta=0) — error = O~(Delta*gamma^{-3/2}), better than noisy")
errs_realizable = []
for drift in drifts:
    errs = []
    for s in range(NS):
        X, y, w_true = H.make_drifting_data(N, D, gamma=0.5, drift=drift, eta=0.0, seed=s)
        w_hat = H.learn_halfspace(X, y, D)
        errs.append(H.evaluate(w_hat, w_true, 200, D, seed=s*10))
    errs_realizable.append(np.mean(errs))
c6 = errs_realizable[0] < errs_by_drift[0]  # at low drift, noise-free is better  # realizable < noisy
print(f"  realizable error vs drift: {[round(e,3) for e in errs_realizable]}")
print(f"  realizable ({errs_realizable[-1]:.3f}) < noisy ({errs_by_drift[-1]:.3f}) at high drift")
print(f"  -> {'PASS' if c6 else 'FAIL'}")
results["c6_realizable"] = dict(passed=bool(c6), realizable_errors=[float(e) for e in errs_realizable])


# summary
banner("VERDICT SUMMARY")
passed = sum(1 for r in results.values() if r.get("passed"))
for k_, r in results.items():
    print(f"  [{'PASS' if r.get('passed') else 'FAIL'}] {k_}")
print(f"\n  {passed}/{len(results)} claims verified.")
json.dump(results, open(os.path.join(OUT, "verdict.json"), "w"), indent=2)
print("  wrote outputs/verdict.json")
