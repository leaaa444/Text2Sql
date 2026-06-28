"use client";

import { useEffect, useRef, useState } from "react";
import { ask, resetMemory, getSuggestions, type AskResult } from "@/lib/api";
import AnswerView from "@/components/AnswerView";

type Msg = { role: "user"; text: string } | { role: "ai"; result: AskResult };

const STORAGE_KEY = "t2s_chat";

const DEFAULT_EXAMPLES = [
  "Koja tri proizvoda su najskuplja?",
  "Koliko narudžbina ima?",
  "Koliko narudžbina je od kupaca iz Beograda?",
  "Koja kategorija ima najviše proizvoda?",
];

export default function Chat() {
  const [messages, setMessages] = useState<Msg[]>([]);
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [examples, setExamples] = useState<string[]>(DEFAULT_EXAMPLES);
  const endRef = useRef<HTMLDivElement>(null);
  const loaded = useRef(false);

  useEffect(() => {
    getSuggestions().then((s) => {
      if (s.length > 0) setExamples(s);
    });
  }, []);

  useEffect(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      try {
        setMessages(JSON.parse(saved));
      } catch {
        /* ignore */
      }
    }
    loaded.current = true;
  }, []);

  useEffect(() => {
    if (loaded.current) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(messages));
    }
  }, [messages]);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function send(text?: string) {
    const q = (text ?? question).trim();
    if (!q || loading) return;
    setMessages((m) => [...m, { role: "user", text: q }]);
    setQuestion("");
    setLoading(true);
    let result: AskResult;
    try {
      result = await ask(q);
    } catch {
      result = { error: "Backend nije dostupan (proveri da li server radi)." };
    }
    setMessages((m) => [...m, { role: "ai", result }]);
    setLoading(false);
  }

  async function clearChat() {
    setMessages([]);
    localStorage.removeItem(STORAGE_KEY);
    try {
      await resetMemory();
    } catch {
      /* ignore */
    }
  }

  return (
    <div className="chat">
      {messages.length > 0 && (
        <div className="chat-head">
          <button className="info-btn" onClick={clearChat}>
            Obriši razgovor
          </button>
        </div>
      )}
      <div className="chat-scroll">
        {messages.length === 0 ? (
          <div className="chat-hero">
            <div className="hero-icon">✦</div>
            <h1 className="hero-title">Pitaj bazu prirodnim jezikom</h1>
            <p className="hero-sub">Agent napiše SQL, proveri ga i izvrši — ti samo pitaš.</p>
            <div className="chips">
              {examples.map((ex) => (
                <button key={ex} className="chip" onClick={() => send(ex)}>
                  {ex}
                </button>
              ))}
            </div>
          </div>
        ) : (
          <div className="chat-inner">
            {messages.map((m, i) =>
              m.role === "user" ? (
                <div key={i} className="msg-user">
                  {m.text}
                </div>
              ) : (
                <div key={i} className="msg-ai">
                  <AnswerView result={m.result} />
                </div>
              )
            )}
            {loading && (
              <div className="msg-ai">
                <span className="thinking">
                  <span></span>
                  <span></span>
                  <span></span>
                </span>
              </div>
            )}
            <div ref={endRef} />
          </div>
        )}
      </div>
      <div className="composer">
        <div className="composer-inner">
          <input
            type="text"
            value={question}
            placeholder="Postavi pitanje…"
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") send();
            }}
          />
          <button className="send" onClick={() => send()}>
            Pošalji
          </button>
        </div>
      </div>
    </div>
  );
}
