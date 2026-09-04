import json
import os
import sys

from agent import ablation, skills
from agent.config import AblationConfig
from eval import evaluate

evaluate.GOLD_PATH = os.getenv("GOLD_PATH", "eval/gold_hard.json")

CONFIGS = [
    ("Pun sistem", AblationConfig()),
    ("bez Retriever", AblationConfig(use_retriever=False)),
    ("bez Selector", AblationConfig(use_selector=False)),
    ("bez Planner", AblationConfig(use_planner=False)),
    ("bez Integrator", AblationConfig(use_integrator=False)),
    ("bez Reflector", AblationConfig(use_reflector=False)),
    ("bez Recorder", AblationConfig(use_recorder=False)),
    ("bez Skill-build", AblationConfig(use_skill_build=False)),
    ("bez svega", AblationConfig.baseline()),
]
OUT = "eval/results_ablation_hard.json"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    table = []
    done = set()
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as f:
            table = json.load(f)
        done = {r["config"] for r in table}

    for name, cfg in CONFIGS:
        if name in done:
            print("preskacem (vec uradjeno):", name)
            continue
        skills.reset()
        ablation.set_config(cfg)
        print(f"\n########## {name} ##########")
        gold = evaluate.evaluate_gold()
        row = {
            "config": name,
            "model": evaluate.model_name(),
            "ex_ok": sum(1 for r in gold if r["match"]),
            "ex_n": len(gold),
            "pitanja": gold,
        }
        table.append(row)
        with open(OUT, "w", encoding="utf-8") as f:
            json.dump(table, f, ensure_ascii=False, indent=2)
    ablation.reset()

    print("\n=== TEZA ABLACIJA (EX) ===")
    for r in table:
        print(f"{r['config']:18} {r['ex_ok']}/{r['ex_n']} ({100 * r['ex_ok'] / r['ex_n']:.0f}%)")


if __name__ == "__main__":
    main()
