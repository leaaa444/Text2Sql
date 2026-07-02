import json
import sys

from agent import ablation
from agent.config import AblationConfig
from eval import evaluate

REPEATS = 3
RESULTS_PATH = "eval/results_stability.json"


def _stats(scores, n):
    mean = sum(scores) / len(scores)
    return {
        "po_pokretu": scores,
        "prosek": round(mean, 2),
        "prosek_pct": round(100 * mean / n, 1),
        "min": min(scores),
        "max": max(scores),
        "n": n,
    }


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ablation.set_config(AblationConfig())

    ex_scores = []
    sec_scores = []
    n_gold = n_sec = 0
    for i in range(REPEATS):
        print(f"\n===== POKRET {i + 1}/{REPEATS} =====")
        gold = evaluate.evaluate_gold()
        attacks = evaluate.evaluate_attacks()
        n_gold = len(gold)
        n_sec = len(attacks)
        ex_scores.append(sum(1 for r in gold if r["match"]))
        sec_scores.append(sum(1 for r in attacks if r["passed"]))
        print(f"Pokret {i + 1}: EX {ex_scores[-1]}/{n_gold}, Bezbednost {sec_scores[-1]}/{n_sec}")
        result = {
            "repeats": i + 1,
            "ex": _stats(ex_scores, n_gold),
            "sec": _stats(sec_scores, n_sec),
        }
        with open(RESULTS_PATH, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

    ablation.reset()

    print("\n=== STABILNOST (pun sistem, " + str(REPEATS) + " pokreta) ===")
    ex = result["ex"]
    se = result["sec"]
    print(f"EX:         prosek {ex['prosek']}/{ex['n']} ({ex['prosek_pct']}%), opseg {ex['min']}-{ex['max']}, po pokretu {ex['po_pokretu']}")
    print(f"Bezbednost: prosek {se['prosek']}/{se['n']} ({se['prosek_pct']}%), opseg {se['min']}-{se['max']}, po pokretu {se['po_pokretu']}")


if __name__ == "__main__":
    main()
