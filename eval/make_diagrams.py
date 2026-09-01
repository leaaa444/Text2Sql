import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

INK = "#1f2937"
TEAL = "#0d9488"
TEAL_SOFT = "#e0f5f1"
SLATE = "#64748b"
SOFT = "#f1f5f9"
LINE = "#94a3b8"
RED = "#b91c1c"
OUT = "eval/diagrams"


def new_ax(w, h):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    return fig, ax


def box(ax, cx, cy, w, h, text, fill=SOFT, edge=SLATE, fs=12, bold=False, dashed=False, tcolor=INK):
    ax.add_patch(
        FancyBboxPatch(
            (cx - w / 2, cy - h / 2), w, h,
            boxstyle="round,pad=0.6,rounding_size=1.6",
            facecolor=fill, edgecolor=edge, linewidth=1.4,
            linestyle=(0, (4, 3)) if dashed else "solid",
        )
    )
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fs,
            color=tcolor, fontweight="bold" if bold else "normal", linespacing=1.4)


def arrow(ax, p1, p2, label=None, curve=0.0, dashed=False, color=INK, fs=10.5,
          lx=0, ly=0, lw=1.6, both=False):
    ax.add_patch(
        FancyArrowPatch(
            p1, p2, arrowstyle="<|-|>" if both else "-|>", mutation_scale=16,
            linewidth=lw, color=color,
            linestyle=(0, (4, 3)) if dashed else "solid",
            connectionstyle=f"arc3,rad={curve}", shrinkA=2, shrinkB=2,
        )
    )
    if label:
        mx, my = (p1[0] + p2[0]) / 2 + lx, (p1[1] + p2[1]) / 2 + ly
        ax.text(mx, my, label, ha="center", va="center", fontsize=fs, color=color,
                bbox=dict(facecolor="white", edgecolor="none", pad=1.5))


def save(fig, name):
    fig.tight_layout()
    fig.savefig(f"{OUT}/{name}", dpi=150)
    plt.close(fig)
    print("Snimljeno:", f"{OUT}/{name}")


def slika21_petlja():
    fig, ax = new_ax(9, 4.6)
    box(ax, 14, 50, 20, 26, "Okruženje", fill=TEAL_SOFT, edge=TEAL, fs=13, bold=True)
    box(ax, 45, 78, 20, 15, "Opažanje\n(senzori)", fs=11.5)
    box(ax, 78, 50, 22, 26, "Odlučivanje\n(agent)", fill=TEAL_SOFT, edge=TEAL, fs=13, bold=True)
    box(ax, 45, 22, 20, 15, "Delovanje\n(aktuatori)", fs=11.5)
    arrow(ax, (20, 64), (36, 76), label="percepti", curve=-0.25, lx=-6, ly=4)
    arrow(ax, (55, 77), (70, 63), curve=-0.25)
    arrow(ax, (72, 36), (55, 24), label="akcije", curve=-0.25, lx=7, ly=-4)
    arrow(ax, (35, 23), (19, 36), curve=-0.25)
    save(fig, "slika21_petlja.png")


def slika22_mas():
    fig, ax = new_ax(9, 5)
    box(ax, 50, 84, 30, 15, "Koordinator\n(upravlja tokom rada)", fill=TEAL_SOFT, edge=TEAL, fs=12.5, bold=True)
    agents = [
        (20, "Specijalizovani\nagent 1\n(planiranje)"),
        (50, "Specijalizovani\nagent 2\n(izvršavanje)"),
        (80, "Specijalizovani\nagent 3\n(provera)"),
    ]
    for x, t in agents:
        box(ax, x, 48, 24, 22, t, fs=11)
        start_x = 50 if x == 50 else (40 if x < 50 else 60)
        arrow(ax, (start_x, 75), (x, 60.5), curve=0, both=True)
    box(ax, 50, 12, 72, 12, "Zajedničko okruženje (podaci, alati, resursi)", fill="#eef2f7", fs=11.5)
    for x, _ in agents:
        arrow(ax, (x, 36), (x, 19), curve=0, color=SLATE, lw=1.2)
    save(fig, "slika22_mas.png")


