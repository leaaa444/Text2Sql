import json

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

TEAL = "#0d9488"
SLATE = "#94a3b8"

CONFIGS = [
    "Pun sistem", "bez Retriever", "bez Selector", "bez Planner",
    "bez Integrator", "bez Reflector", "bez Recorder", "bez Skill-build", "bez svega",
]

# 8b (llama-3.1-8b-instant) EX u procentima
EX_8B = {
    "Pun sistem": 70.8, "bez Retriever": 75.0, "bez Selector": 70.8, "bez Planner": 58.3,
    "bez Integrator": 83.3, "bez Reflector": 79.2, "bez Recorder": 79.2,
    "bez Skill-build": 83.3, "bez svega": 8.3,
}


def load_4o():
    with open("eval/results_ablation.json", encoding="utf-8") as f:
        rows = json.load(f)
    out = {}
    for r in rows:
        if "ex_n" in r:
            out[r["config"]] = 100 * r["ex_ok"] / r["ex_n"]
    return out


def main():
    ex_4o = load_4o()
    labels = CONFIGS
    a = [EX_8B[c] for c in labels]
    b = [ex_4o.get(c, 0) for c in labels]

    x = np.arange(len(labels))
    w = 0.4
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(x - w / 2, a, w, label="llama-3.1-8b (slabiji model)", color=SLATE, edgecolor="white")
    ax.bar(x + w / 2, b, w, label="gpt-4o-mini (jaci model)", color=TEAL, edgecolor="white")

    for i, (va, vb) in enumerate(zip(a, b)):
        ax.text(i - w / 2, va + 1.5, f"{va:.0f}", ha="center", fontsize=8.5)
        ax.text(i + w / 2, vb + 1.5, f"{vb:.0f}", ha="center", fontsize=8.5, fontweight="bold")

    ax.set_ylim(0, 108)
    ax.set_ylabel("EX (%)")
    ax.set_title("Poređenje modela — tačnost (EX) po konfiguraciji ablacione studije",
                 fontsize=13, fontweight="bold", pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=25, ha="right", fontsize=9.5)
    ax.legend(loc="lower left", fontsize=10)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    fig.savefig("eval/chart_comparison.png", dpi=150)
    plt.close(fig)
    print("Snimljeno: eval/chart_comparison.png")


if __name__ == "__main__":
    main()
