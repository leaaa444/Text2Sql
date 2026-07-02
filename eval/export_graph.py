import sys

from agent.graph import graph

MMD_PATH = "eval/graph.mmd"
PNG_PATH = "eval/graph.png"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    drawable = graph.get_graph()

    mermaid = drawable.draw_mermaid()
    with open(MMD_PATH, "w", encoding="utf-8") as f:
        f.write(mermaid)
    print(f"Snimljen Mermaid izvor: {MMD_PATH}")

    try:
        png = drawable.draw_mermaid_png()
        with open(PNG_PATH, "wb") as f:
            f.write(png)
        print(f"Snimljena slika: {PNG_PATH}")
    except Exception as exc:
        print(f"PNG nije napravljen (verovatno nema interneta): {exc}")
        print("Mermaid izvor je tu — nalepi ga na https://mermaid.live ili u draw.io.")


if __name__ == "__main__":
    main()
