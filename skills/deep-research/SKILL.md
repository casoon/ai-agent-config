---
name: deep-research
description: Mehrquellen-Rechercheverfahren — Fan-out-Websuche, Quellen abrufen, Behauptungen adversarial verifizieren, zitierten Report synthetisieren. Nutzen für tiefe, faktengeprüfte Recherche (Markt, Wettbewerb, Technik, Thought-Leadership, Whitepaper). NICHT für einfache Faktenfragen, schnelle Lookups oder Themen-Monitoring (dafür topic-radar).
---

# Deep Research

Kein einzelner Such-Prompt, sondern ein Verfahren gegen die zwei Schwächen von
LLM-Recherche: **halluzinierte Zitate** (~40% Fehlerrate, wenn aus dem Gedächtnis
generiert) und **einseitige Synthese** (die erste plausible Erzählung setzt sich
durch). Breit suchen → tief nachfassen → adversarial verifizieren → zitiert
synthetisieren.

## Vorab: Frage schärfen
Ist die Frage unterspezifiziert (fehlt Scope, Zeitraum, Region, Zweck), **erst
2–3 Rückfragen**, dann recherchieren. Eine vage Frage produziert vage Treffer.

## Phase 1 — Breite
4–6 **parallele Such-Winkel** mit unterschiedlichen Formulierungen und Quelltypen
(Doku, News, Primärquellen, Gegenpositionen). In Claude Code via `Agent`-Tool
(parallele Sucher) oder `Workflow` (mehrstufige Pipeline); Werkzeuge: WebSearch,
WebFetch. Jeder Winkel ist blind für die anderen — verhindert Tunnelblick.

## Phase 2 — Tiefe + Sättigungs-Stopp
Follow-ups aus dem **in Runde 1 gelernten Vokabular/den Zitaten** ziehen (nicht
aus der Ausgangsfrage). **Stopp-Heuristik: aufhören, wenn >80% der Treffer schon
bekannt sind** — Sättigung, nicht eine feste Rundenzahl. Verhindert endloses
Weitersuchen genauso wie vorzeitiges Abbrechen.

## Fakten-Rigor (nicht verhandelbar)
- **Nie aus dem Gedächtnis zitieren.** Jede Quelle abrufen.
- **2-Quellen-Regel** für belastbare Aussagen.
- **VALIDATE:** prüfen, dass die Quelle den Claim **wirklich stützt** — nicht nur,
  dass die Quelle existiert. Der häufigste Fehler: Zitat passt thematisch, belegt
  die Aussage aber nicht.
- Unbelegtes explizit als `[QUELLE FEHLT]` markieren, nicht glätten.

## Adversariale Verifikation (Blind-Judge)
Strittige Claims durch mehrere **unabhängige** Prüfer/Winkel gegenchecken. Bei der
Bewertung: **randomisierte/anonyme Labels** (Quelle A/B, nicht „laut Anbieter X") —
sonst Marken-/Reihenfolge-Bias. **Konservativer Tiebreak:** bei Gleichstand
gewinnt der Status quo / die bestehende Annahme, nicht die neuere Behauptung. Für
Entscheidungen mit echten Zielkonflikten → [[llm-council]].

## Iteration richtig einsetzen (Gotcha)
Welche Verfeinerungsstrategie taugt, hängt von Modell-Tier × Aufgabe ab:
- **Critique-and-revise** für konkrete Aufgaben: ein Pass benennt NUR Schwächen,
  ein separater Pass adressiert **genau diese** („fix these", nicht „mach's besser").
- **Warnung:** Selbst-Refinement ohne konkrete Kritikpunkte driftet — das Modell
  halluziniert Probleme, Scope kriecht, Qualität sinkt (Sycophancy). Immer an
  benannten Punkten entlang.

## Synthese
Zitierter Report, **entlang der Frage** strukturiert (nicht entlang der
Rohtreffer). Widersprüche zwischen Quellen **offen benennen**, nicht zu einer
glatten Erzählung mitteln. Konfidenz kennzeichnen, wo Belege dünn sind.

## Verzahnung
- Belegte Fakten dauerhaft ablegen → [[knowledge-base]] (Provenance).
- Laufendes Quellen-Monitoring statt Einzelrecherche → [[topic-radar]].
- Ergebnis in Content überführen → [[seo-article-from-audit-data]],
  [[case-study-from-audit]].

## Gotchas
- Keine Behauptung ohne abgerufene Quelle; keine Zahl aus dem Gedächtnis.
- Sättigung als Stopp, nicht Rundenzahl.
- Bei Bewertung anonymisieren; bei Gleichstand konservativ.
- Contested offen lassen statt vorschnell auflösen.
- Frage vorab schärfen — der teuerste Fehler ist tiefe Recherche zur falschen Frage.
