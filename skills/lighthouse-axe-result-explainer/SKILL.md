---
name: lighthouse-axe-result-explainer
description: Erklärt Lighthouse- und axe-Ergebnisse: was die Regel bedeutet, warum sie zählt, wie man sie behebt. Nutzen, wenn Tool-Output eingeordnet werden soll (intern/technisch).
---
# Lighthouse-/axe-Result-Explainer

Ordnet automatisierten a11y-Tool-Output ein: was eine Regel bedeutet, welche Nutzer betroffen sind, wie man sie behebt. Interner/technischer Blick.

## Wann verwenden
- Ein Lighthouse-Report oder axe-Ausgabe soll erklärt und priorisiert werden.
- Regel-IDs/Violations sollen in konkrete Fixes übersetzt werden.

## Input
- Tool-Output (Regel-IDs, betroffene Selektoren) oder Report-Pfad.

## Prüf-Vorgehen
Pro Violation/Audit:
1. Regel-ID auflösen (z.B. `color-contrast`, `image-alt`, `label`, `aria-*`).
2. Bedeutung: was prüft die Regel konkret?
3. Nutzerauswirkung: welche Nutzergruppe ist betroffen (Screenreader, Tastatur, Sehschwäche)?
4. Fix: konkretes Snippet für den betroffenen Selektor.
5. False-Positive-Check: kann die Meldung im Kontext harmlos/falsch sein? (z.B. Kontrast auf verdecktem Element).

## Output
Je Regel:
- **Regel + Ort:** ID + Selektor.
- **Bedeutung:** 1 Satz.
- **Auswirkung:** wer ist betroffen.
- **Fix:** Snippet.
- **Priorität:** hoch (Sperre) / mittel / niedrig / möglicher False Positive.

## Gotchas
- Automatisierte Tools finden nur ~30–40% der Barrieren — manuelle Prüfung bleibt nötig.
- Ein grüner Score ist kein Freibrief; `passed` ≠ barrierefrei.
- Kontrast-Meldungen sind oft False Positives bei Overlays/verdeckten/animierten Elementen.
- Gleiche Regel, mehrere Vorkommen: erst die Ursache im Muster/Component fixen, nicht jedes Vorkommen einzeln.
- Für tiefergehende E2E-Prüfung siehe `playwright` (axe-core), für Patterns `accessibility-audit`.