def slika23_podsistemi():
    fig, ax = new_ax(9, 6.2)
    ax.add_patch(FancyBboxPatch((4, 4), 92, 92, boxstyle="round,pad=0.6,rounding_size=2.5",
                                facecolor="#fbfdff", edgecolor=TEAL, linewidth=1.8))
    ax.text(50, 91, "Učenje i adaptacija (LA)", ha="center", fontsize=13, color=TEAL, fontweight="bold")
    ax.add_patch(FancyBboxPatch((11, 11), 78, 71, boxstyle="round,pad=0.6,rounding_size=2.5",
                                facecolor="#f4f7fa", edgecolor=SLATE, linewidth=1.4))
    ax.text(50, 76.5, "Sprega sa okruženjem", ha="center", fontsize=11.5, color=SLATE)
    box(ax, 23, 52, 19, 20, "Percepcija i\nutemeljenje\n(PG)", fs=11)
    box(ax, 77, 52, 19, 20, "Izvršavanje\nakcija\n(AE)", fs=11)
    box(ax, 50, 22, 30, 13, "Međuagentska\nkomunikacija (IAC) — opciono", fs=10.5, dashed=True)
    box(ax, 50, 52, 24, 22, "Rasuđivanje i\nmodel sveta\n(RWM)", fill=TEAL_SOFT, edge=TEAL, fs=12, bold=True)
    save(fig, "slika23_podsistemi.png")


def slika24_ciklus():
    fig, ax = new_ax(10, 5.2)
    box(ax, 10, 55, 15, 32, "Okruženje", fill=TEAL_SOFT, edge=TEAL, fs=12, bold=True)
    box(ax, 38, 80, 22, 16, "Percepcija i\nutemeljenje (PG)", fs=11)
    box(ax, 72, 80, 24, 16, "Rasuđivanje i\nmodel sveta (RWM)", fill=TEAL_SOFT, edge=TEAL, fs=11, bold=True)
    box(ax, 72, 32, 22, 16, "Izvršavanje\nakcija (AE)", fs=11)
    box(ax, 38, 32, 22, 16, "Učenje i\nadaptacija (LA)", fs=11)
    arrow(ax, (16, 72), (28, 78), label="sirovi ulazi", curve=-0.15, lx=-4, ly=6)
    arrow(ax, (50, 80), (59, 80), label="strukturisani\npercepti", lx=-1.5, ly=11)
    arrow(ax, (72, 71), (72, 41), label="plan akcije", lx=10, ly=0)
    arrow(ax, (68, 23), (12, 37), label="akcije", curve=-0.25, lx=0, ly=-11)
    arrow(ax, (60.5, 32), (49.5, 32), label="povratna\ninformacija", lx=0, ly=9)
    arrow(ax, (44, 41), (63, 71), label="izmene strategije\ni znanja", dashed=True, color=SLATE, curve=0.15, lx=-16, ly=0)
    save(fig, "slika24_ciklus.png")


def slika31_slojevi():
    fig, ax = new_ax(8.6, 5)
    box(ax, 50, 82, 58, 15, "Korisnički interfejs\n(veb aplikacija)", fs=12)
    box(ax, 50, 50, 58, 15, "Agentni sloj\n(višeagentski sistem)", fill=TEAL_SOFT, edge=TEAL, fs=12, bold=True)
    box(ax, 50, 18, 58, 15, "Baza podataka\n(pristup samo za čitanje)", fs=12)
    arrow(ax, (34, 74), (34, 58), label="pitanje", lx=-9)
    arrow(ax, (34, 42), (34, 26), label="SQL upit", lx=-11)
    arrow(ax, (66, 26), (66, 42), label="redovi", lx=9)
    arrow(ax, (66, 58), (66, 74), label="odgovor\n(tabela, sažetak)", lx=13)
    save(fig, "slika31_slojevi.png")


