---
name: agent-config-authoring
description: Konventionen für die Projekt-Config-Ebene der Coding-Agenten (CLAUDE.md / AGENTS.md / GEMINI.md) — Verhaltens-Baseline, Hierarchie, Token-Effizienz, Multi-Tool-Symlinks. Vor allem: die Entscheidung, was in CLAUDE.md gehört vs. in einen Skill vs. Auto-Memory vs. knowledge-base. Nutzen beim Aufsetzen/Verbessern von Projekt-Config. NICHT für das Schreiben einzelner Skills (→ skill-authoring).
---

# Agent-Config-Authoring

Steuerung verlagert sich von Einzel-Prompts zu **dauerhaft gepflegten Projektdateien**. Behandle `CLAUDE.md` wie `README.md`/`.editorconfig`/CI — Teil des Projekts, versioniert, wiederholbar. Diese Datei = die *immer-aktive* Ebene; Skills/Memory/Wissensbasis sind die *bei-Bedarf*-Ebenen.

## Was gehört wohin (Kern-Entscheidung)
| Ebene | Inhalt | Merkmal |
|---|---|---|
| **CLAUDE.md / AGENTS.md** | Verhaltensregeln, Projekt-Architektur/-Konventionen, Definition-of-Done, Antwortformat | **immer geladen** → kurz halten |
| **Skill** ([[skill-authoring]]) | getriggertes Domänenwissen / Workflow | lädt nur bei Bedarf |
| **Auto-Memory** (`MEMORY.md`) | dauerhafte Nutzer-Präferenzen + Feedback | sessionübergreifend, personenbezogen |
| **knowledge-base** ([[knowledge-base]]) | belegte Projekt-/Domänenfakten mit Herkunft | kompiliert, verlinkt, gelintet |

Faustregel: **immer-relevant + kurz → CLAUDE.md**; **fachlich + getriggert → Skill**; **Präferenz → Memory**; **belegbarer Fakt → knowledge-base**. Domänenwissen NICHT in CLAUDE.md kippen (bläht jeden Turn auf).

## Verhaltens-Baseline (Karpathy)
Fünf Regeln als Einstieg für nahezu jedes Projekt — knapp, ausführbar formuliert:
1. Erst nachdenken, dann programmieren.
2. Bei Unklarheit nachfragen statt raten.
3. Nur den nötigen Code schreiben.
4. Nur die angeforderten Stellen ändern.
5. Vorab definieren, wann eine Aufgabe „fertig" ist.
Effekt: weniger Halluzination, weniger unnötige Refactorings, präzisere Änderungen — etwas langsamer, deutlich zuverlässiger.

## Hierarchie
Der Agent liest alle `CLAUDE.md` im Verzeichnisbaum: **global** (`~/.claude/CLAUDE.md`) → **projekt** (Repo-Root) → **ordnerspezifisch**. So wird Wissen gestaffelt: generell oben, spezifisch unten. Ordner-Config nur, wo sich Regeln wirklich unterscheiden.

## Multi-Tool per Symlink
Eine Quelle, auf `CLAUDE.md` + `AGENTS.md` + `GEMINI.md` verlinkt → einmal ändern, überall aktiv. (Genau das Muster dieses Repos: eine `GLOBAL.md` als Quelle.) Ideal, wenn man zwischen Claude/Codex/Gemini wechselt.

## Token-Effizienz-Modus (optional)
Füllfloskeln unterbinden: „Gute Frage…", Wiederholung der Anfrage, Höflichkeits-Schluss. Bringt spürbar kürzere Antworten (Benchmarks: bis ~60% weniger Wörter, ~12% weniger Output-Tokens). **Trade-off:** die Config-Datei selbst kostet Input-Tokens — lohnt sich bei Automatisierung, vielen Reviews, Pipelines; bei gelegentlichen Einzelanfragen kaum.

## MCP-Server: Kontextbudget
Jeder aktive MCP-Server kostet Tokens **beim Session-Start** (Tool-Schemas werden vorab geladen) — grob ~55k Tokens pro Server, unabhängig davon, ob er in der Session je aufgerufen wird. Faustregel: **max. 3–5 aktive MCPs** pro Projekt-`.mcp.json`. Bei mehr: nicht dauerhaft aktivieren, sondern nur bei Bedarf (projektspezifische `.mcp.json` statt global, oder situativ per Flag zuschalten).

## Gotchas
- **CLAUDE.md kurz halten** — sie ist immer geladen; jede Zeile ist Dauer-Token-Kost.
- **Regeln ausführbar formulieren:** „bei Unklarheit nachfragen", nicht „sei schlau". Vgl. die Retrospektive-Disziplin in [[conversation-retrospective]].
- **Keine Secrets / Maschinen-Config** in getrackte CLAUDE.md (→ gitignore).
- **Nicht duplizieren:** was ein Skill/Memory schon trägt, nicht zusätzlich in CLAUDE.md wiederholen.
- Die Varianten (Karpathy / Token-effizient / Multi-Tool / Memory-Bank) **schließen sich nicht aus** — kombinieren.
