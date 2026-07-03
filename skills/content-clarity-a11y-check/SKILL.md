---
name: content-clarity-a11y-check
description: Prüft Website-Texte auf Verständlichkeit und Barrierefreiheit (Sprache, Struktur, Linktexte, Lesbarkeit). Nutzen beim Review von Inhaltstexten.
---
# Content-Clarity-a11y-Check

Prüft Inhaltstexte auf Verständlichkeit und textliche Barrierefreiheit: Sprache, Struktur, Linktexte, Lesbarkeit.

## Wann verwenden
- Website-/Seiten-Texte sollen auf Klarheit und Zugänglichkeit geprüft werden.
- Nicht für Markup/Code — dafür die anderen Review-Skills.

## Input
- Der zu prüfende Text (oder Seiten-Pfad), idealerweise mit Überschriftenstruktur.

## Prüf-Vorgehen
1. Verständliche Sprache: kurze Sätze, aktive Formulierung, Fachjargon nur mit Erklärung.
2. Linktexte aussagekräftig — kein „hier klicken" / „mehr". Der Linktext muss allein sagen, wohin er führt.
3. Überschriftenstruktur logisch und ohne übersprungene Ebenen (h1 → h2 → h3).
4. Abkürzungen/Akronyme beim ersten Auftreten ausschreiben oder erklären.
5. Lesbarkeit: Absätze nicht zu lang, Aufzählungen wo sinnvoll.

## Prosa-Qualität (ergänzend zur Verständlichkeit)
- **Satzlängen-Varianz:** nicht alle Sätze gleich lang — ein kurzer Satz nach langen setzt Betonung.
- **Konkret vor abstrakt:** Substantive und Beispiele statt Abstrakta („lädt in 0,8 s" statt „performant").
- **Modifikator-Diät:** Adjektiv-/Adverb-Stapel kürzen; ein präzises Wort schlägt drei vage.
- **Struktur vor Prosa-Politur:** erst Reihenfolge/Funktion der Absätze prüfen, dann Sätze feilen — poliere nie eine Passage, die du danach streichst.

## Output
Je Finding:
- **Problem:** was die Verständlichkeit/Zugänglichkeit einschränkt.
- **Ort:** Textstelle/Abschnitt.
- **Vorschlag:** konkrete Umformulierung.
- **Priorität:** hoch / mittel / niedrig.

## Gotchas
- Linktexte werden von Screenreadern oft aus dem Kontext gerissen vorgelesen (Linkliste) — sie müssen für sich allein funktionieren.
- Mehrere „hier klicken"-Links auf einer Seite sind nicht unterscheidbar.
- Übersprungene Überschriftenebenen brechen die Screenreader-Navigation.
- Lange Schachtelsätze sind eine Barriere, nicht nur ein Stilproblem.

## Bevorzugte Formulierungen
- „Es gibt Hinweise auf Barrieren."
- „Die Prüfung zeigt Auffälligkeiten bei …"
- „Eine manuelle Prüfung sollte das ergänzen."

## Nicht verwenden
- absolute Aussagen ohne Prüfung, Panikmache, Schuldzuweisungen.
