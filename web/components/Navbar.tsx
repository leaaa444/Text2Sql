"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const links = [
  { href: "/", label: "Razgovor" },
  { href: "/tabele", label: "Tabele" },
];

export default function Navbar() {
  const path = usePathname();
  return (
    <header className="navbar">
      <Link href="/" className="brand">
        <span className="brand-mark">t2s</span>
        <div>
          <div className="brand-name">text2sql</div>
          <div className="brand-sub">agentni asistent</div>
        </div>
      </Link>
      <nav className="nav-links">
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
    </header>
  );
}
