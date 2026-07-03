---
name: llm-council
description: Deliberationsverfahren (Karpathys „LLM Council") für Entscheidungen mit echten Zielkonflikten — unabhängige Perspektiven erzeugen, sich gegenseitig kritisieren lassen, dann synthetisieren. Nutzen bei Strategie, Positionierung, Architektur, Preisgestaltung, Priorisierung, Design-Richtung. NICHT für Faktenfragen, Zusammenfassungen, Übersetzungen oder kleine Aufgaben.
---

# LLM Council

Kein Super-Prompt, sondern ein Qualitätssicherungs-Verfahren gegen die zwei
Kernschwächen von Sprachmodellen: **Halluzination** (plausibel, aber falsch)
und **Confirmation Bias** (das Modell übernimmt die im Prompt implizierte
Richtung, statt sie zu prüfen). Statt einer Meinung → mehrere unabhängige
Sichten, gegenseitige Kritik, begründete Synthese. Wie Peer Review.

## Wann verwenden
Entscheidungen mit echten Trade-offs: Unternehmens-/Produktstrategie,
Positionierung, Architektur, größere Investitionen, Preisgestaltung,
Feature-Priorisierung, Design-Richtung.

## Wann NICHT
Faktenfragen, Zusammenfassungen, Übersetzungen, Textentwürfe, kleine
Code-Aufgaben. Dort ist der Aufwand reiner Overkill.

## Beste Form: mehrere unabhängige Agents
In Claude Code läuft das echt-parallel, nicht simuliert — das ist der Kern:
**echte Unabhängigkeit schlägt Rollenspiel in einem Kontext.**

- **Phase 1 — Unabhängige Erstantworten.** Mehrere Ratsmitglieder bekommen
  exakt dieselbe Frage und sehen einander NICHT. Per `Agent`-Tool mehrere
  Agents parallel spawnen (oder das `Workflow`-Tool für die 3-Stufen-Pipeline).
  Verhindert Gruppendenken.
- **Phase 2 — Anonymisiertes Peer Review.** Jedes Mitglied bekommt alle
  anderen Antworten, aber anonym („Antwort A/B/C", nicht „GPT/Claude") — sonst
  Marken-/Reihenfolge-Bias. Jedes beantwortet: Welche Antwort ist am stärksten?
  Welche hat den größten blinden Fleck? **Was haben ALLE übersehen?**
- **Phase 3 — Chairman.** Ein weiteres Modell bekommt alle Erstantworten +
  Bewertungen. Es beantwortet NICHT erneut die Frage, sondern gewichtet:
  Gemeinsamkeiten, Widersprüche, starke Argumente → konsolidierte Empfehlung.

Wenn mehrere Anbieter verfügbar sind (GPT, Claude, Gemini, Grok via
OpenRouter o.ä.), erhöht das die Diversität zusätzlich.

## Disziplin gegen Anchoring
- Formuliere jede Perspektive **falsifizierbar**: „Wenn X zutrifft, sagt das Y
  voraus" — nicht bloß plausibel. Prüfbare Vorhersagen schlagen wohlklingende Meinungen.
- Erzeuge **3–5 gerankte** Perspektiven und zeige dem User die **Rangliste VOR**
  der Chairman-Synthese. Billiger Checkpoint: der User re-rankt oft sofort und
  verhindert, dass sich die Synthese an der erstbesten Sicht festbeißt.

## Vereinfachte Ein-Modell-Variante (5 Denkrollen)
Ohne mehrere Modelle: dasselbe Modell nimmt nacheinander fünf **Denkmethoden**
ein (keine Berufe). Weniger unabhängig, aber deutlich besser als eine Antwort.

1. **Skeptiker** — „Warum scheitert das?" Risiken, Fehlannahmen, Schwachstellen.
2. **Grundsatz-Denker** — „Ist das überhaupt das richtige Problem?"
3. **Visionär** — „Welches Potenzial übersehen alle?"
4. **Außenstehender** — kein Vorwissen: unklare Begriffe, implizite Annahmen,
   blinde Flecken der Experten.
5. **Macher** — „Was mache ich Montagmorgen konkret?"

Danach **Meta-Kritik**: Welche Argumentation war am stärksten? Welche Rolle
hatte den größten blinden Fleck? Was haben alle gemeinsam übersehen? — Diese
Selbstkritik ist der wertvollste Teil.

## Output (Chairman-Synthese)
- Wo besteht Einigkeit?
- Wo gibt es echten Widerspruch?
- Was wurde fast vergessen?
- Empfehlung (kein Mittelwert, sondern gewichtet)
- Erster konkreter Schritt

## Gotchas
- Rollen-Simulation in EINEM Modell ≠ echte Diversität — alle Antworten
  stammen aus demselben Wissens-/Denkraum. Für die stärkste Wirkung echte
  unabhängige Agents/Modelle nutzen.
- „Was haben alle übersehen?" ist die ergiebigste Frage — nicht weglassen.
- Anonymisieren im Peer Review, sonst bewertet das Modell Marken statt Inhalte.
- Der Mensch bleibt fachlicher Entscheider; die Synthese ist Entscheidungshilfe.

Paart sich mit [[landing-and-site-builder]] als Entscheidungs-Gate vor dem Bauen.
