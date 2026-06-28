"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const links = [
  { href: "/", label: "Razgovor" },
  { href: "/tabele", label: "Tabele" },
];

export default function Sidebar() {
  const path = usePathname();
  return (
    <aside className="sidebar">
      <div className="brand">
        <span className="brand-mark">t2s</span>
        <div>
          <div className="brand-name">text2sql</div>
          <div className="brand-sub">agentni asistent</div>
        </div>
      </div>
      <nav>
        {links.map((l) => (
          <Link
            key={l.href}
            href={l.href}
            className={`nav-link${path === l.href ? " active" : ""}`}
          >
            {l.label}
          </Link>
        ))}
      </nav>
      <div className="sidebar-foot">
        12 agentnih paterna
        <br />
        LangGraph · FastAPI · PostgreSQL
      </div>
    </aside>
  );
}
