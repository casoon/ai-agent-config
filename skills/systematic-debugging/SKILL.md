---
name: systematic-debugging
description: Diszipliniertes Root-Cause-Debugging für harte Bugs und Performance-Regressionen im Astro/Cloudflare-Stack — zuerst eine schnelle Pass/Fail-Feedback-Loop bauen, dann Ursache belegen, dann minimal fixen. Nutzen, wenn etwas kaputt/flaky ist, wirft, fehlschlägt, sich falsch verhält, seit einem Deploy langsamer wurde, oder wenn schon 2+ Fix-Versuche gescheitert sind. Nicht für triviale, offensichtliche Einzeiler (Typo, fehlender Import) und nicht für das Schreiben neuer E2E-Specs (siehe playwright).
---

# Systematic Debugging

## Iron Law

```
KEIN FIX, BEVOR DIE URSACHE BELEGT IST.
```

Symptom-Fixes sind kein Fix. Wer nicht sagen kann *warum* der Bug auftritt, darf keinen Fix vorschlagen. "Ich sehe das Problem" ≠ Ursache verstanden.

## Der eigentliche Trick: zuerst die Feedback-Loop

Das ist der Skill — der Rest ist Mechanik. Baue **zuerst** ein schnelles, deterministisches, agent-ausführbares Pass/Fail-Signal für den Bug. Hast du das, ist der Bug zu ~90 % gelöst; Bisection, Hypothesen-Test und Instrumentierung konsumieren nur noch dieses Signal. Hast du es nicht, rettet dich kein Code-Starren.

Loop-Optionen für diesen Stack, in etwa dieser Reihenfolge:

1. **Playwright-Skript** — treibt UI/Island, prüft DOM/Console/Network. Siehe Skill `playwright` (E2E + axe). Für Hydration-/Client-Bugs die erste Wahl.
2. **`curl` gegen `wrangler dev`** — SSR-Response, API-Route oder Worker-Fetch deterministisch abfragen; Body/Header/Status gegen bekannt-gut diffen.
3. **Trace-Replay** — echten Request/Payload (HAR, gespeicherter Body) isoliert durch den Code-Pfad schicken.
4. **Differential-Loop** — gleicher Input gegen alt vs. neu (Commit/Config) diffen; ideal für "seit Deploy X kaputt".

Mach die Loop **schnell, scharf, deterministisch**: Zeit pinnen, RNG seeden, auf das konkrete Symptom asserten (nicht "crasht nicht"). Eine 2-s-deterministische Loop schlägt eine 30-s-flaky Loop.

Bei nicht-deterministischen Bugs ist das Ziel keine saubere Repro, sondern eine **höhere Reproduktionsrate**: Trigger 100× loopen, parallelisieren, Timing-Fenster verengen. 50 % flake ist debugbar, 1 % nicht.

Kannst du keine Loop bauen? **Stopp, sag es explizit**, liste was du versucht hast, und fordere Artefakt (HAR, Log-Dump, `wrangler tail`-Ausgabe) oder Umgebungszugang an. Nicht ohne Loop hypothesieren.

## Component-Grenzen isolieren (dieser Stack)

Bugs leben an den Grenzen. Belege pro Grenze, welche Daten rein- und rausgehen:

- **SSR vs. Island-Hydration** — Rendert der Server korrekt, bricht es erst nach Hydration? "View Source" (SSR-HTML) gegen DOM nach Hydration vergleichen. Häufig: Server/Client-State-Mismatch, `client:*`-Directive falsch, Svelte-5-Runes reagieren nicht wie erwartet.
- **Worker-Fetch-Layer** — `curl` gegen `wrangler dev` isoliert Server-seitig vom Browser. Bindings/Env korrekt propagiert?
- **Worker-Logs** — `wrangler tail` für Live-Logs aus dem laufenden Worker; Boundary-Logs mit eindeutigem Prefix taggen (`[DBG-a4f2]`), Cleanup = ein `grep`.

## Phasen

1. **Reproduzieren** — Loop bauen und laufen lassen, bis genau das vom User beschriebene Symptom erscheint (nicht ein zufällig benachbartes). Symptom exakt festhalten.
2. **Isolieren** — an welcher Component-Grenze bricht es? Recent changes prüfen (`git log --oneline -10`, `git diff`).
3. **Ursache belegen** — 3–5 falsifizierbare Hypothesen ranken ("Wenn X Ursache, dann macht Änderung Y den Bug weg"). Pro Probe **eine** Variable ändern. Nicht "alles loggen und grep".
4. **Minimal fixen** — kleinstmögliche Änderung an der Ursache. Kein "while I'm here"-Refactor, kein Bundling.
5. **Verifizieren** — Regressionstest an korrektem Seam schreiben (bricht der Bug erst nach Hydration, muss der Test das erreichen — sonst falsche Sicherheit). Dann Phase-1-Loop gegen das Originalszenario. Getaggte Debug-Logs entfernen.

## Rule of Three

Nach **3 gescheiterten Fix-Versuchen: STOPP.** Nicht Fix #4. Das ist kein weiterer Fehlschlag einer Hypothese — es ist ein Zeichen für falsche Architektur/Annahme.

Muster: jeder Fix deckt an anderer Stelle neues Coupling/Shared State auf, oder erzeugt neues Symptom woanders, oder braucht "massives Refactoring". Dann Annahme/Architektur infrage stellen und **mit dem User besprechen**, nicht weiterfixen.

## Red Flags — STOP

- "Quick fix jetzt, Ursache später"
- "Einfach X ändern und schauen ob's läuft"
- Mehrere Änderungen gleichzeitig, dann testen
- Lösung vorschlagen, bevor der Datenfluss verfolgt ist
- "Wahrscheinlich X, fix ich mal"
- **"Noch ein Versuch" (nach 2+ Fehlversuchen)**

Jede davon heißt: zurück zu Phase 1.

## Common Rationalizations

| Ausrede | Realität |
|---------|----------|
| "Ist simpel, kein Prozess nötig" | Simple Bugs haben auch Ursachen. Der Prozess ist bei ihnen schnell. |
| "Notfall, keine Zeit" | Systematisch ist *schneller* als Raten-und-Prüfen. |
| "Erst fixen, dann untersuchen" | Der erste Fix setzt das Muster. Gleich richtig machen. |
| "Test schreib ich, wenn der Fix steht" | Ungetestete Fixes halten nicht. Test zuerst beweist es. |
| "Ich seh das Problem doch" | Symptom sehen ≠ Ursache verstehen. |
| "Noch ein Fix-Versuch" (nach 2+) | 3+ Fehlschläge = Architekturproblem, nicht Fix #4. |
