"""Clean-room drifting halfspace learning from "Efficiently Learning Drifting Halfspaces with
Massart Noise" (arXiv 2606.11149). numpy, CPU. Halfspace y=sign(w*·x) with drift w* changes by
Delta per round; Massart noise flips labels with prob <= eta independently per sample.
c1: error = eta + O~(Delta^{1/3}/gamma); c6: realizable error O~(Delta*gamma^{-3/2}).
"""
from __future__ import annotations
import numpy as np


def make_drifting_data(n, d, gamma, drift, eta, seed=0):
    """Generate n samples with a drifting halfspace (margin gamma, drift Delta, Massart noise eta)."""
    rng = np.random.default_rng(seed)
    w = rng.standard_normal(d); w /= np.linalg.norm(w)
    X = []; y = []
    for i in range(n):
        # drift: w rotates slightly each round
        w_drift = w + drift * rng.standard_normal(d); w_drift /= np.linalg.norm(w_drift)
        w = w_drift
        x = rng.standard_normal(d)
        true_label = 1 if x @ w > 0 else -1
        margin = abs(x @ w)
        # Massart noise: flip with prob <= eta (independent of margin)
        if rng.random() < eta:
            label = -true_label
        else:
            label = true_label
        X.append(x); y.append(label)
    return np.array(X), np.array(y), w


def learn_halfspace(X, y, d, epochs=50, lr=0.01, lam=0.01):
    """Learn a halfspace via L2-regularized logistic regression (gradient descent)."""
    w = np.zeros(d)
    for _ in range(epochs):
        for i in range(len(X)):
            margin = y[i] * (X[i] @ w)
            if margin < 1:  # hinge-like loss gradient
                w += lr * (y[i] * X[i] - lam * w)
            else:
                w -= lr * lam * w
    return w / max(np.linalg.norm(w), 1e-9)


def evaluate(w_hat, w_true, n_test, d, seed=0):
    """Error rate of w_hat vs the true halfspace w_true on fresh test data."""
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((n_test, d))
    y_true = np.sign(X @ w_true)
    y_hat = np.sign(X @ w_hat)
    return float(np.mean(y_true != y_hat))
