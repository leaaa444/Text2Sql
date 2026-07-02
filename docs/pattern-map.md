# Mapa agentnih paterna → kod

Svaki od 12 paterna realizovan je kao zaseban deo sistema. Imena LangGraph
čvorova odgovaraju imenima paterna.

## 12 paterna

| # | Patern | Fajl | Ključna funkcija | Šta radi | Ablacioni prekidač |
|---|---|---|---|---|---|
| 1 | Coordinator | `agent/graph.py` | `_build`, `answer` | LangGraph `StateGraph`: čvorovi, ivice i uslovno granaje — orkestrira ceo tok | (sama orkestracija) |
| 2 | Recorder | `agent/nodes/recorder.py` + `agent/memory.py` | `recorder_load_node`, `recorder_save_node` | Učitava/čuva istoriju razgovora (kontekst između pitanja) | `use_recorder` |
| 3 | Retriever | `agent/nodes/retriever.py` + `agent/db/schema.py` | `retriever_node`, `get_schema_text` | Učitava šemu baze (tabele, kolone, strani ključevi) | `use_retriever` |
| 4 | Selector | `agent/nodes/selector.py` | `selector_node` | Pretvara nastavno pitanje u samostalno koristeći istoriju | `use_selector` |
| 5 | Planner | `agent/nodes/planner.py` | `planner_node` | Razbija pitanje na 1–4 koraka za izgradnju SQL-a | `use_planner` |
| 6 | Deliberator | `agent/nodes/deliberator.py` | `deliberator_node` | Generiše SQL upit (jezgro rezonovanja) | (jezgro, bez prekidača) |
| 7 | Integrator | `agent/nodes/integrator.py` | `integrator_node` | Validira SQL: parsira (`sqlglot`) i proverava da li tabele postoje | `use_integrator` |
| 8 | Tool Use | `agent/db/connection.py` | `run_query` | Spoljašnji alat: read-only pristup PostgreSQL bazi | (alat, koristi ga Executor) |
| 9 | Executor | `agent/nodes/executor.py` | `executor_node` | Izvršava SQL, ograničava broj redova, maskira PII | (jezgro, bez prekidača) |
| 10 | Reflector | `agent/nodes/reflector.py` | `reflector_node` | Na grešku popravlja SQL i pokušava ponovo | `use_reflector`, `max_retries` |
| 11 | Skill Build | `agent/skills.py` | `retrieve`, `add` | Few-shot uzori: pamti uspešne parove pitanje→SQL i ubacuje slične | `use_skill_build` |
| 12 | Controller | `agent/nodes/guard.py` + `agent/nodes/scope.py` | `guard_node`, `scope_node` | Bezbednosna kontrola: samo-SELECT, jedan upit, LIMIT, te ulazna kapija za temu | `use_security_guard`, `use_scope` |

## Pomoćni čvorovi (nisu među 12 paterna)

| Komponenta | Fajl | Uloga |
|---|---|---|
| Presenter | `agent/nodes/presenter.py` | Pretvara redove u odgovor na prirodnom jeziku; samo iz podataka; `[NO_DATA]` kad podaci ne odgovaraju na pitanje |
| Stanje | `agent/state.py` | `AgentState` (TypedDict) — zajedničko stanje kroz graf |
| LLM sloj | `agent/llm.py` | `get_llm` — zamenjiv provajder (Anthropic/Gemini/Groq), rate-limiter, brojač poziva |

## Bezbednost — slojevi (defense in depth)

| Sloj | Gde živi | Šta zaustavlja |
|---|---|---|
| 1. Scope (ulaz) | `nodes/scope.py` | off-topic, jailbreak |
| 2. Integrator | `nodes/integrator.py` | nepoznate tabele / neispravan SQL |
| 3. Controller/Guard | `nodes/guard.py` | ne-SELECT upiti, više upita, izostanak LIMIT-a |
| 4. Read-only uloga | `db/init/01_readonly_role.sql` + `db/connection.py` | bilo kakav upis na nivou baze (DROP/DELETE/UPDATE) |
| 5. PII maskiranje | `guard.py` (`mask_pii`), primenjeno u `executor.py` | otkrivanje email/telefon/lozinka |

Slojevi 4 i 5 su **uvek aktivni** (nezavisni od paterna) — zato i kad se Guard ugasi
u ablaciji, destruktivni napadi i dalje ne prolaze.

## Tok izvršavanja

`recorder_load → retriever → scope → selector → planner → deliberator → integrator → guard → executor → presenter → recorder_save`

Uslovna granaja: scope može odbiti (→ kraj); integrator/executor na grešku idu u
reflector (petlja nazad), uz ograničenje `max_retries`. Auto-generisani dijagram:
`eval/graph.png` (izvor `eval/graph.mmd`).
