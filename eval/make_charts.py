import json

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

RESULTS_PATH = "eval/results_ablation.json"
TEAL = "#0d9488"
RED = "#dc2626"
SLATE = "#94a3b8"


def _color(name):
    if name == "Pun sistem":
        return TEAL
    if name == "bez svega":
        return RED
    return SLATE


def _bar_chart(rows, ok_key, n_key, title, ylabel, path):
    data = [(r["config"], 100 * r[ok_key] / r[n_key]) for r in rows if n_key in r]
    labels = [d[0] for d in data]
    values = [d[1] for d in data]
    colors = [_color(name) for name in labels]

    fig, ax = plt.subplots(figsize=(8.5, 4.8))
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


if __name__ == "__main__":
    main()
