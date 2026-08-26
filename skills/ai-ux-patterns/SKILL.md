---
name: ai-ux-patterns
description: UX-Patterns für KI-/Assistenz-Interfaces — Prompt-UI, Chat-Interfaces, KI als Assistenz vs. Automat, Explainable-AI-Elemente, adaptive/personalisierte Interfaces, konversationelle UX. Nutzen beim Design von Chat-, Prompt- oder Assistenz-Features. NICHT für allgemeine UX-Zustände (→ ux-patterns) oder visuelle Gestaltung von Chat-UI-Komponenten (→ ui-design).
---

# AI/Assistenz UX Patterns

## Prompt-UI
- Warum: Ein leeres Eingabefeld ohne Führung überfordert — Nutzer wissen selten, was ein System leisten kann.
- Umsetzung: Platzhalter-Beispiele/Vorschläge ("Prompt-Chips") statt leerem Feld, sichtbarer Kontext-Hinweis wenn relevant (Zeichenlimit, Dateianhänge).
- Typische Fehler: Freitextfeld ohne jede Beispielführung bei komplexen/fachspezifischen Prompts; Absenden ohne erkennbaren "läuft"-Zustand.

## Chat-Interfaces
- Warum: etabliertes Mentalmodell (Messenger), aber KI-Antworten verhalten sich anders als Mensch-Nachrichten — Streaming, mögliche Fehler, Quellen.
- Umsetzung: Streaming-Text mit sichtbarem "wird generiert"-Indikator statt Warten auf Komplettantwort; klare Trennung Nutzer- vs. KI-Nachricht auch ohne Farbcode (z. B. für Screenreader); Stop-Button während Generierung.
- Typische Fehler: kein Weg, eine laufende Antwort abzubrechen; History ohne Möglichkeit, einzelne Nachrichten zu referenzieren/zu zitieren.

## KI als Assistenz vs. Automat
- Warum: Vertrauen hängt davon ab, ob Nutzer verstehen, ob die KI vorschlägt oder direkt handelt.
- Umsetzung: bei folgenreichen Aktionen (Löschen, Senden, Kaufen) immer Vorschlag + explizite Bestätigung, nicht automatische Ausführung. Bei reversiblen/geringfügigen Aktionen kann Automatisierung ohne Bestätigung sinnvoll sein — Schwelle: Wie teuer ist ein falsches Ergebnis rückgängig zu machen?
- Typische Fehler: Automat-Verhalten ohne Ankündigung ("KI hat X für dich erledigt" im Nachhinein statt vorher gefragt).

## Explainable-AI-Elemente
- Warum: "Warum diese Antwort/Empfehlung?" ist die häufigste Vertrauensfrage bei KI-Output.
- Umsetzung: Quellenangaben bei faktenbasierten Antworten (RAG-Zitate), sichtbare Konfidenz nur wenn sie tatsächlich kalibriert ist (sonst weglassen — falsche Sicherheit ist schlimmer als keine Angabe), kurze Begründung bei Empfehlungen/Scores statt reiner Zahl.
- Typische Fehler: Konfidenz-Prozentzahl ohne echte Kalibrierung anzeigen (täuscht Präzision vor); Black-Box-Ergebnis ohne jeden Anhaltspunkt, wie es zustande kam.

## Adaptive/personalisierte Interfaces
- Warum: KI-Systeme können sich an Nutzerverhalten anpassen — das ist Chance und Risiko zugleich (Unvorhersehbarkeit).
- Umsetzung: Änderungen am Interface durch Personalisierung sichtbar/erklärbar machen ("Für dich sortiert, weil…"), Rückweg zu neutraler/Standard-Ansicht immer verfügbar.
- Typische Fehler: Interface verändert sich unbemerkt zwischen Sessions — Nutzer verliert Orientierung, weil er nicht weiß, dass Personalisierung die Ursache ist.

## Konversationelle UX
- Warum: Ton und Fehlerverhalten eines Chat-Interfaces prägen die Wahrnehmung des ganzen Produkts stärker als bei klassischer UI.
- Umsetzung: Fehler/Nicht-Verstehen ehrlich kommunizieren ("Das konnte ich nicht sicher beantworten") statt zu halluzinieren oder auszuweichen; Ton konsistent mit der Marken-Voice halten, nicht generisch-freundlich für sich stehend.
- Typische Fehler: KI antwortet mit übertriebener Sicherheit auf Fragen außerhalb ihres Wissens/ihrer Daten.

## Gotchas
- Diese Patterns ergänzen [[ux-patterns]] um KI-spezifische Zustände — allgemeine Lade-/Fehlerzustände gelten weiterhin.
- Visuelle Umsetzung von Chat-Bubbles, Streaming-Cursor etc. folgt [[ui-design]]/[[motion-design]], nicht diesem Skill.
- "Assistenz vs. Automat"-Entscheidung ist die wichtigste Weiche im ganzen Feature — bei Unsicherheit immer Richtung Bestätigung, nicht Richtung Automatisierung.
