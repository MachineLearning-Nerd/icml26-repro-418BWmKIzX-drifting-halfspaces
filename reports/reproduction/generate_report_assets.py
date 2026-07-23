"""Generate the evidence-bearing figures used by the reproduction report."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).with_name("images")
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams.update(
    {
        "figure.dpi": 160,
        "savefig.dpi": 180,
        "font.size": 10,
        "axes.titlesize": 12,
        "axes.labelsize": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
    }
)

NAVY = "#214761"
TEAL = "#25858A"
GOLD = "#D29B38"
RED = "#B64A4A"
GRAY = "#6D7780"
LIGHT = "#E7ECEF"


def save(fig: plt.Figure, name: str) -> None:
    fig.tight_layout()
    fig.savefig(OUT / name, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def verdicts() -> None:
    labels = ["1", "2", "3", "4", "5", "6"]
    verdict = ["VERIFIED", "BLOCKED", "VERIFIED", "VERIFIED", "FALSIFIED", "FALSIFIED"]
    colors = [TEAL, GRAY, TEAL, TEAL, RED, RED]
    fig, ax = plt.subplots(figsize=(10.5, 2.7))
    ax.barh([0] * 6, [0.86] * 6, left=np.arange(6), color=colors, height=0.58)
    for idx, (claim, result) in enumerate(zip(labels, verdict)):
        ax.text(idx + 0.43, 0.08, f"Claim {claim}", ha="center", va="center", color="white", weight="bold")
        ax.text(idx + 0.43, -0.13, result, ha="center", va="center", color="white", fontsize=8)
    ax.text(0, 0.63, "Five exact claims resolved; one conditional hardness claim remains blocked", color=NAVY, fontsize=13, weight="bold")
    ax.text(0, 0.45, "No toy trend is counted as theorem evidence", color=GRAY)
    ax.set_xlim(-0.05, 6)
    ax.set_ylim(-0.55, 0.85)
    ax.axis("off")
    save(fig, "headline-verdicts.png")


def rate_balancing() -> None:
    ratio = np.logspace(-2, 2, 400)
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.0), sharey=True)
    panels = [
        (
            axes[0],
            ratio ** -0.5,
            ratio,
            "Claim 1: efficient Massart learner",
            r"$W/W_\star$,  $W_\star=\Delta^{-2/3}$",
        ),
        (
            axes[1],
            ratio ** -1,
            ratio,
            "Claim 3: information-theoretic ERM",
            r"$W/W_\star$,  $W_\star=\sqrt{d/(q\Delta)}$",
        ),
    ]
    for ax, estimation, drift, title, xlabel in panels:
        ax.loglog(ratio, estimation, color=NAVY, label="estimation / optimization")
        ax.loglog(ratio, drift, color=GOLD, label="drift")
        ax.loglog(ratio, estimation + drift, color=TEAL, linewidth=2.2, label="combined")
        ax.axvline(1, color=GRAY, linestyle="--", linewidth=1)
        ax.scatter([1], [2], color=TEAL, zorder=3)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.grid(True, which="both", color=LIGHT, linewidth=0.6)
    axes[0].set_ylabel("term relative to its value at the balance point")
    axes[0].legend(frameon=False, loc="lower left")
    save(fig, "rate-balancing.png")


def claim5_distinguisher() -> None:
    t = np.arange(1, 26)
    standardized_gap = np.sqrt(t / 2)
    fig, ax = plt.subplots(figsize=(8.2, 4.2))
    ax.plot(t, standardized_gap, color=RED, linewidth=2.4, marker="o", markersize=3)
    ax.axhline(1, color=NAVY, linestyle="--", label="1-distinguisher threshold")
    ax.scatter([2], [1], color=GOLD, edgecolor=NAVY, zorder=4, s=70)
    ax.annotate(
        "degree-1 test reaches the forbidden threshold at T=2",
        xy=(2, 1),
        xytext=(6, 1.75),
        arrowprops={"arrowstyle": "->", "color": GRAY},
    )
    ax.set_xlabel("trajectory length T")
    ax.set_ylabel(r"standardized gap  $|E_0p-E_1p|/\sqrt{Var_0p}$")
    ax.set_title(r"Claim 5 contradiction:  $p(z)=\sum_i y_i$ has gap $\sqrt{T/2}$")
    ax.grid(True, color=LIGHT)
    ax.legend(frameon=False)
    save(fig, "claim5-degree-one.png")


def claim4_fano() -> None:
    d = np.arange(12, 201)
    entropy_quarter = -(0.25 * np.log(0.25) + 0.75 * np.log(0.75))
    denominator = np.log(2) - entropy_quarter
    success = (d / 1600 + np.log(2)) / (d * denominator)
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.0))
    ax = axes[0]
    ax.plot(d, success, color=TEAL, linewidth=2.3)
    ax.axhline(0.5, color=RED, linestyle="--", label="required < 1/2")
    ax.axvline(40, color=GRAY, linestyle=":")
    ax.scatter([40], [success[d.tolist().index(40)]], color=GOLD, edgecolor=NAVY, zorder=4)
    ax.set_xlabel("dimension d")
    ax.set_ylabel("generalized-Fano success upper bound")
    ax.set_title("Probability quantifier")
    ax.set_ylim(0, 0.65)
    ax.grid(True, color=LIGHT)
    ax.legend(frameon=False)

    ax = axes[1]
    labels = ["TV per step", "information", "excess risk"]
    values = [1.0, 1 / 1600, 1 / 640]
    annotations = [r"$\leq\Delta$", r"$\leq d/1600$", r"$\geq\sqrt{d\Delta/q}/640$"]
    bars = ax.bar(labels, values, color=[NAVY, GOLD, TEAL])
    ax.set_yscale("log")
    ax.set_ylim(3e-4, 2)
    ax.set_title("Certified constants (normalized)")
    ax.set_ylabel("normalized scale (log axis)")
    ax.grid(True, axis="y", which="both", color=LIGHT)
    for bar, annotation in zip(bars, annotations):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() * 1.25, annotation, ha="center", fontsize=9)
    save(fig, "claim4-fano-certificate.png")


def main() -> None:
    verdicts()
    rate_balancing()
    claim5_distinguisher()
    claim4_fano()


if __name__ == "__main__":
    main()
