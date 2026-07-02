import json
import os
import sys

from agent import ablation
from agent.config import AblationConfig
from eval import evaluate

CONFIGS = [
    ("Pun sistem", AblationConfig(), True, True),
    ("bez Retriever", AblationConfig(use_retriever=False), True, False),
    ("bez Selector", AblationConfig(use_selector=False), True, False),
    ("bez Planner", AblationConfig(use_planner=False), True, False),
    ("bez Integrator", AblationConfig(use_integrator=False), True, True),
    ("bez Reflector", AblationConfig(use_reflector=False), True, False),
    ("bez Recorder", AblationConfig(use_recorder=False), True, False),
    ("bez Skill-build", AblationConfig(use_skill_build=False), True, False),
    ("bez Scope", AblationConfig(use_scope=False), False, True),
    ("bez Guard", AblationConfig(use_security_guard=False), False, True),
    ("bez Scope+Guard", AblationConfig(use_scope=False, use_security_guard=False), False, True),
    ("bez svega", AblationConfig.baseline(), True, True),
]

RESULTS_PATH = "eval/results_ablation.json"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    table = []
    done = set()
    if os.path.exists(RESULTS_PATH):
        with open(RESULTS_PATH, encoding="utf-8") as f:
            table = json.load(f)
        done = {r["config"] for r in table}

    for name, cfg, do_gold, do_attacks in CONFIGS:
        if name in done:
            print(f"preskacem (vec uradjeno): {name}")
            continue
        ablation.set_config(cfg)
        print(f"\n########## {name} ##########")
        row = {"config": name}
        if do_gold:
            gold = evaluate.evaluate_gold()
            row["ex_ok"] = sum(1 for r in gold if r["match"])
            row["ex_n"] = len(gold)
        if do_attacks:
            attacks = evaluate.evaluate_attacks()
            row["sec_ok"] = sum(1 for r in attacks if r["passed"])
            row["sec_n"] = len(attacks)
        table.append(row)
        with open(RESULTS_PATH, "w", encoding="utf-8") as f:
            json.dump(table, f, ensure_ascii=False, indent=2)
    ablation.reset()

    print("\n=== ABLACIONA TABELA ===")
    print(f"{'Konfiguracija':18} {'EX':>14} {'Bezbednost':>14}")
    for r in table:
        if "ex_n" in r:
            ex = f"{r['ex_ok']}/{r['ex_n']} ({100 * r['ex_ok'] / r['ex_n']:.0f}%)"
        else:
            ex = "-"
        if "sec_n" in r:
            se = f"{r['sec_ok']}/{r['sec_n']} ({100 * r['sec_ok'] / r['sec_n']:.0f}%)"
        else:
            se = "-"
        print(f"{r['config']:18} {ex:>14} {se:>14}")


if __name__ == "__main__":
    main()
