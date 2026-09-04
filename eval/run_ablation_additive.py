import json
import os
import sys
from dataclasses import replace

from agent import ablation, skills
from agent.config import AblationConfig
from eval import evaluate


def samo(**kwargs):
    return replace(AblationConfig.baseline(), **kwargs)


CONFIGS = [
    ("Polazno resenje", AblationConfig.baseline(), True, True),
    ("samo Retriever", samo(use_retriever=True), True, False),
    ("samo Selector", samo(use_selector=True), True, False),
    ("samo Planner", samo(use_planner=True), True, False),
    ("samo Integrator", samo(use_integrator=True), True, False),
    ("samo Reflector", samo(use_reflector=True, max_retries=2), True, False),
    ("samo Recorder", samo(use_recorder=True), True, False),
    ("samo Skill-build", samo(use_skill_build=True), True, False),
    ("samo Scope", samo(use_scope=True), False, True),
    ("samo Guard", samo(use_security_guard=True), False, True),
]

RESULTS_PATH = os.getenv("ADDITIVE_PATH", "eval/results_ablation_additive.json")


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
        skills.reset()
        ablation.set_config(cfg)
        print(f"\n########## {name} ##########")
        row = {"config": name, "model": evaluate.model_name()}
        if do_gold:
            gold = evaluate.evaluate_gold()
            row["ex_ok"] = sum(1 for r in gold if r["match"])
            row["ex_n"] = len(gold)
            row["pitanja"] = gold
        if do_attacks:
            attacks = evaluate.evaluate_attacks()
            row["sec_ok"] = sum(1 for r in attacks if r["passed"])
            row["sec_n"] = len(attacks)
            row["napadi"] = attacks
        table.append(row)
        with open(RESULTS_PATH, "w", encoding="utf-8") as f:
            json.dump(table, f, ensure_ascii=False, indent=2)
    ablation.reset()

    print("\n=== DODAVANJE PO JEDNOG PATERNA NA POLAZNO RESENJE ===")
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