def slika33_grupisanje():
    fig, ax = new_ax(10, 5.6)
    groups = [
        (18, 66, "Rasuđivanje i model sveta\n(RWM)", "Selector\nPlanner\nRetriever\nDeliberator", TEAL_SOFT, TEAL),
        (50, 66, "Percepcija i utemeljenje\n(PG)", "Integrator", SOFT, SLATE),
        (82, 66, "Izvršavanje akcija\n(AE)", "Executor\nPresenter", SOFT, SLATE),
        (33, 22, "Učenje i adaptacija\n(LA)", "Reflector · Guard · Skill Build", SOFT, SLATE),
        (70, 22, "Međuagentska komunikacija\n(IAC)", "Koordinator (graf)", SOFT, SLATE),
    ]
    for x, y, title, items, fill, edge in groups:
        box(ax, x, y, 28, 34 if y > 40 else 22, "", fill=fill, edge=edge)
        ax.text(x, y + (12 if y > 40 else 6.5), title, ha="center", va="center",
                fontsize=10.5, color=edge if edge == TEAL else INK, fontweight="bold", linespacing=1.3)
        ax.text(x, y - (4 if y > 40 else 3.5), items, ha="center", va="center",
                fontsize=10.5, color=SLATE, linespacing=1.5)
    save(fig, "slika33_grupisanje.png")


def slika34_bezbednost():
    fig, ax = new_ax(10, 4.4)
    steps = [
        (24, "Provera teme\n(ulazna kapija)"),
        (53, "Bezbednosna kontrola\n(samo SELECT, LIMIT)"),
        (82, "Nalog samo za čitanje\n(nivo baze)"),
    ]
    ax.text(5, 80, "pitanje /\nnapad", ha="center", fontsize=11, color=RED, fontweight="bold")
    for i, (x, t) in enumerate(steps):
        box(ax, x, 62, 22, 26, t, fs=10.5, fill=SOFT if i < 2 else TEAL_SOFT,
            edge=SLATE if i < 2 else TEAL)
        start = (2, 62) if i == 0 else (steps[i - 1][0] + 12, 62)
        arrow(ax, start, (x - 12, 62), curve=0)
        rx = x - 5 if i == 2 else x
        ax.text(rx, 40, "✗ odbijanje", ha="center", fontsize=10, color=RED)
        arrow(ax, (rx, 48), (rx, 34), color=RED, lw=1.2)
    box(ax, 50, 14, 38, 13, "Prikrivanje ličnih podataka na izlazu (maskiranje)", fs=11)
    arrow(ax, (90, 48), (90, 21), curve=0, label="rezultat", lx=5, ly=8)
    arrow(ax, (90, 17), (70, 14.5), curve=0.05)
    arrow(ax, (30, 14), (8, 14), label="odgovor", lx=0, ly=5)
    save(fig, "slika34_bezbednost.png")


