import "./globals.css";
import type { Metadata } from "next";
import type { ReactNode } from "react";
import { Manrope, JetBrains_Mono } from "next/font/google";
import Navbar from "@/components/Navbar";

const sans = Manrope({ subsets: ["latin", "latin-ext"], variable: "--font-sans", display: "swap" });
const mono = JetBrains_Mono({ subsets: ["latin", "latin-ext"], variable: "--font-mono", display: "swap" });

export const metadata: Metadata = {
  title: "text2sql — agentni asistent",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="sr" className={`${sans.variable} ${mono.variable}`}>
      <body>
        <div className="app">
          <Navbar />
          <main className="main">{children}</main>
        </div>
      </body>
    </html>
  );
}
