import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

RESULTS_PATH = "eval/results_ablation.json"
HARD_PATH = "eval/results_ablation_hard.json"
ADDITIVE_PATH = "eval/results_ablation_additive.json"
TEAL = "#0d9488"
RED = "#dc2626"
SLATE = "#94a3b8"


def _color(name):
    if name in ("Pun sistem", "samo Retriever"):
        return TEAL
    if name in ("bez svega", "Polazno resenje"):
        return RED
    return SLATE


def _bar_chart(rows, ok_key, n_key, title, ylabel, path, figsize=(8.5, 4.8)):
    data = [(r["config"], 100 * r[ok_key] / r[n_key]) for r in rows if n_key in r]
    labels = [d[0] for d in data]
    values = [d[1] for d in data]
    colors = [_color(name) for name in labels]

    fig, ax = plt.subplots(figsize=figsize)
    bars = ax.bar(labels, values, color=colors, edgecolor="white", linewidth=0.5)
    ax.set_ylim(0, 105)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_title(title, fontsize=13, fontweight="bold", pad=12)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.set_axisbelow(True)
    plt.setp(ax.get_xticklabels(), rotation=25, ha="right", fontsize=10)

    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 1.5,
            f"{value:.0f}%",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
        )

    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"Snimljeno: {path}")


def main():
    with open(RESULTS_PATH, encoding="utf-8") as f:
        rows = json.load(f)

    _bar_chart(
        rows,
        "ex_ok",
        "ex_n",
        "Tačnost (EX) po konfiguraciji — ablaciona studija",
        "EX (%)",
        "eval/chart_ex.png",
    )
    _bar_chart(
        rows,
        "sec_ok",
        "sec_n",
        "Bezbednost po konfiguraciji — ablaciona studija",
        "Blokirano / maskirano (%)",
        "eval/chart_security.png",
    )
    if os.path.exists(HARD_PATH):
        with open(HARD_PATH, encoding="utf-8") as f:
            hard = json.load(f)
        _bar_chart(
            hard,
            "ex_ok",
            "ex_n",
            "Tačnost (EX) na težim pitanjima — ablaciona studija",
            "EX (%)",
            "eval/chart_ex_hard.png",
            figsize=(9, 4.6),
        )
    if os.path.exists(ADDITIVE_PATH):
        with open(ADDITIVE_PATH, encoding="utf-8") as f:
            additive = json.load(f)
        _bar_chart(
            additive,
            "ex_ok",
            "ex_n",
            "Tačnost (EX) pri dodavanju po jednog paterna na polazno rešenje",
            "EX (%)",
            "eval/chart_ex_additive.png",
            figsize=(9.5, 4.8),
        )


if __name__ == "__main__":
    main()
