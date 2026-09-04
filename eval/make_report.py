import json
import os
from datetime import date

EVAL = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(EVAL, "REZULTATI.md")


def _load(name):
    path = os.path.join(EVAL, name)
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _cell(value):
    text = "" if value is None else str(value)
    return " ".join(text.split()).replace("|", "\\|")


def _pct(ok, n):
    return f"{ok}/{n} ({100 * ok / n:.1f}%)" if n else "-"


def _tabela(header, rows):
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    for row in rows:
        lines.append("| " + " | ".join(_cell(c) for c in row) + " |")
    return lines + [""]


def _sql(text):
    return f"`{' '.join(str(text).split())}`" if text else ""


def _pitanja(items, tekst):
    rows = [
        [r["id"], tekst.get(r["id"], ""), "DA" if r["match"] else "NE",
         r.get("retry_count", ""), _sql(r.get("agent_sql")), r.get("error") or ""]
        for r in items
    ]
    return _tabela(["ID", "Pitanje", "Tačno", "Samoispr.", "SQL koji je sistem izvršio", "Greška"], rows)


def _napadi(items, tekst):
    rows = [
        [r["id"], tekst.get(r["id"], ""), "DA" if r["passed"] else "NE",
         r.get("error") or "", _sql(r.get("agent_sql")), r.get("odgovor") or ""]
        for r in items
    ]
    return _tabela(["ID", "Napad", "Odbranjen", "Poruka sistema", "SQL", "Odgovor"], rows)


def _po_kategorijama(items):
    cats = {}
    for r in items:
        c = cats.setdefault(r["category"], [0, 0])
        c[1] += 1
        c[0] += int(r["match"])
    return _tabela(["Kategorija", "Tačno"], [[k, _pct(ok, n)] for k, (ok, n) in cats.items()])


def _ablacija(naslov, data, gold_tekst, napad_tekst):
    lines = [f"## {naslov}", ""]
    if not data:
        return lines + ["Nema rezultata.", ""]
    modeli = sorted({r.get("model", "") for r in data if r.get("model")})
    if modeli:
        lines.append("Model: " + ", ".join(modeli))
        lines.append("")
    rows = []
    for r in data:
        ex = _pct(r["ex_ok"], r["ex_n"]) if "ex_n" in r else "-"
        se = _pct(r["sec_ok"], r["sec_n"]) if "sec_n" in r else "-"
        rows.append([r["config"], ex, se])
    lines += _tabela(["Konfiguracija", "Tačnost (EX)", "Bezbednost"], rows)
    for r in data:
        if "pitanja" not in r and "napadi" not in r:
            continue
        lines += [f"### {r['config']}", ""]
        if r.get("pitanja"):
            lines += _pitanja(r["pitanja"], gold_tekst)
        if r.get("napadi"):
            lines += _napadi(r["napadi"], napad_tekst)
    return lines


def main():
    gold_tekst = {g["id"]: g["question"] for g in _load("gold_set.json") or []}
    hard_tekst = {g["id"]: g["question"] for g in _load("gold_hard.json") or []}
    napad_tekst = {a["id"]: a["question"] for a in _load("attacks.json") or []}

    lines = [
        "# Rezultati merenja",
        "",
        f"Generisano: {date.today().isoformat()} (`python -m eval.make_report`). "
        f"Skupovi: {len(gold_tekst)} pitanja sa poznatim odgovorima (`gold_set.json`), "
        f"{len(hard_tekst)} težih pitanja (`gold_hard.json`), {len(napad_tekst)} napada (`attacks.json`). "
        "Za svako pitanje zabeležen je SQL koji je sistem na kraju izvršio i da li se rezultat poklopio "
        "sa tačnim odgovorom (metrika EX).",
        "",
    ]

    pun = _load("results_baseline.json")
    lines += ["## 1. Pun sistem", ""]
    if pun:
        gold = pun.get("gold", [])
        attacks = pun.get("attacks", [])
        ex_ok = sum(1 for r in gold if r["match"])
        sec_ok = sum(1 for r in attacks if r["passed"])
        calls = [r["llm_calls"] for r in gold if r.get("llm_calls")]
        times = [r["elapsed_ms"] for r in gold if r.get("elapsed_ms")]
        lines.append(f"Model: {pun.get('model', '?')}. Tačnost: {_pct(ex_ok, len(gold))}. "
                     f"Bezbednost: {_pct(sec_ok, len(attacks))}.")
        if calls and times:
            lines.append(f"Prosek: {sum(calls) / len(calls):.1f} poziva modelu i "
                         f"{sum(times) / len(times) / 1000:.1f} s po pitanju; samoispravljanja ukupno: "
                         f"{sum(r.get('retry_count') or 0 for r in gold)}.")
        lines.append("")
        lines += _po_kategorijama(gold)
        lines += _pitanja(gold, gold_tekst)
        lines += _napadi(attacks, napad_tekst)
    else:
        lines += ["Nema rezultata.", ""]

    lines += _ablacija(
        "2. Ablaciona studija (isključivanje po jednog paterna iz punog sistema)",
        _load("results_ablation.json"), gold_tekst, napad_tekst,
    )
    lines += _ablacija(
        "3. Dodavanje po jednog paterna na polazno rešenje",
        _load("results_ablation_additive.json"), gold_tekst, napad_tekst,
    )
    lines += _ablacija("4. Ablacija na težim pitanjima", _load("results_ablation_hard.json"), hard_tekst, napad_tekst)

    stab = _load("results_stability.json")
    lines += ["## 5. Stabilnost (ponovljena merenja punog sistema)", ""]
    if stab:
        ex, se = stab["ex"], stab["sec"]
        lines.append(f"Model: {stab.get('model', '?')}. Ponavljanja: {stab['repeats']}. "
                     f"EX po pokretu: {ex['po_pokretu']} (prosek {ex['prosek_pct']}%). "
                     f"Bezbednost po pokretu: {se['po_pokretu']} (prosek {se['prosek_pct']}%).")
        lines.append("")
        for p in stab.get("pokreti", []):
            lines += [f"### Pokret {p['pokret']}", ""]
            lines += _pitanja(p["pitanja"], gold_tekst)
            lines += _napadi(p["napadi"], napad_tekst)
    else:
        lines += ["Nema rezultata.", ""]

    lines += _ablacija("6. Slabiji model (poređenje)", _load("results_ablation_8b.json"), gold_tekst, napad_tekst)

    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines).rstrip() + "\n")
    print(f"Snimljeno: {OUT}")


if __name__ == "__main__":
    main()