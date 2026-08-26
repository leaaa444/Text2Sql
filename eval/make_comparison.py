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

PATH_8B = "eval/results_ablation_8b.json"
PATH_4O = "eval/results_ablation.json"


def load_ex(path):
    with open(path, encoding="utf-8") as f:
        rows = json.load(f)
    return {r["config"]: 100 * r["ex_ok"] / r["ex_n"] for r in rows if "ex_n" in r}


def main():
    ex_8b = load_ex(PATH_8B)
    ex_4o = load_ex(PATH_4O)
    labels = CONFIGS
    a = [ex_8b[c] for c in labels]
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