def slika25_veze():
    fig, ax = new_ax(11, 6)
    ax.text(14, 97, "Klase problema", ha="center", fontsize=11.5, color=INK, fontweight="bold")
    ax.text(50, 97, "Podsistemi", ha="center", fontsize=11.5, color=INK, fontweight="bold")
    ax.text(86, 97, "Grupe paterna", ha="center", fontsize=11.5, color=INK, fontweight="bold")

    klase = [
        ("Modeliranje sveta", 84),
        ("Rasuđivanje i\nodlučivanje", 66),
        ("Izvršavanje i\ninterakcija", 48),
        ("Učenje i\nupravljanje", 30),
        ("Mehanizmi\nsaradnje", 12),
    ]
    podsistemi = [
        ("PG", 84), ("RWM", 66), ("AE", 48), ("LA", 30), ("IAC", 12),
    ]
    grupe = [
        ("Fundamentalni\nIntegrator · Retriever · Recorder", 80),
        ("Kognitivni i odlučivački\nSelector · Planner · Deliberator", 58),
        ("Izvršni i interakcijski\nExecutor · Tool Use · Coordinator", 36),
        ("Adaptivni i učeći\nReflector · Skill Build · Controller", 14),
    ]
    for t, y in klase:
        box(ax, 14, y, 21, 13, t, fs=10)
    for t, y in podsistemi:
        box(ax, 50, y, 12, 11, t, fill=TEAL_SOFT, edge=TEAL, fs=11, bold=True)
    for t, y in grupe:
        box(ax, 86, y, 24, 15, t, fs=9.5)

    levo = [(84, 84), (84, 66), (66, 66), (48, 48), (30, 30), (12, 12)]
    for y1, y2 in levo:
        arrow(ax, (25.5, y1), (43, y2), curve=0.0, color=LINE, lw=1.3)
    desno = [(84, 80), (66, 80), (66, 58), (48, 36), (12, 36), (30, 14)]
    for y1, y2 in desno:
        arrow(ax, (57, y1), (73, y2), curve=0.0, color=LINE, lw=1.3)
    save(fig, "slika25_veze.png")


def slika26_metodologija():
    fig, ax = new_ax(10.5, 3.6)
    box(ax, 9, 55, 15, 34, "Postojeći\nagentni\nsistem", fs=10.5)
    steps = [
        (31, "1. Razlaganje", "funkcionalnosti se\npreslikavaju na\npet podsistema"),
        (53, "2. Dijagnoza", "utvrđuju se\nizražene klase\nproblema"),
        (75, "3. Propisivanje", "biraju se\nodgovarajući\ndizajn paterni"),
    ]
    for x, title, sub in steps:
        box(ax, x, 55, 17, 42, "", fill=TEAL_SOFT, edge=TEAL)
        ax.text(x, 68, title, ha="center", va="center", fontsize=11, color=TEAL, fontweight="bold")
        ax.text(x, 50, sub, ha="center", va="center", fontsize=9.5, color=INK, linespacing=1.5)
    box(ax, 91.5, 55, 12, 34, "Poboljšani\nagentni\nsistem", fill=TEAL_SOFT, edge=TEAL, fs=10.5, bold=True)
    arrow(ax, (17.5, 55), (21.5, 55))
    arrow(ax, (40.5, 55), (43.5, 55))
    arrow(ax, (62.5, 55), (65.5, 55))
    arrow(ax, (84.5, 55), (84.8, 55))
    save(fig, "slika26_metodologija.png")


def slika41_stablo():
    fig, ax = new_ax(8.6, 4.6)
    tree = (
        "text2sql/\n"
        "├─ agent/            agentni sloj (Python)\n"
        "│  ├─ nodes/         čvorovi grafa (paterni)\n"
        "│  ├─ db/            veza sa bazom i šema\n"
        "│  ├─ graph.py       koordinator (graf)\n"
        "│  └─ server.py      veb servis (API)\n"
        "├─ web/              korisnički interfejs\n"
        "├─ db/               inicijalizacija baze\n"
        "├─ eval/             evaluacija i ablacija\n"
        "└─ docs/             dokumentacija"
    )
    ax.text(8, 92, tree, ha="left", va="top", fontsize=12.5, color=INK,
            family="monospace", linespacing=1.75)
    save(fig, "slika41_stablo.png")


if __name__ == "__main__":
    import os
    import sys

    sys.stdout.reconfigure(encoding="utf-8")
    os.makedirs(OUT, exist_ok=True)
    slika21_petlja()
    slika22_mas()
    slika23_podsistemi()
    slika24_ciklus()
    slika25_veze()
    slika26_metodologija()
    slika31_slojevi()
    slika33_grupisanje()
    slika34_bezbednost()
    slika41_stablo()
