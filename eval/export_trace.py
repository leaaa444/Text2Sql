import sys

from agent import graph, memory

OUT_PATH = "docs/trace-primer.md"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    question = sys.argv[1] if len(sys.argv) > 1 else "Koji glumac glumi u najvise filmova?"

    memory.reset()
    out = graph.answer(question)

    lines = []
    lines.append("# Primer kompletnog traga (trace) kroz agentni graf")
    lines.append("")
    lines.append(f"**Pitanje:** {question}")
    lines.append("")
    lines.append("## Koraci kroz cvorove")
    lines.append("")
    lines.append("| # | Cvor (patern) | Ishod |")
    lines.append("|---|---|---|")
    for i, step in enumerate(out["trace"], 1):
        lines.append(f"| {i} | `{step['node']}` | {step['info']} |")
    lines.append("")
    if out.get("plan"):
        lines.append("## Plan (Planner)")
        lines.append("")
        for i, step in enumerate(out["plan"], 1):
            lines.append(f"{i}. {step}")
        lines.append("")
    lines.append("## Generisani SQL (Deliberator, posle Guard-a)")
    lines.append("")
    lines.append("```sql")
    lines.append(out.get("sql", ""))
    lines.append("```")
    lines.append("")
    lines.append("## Rezultat")
    lines.append("")
    lines.append(f"**Odgovor (Presenter):** {out.get('summary', '')}")
    lines.append("")
    if out.get("error"):
        lines.append(f"**Greska:** {out['error']}")
        lines.append("")
    lines.append(f"**Broj LLM poziva:** {out.get('llm_calls')} · "
                 f"**Vreme:** {out.get('elapsed_ms', 0) / 1000:.1f} s · "
                 f"**Samoispravljanja:** {out.get('retry_count', 0)}")
    lines.append("")

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Snimljeno u {OUT_PATH}")
    print()
    print("\n".join(lines))


if __name__ == "__main__":
    main()
