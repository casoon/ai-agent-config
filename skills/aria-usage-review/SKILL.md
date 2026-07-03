---
name: aria-usage-review
description: Findet falsche oder überflüssige ARIA-Nutzung (redundante Roles, kaputte id-Referenzen, ARIA statt nativem Element) und korrigiert sie. Nutzen beim Review von ARIA-Attributen.
---
# ARIA-Usage-Review

Prüft ARIA-Attribute auf Fehler und Redundanz. Erste ARIA-Regel: **Kein ARIA ist besser als falsches ARIA.**

## Wann verwenden
- Code enthält `role`, `aria-*`-Attribute, die geprüft/aufgeräumt werden sollen.
- Custom-Widget mit ARIA soll validiert werden.

## Input
- Markup mit ARIA-Attributen (oder Pfad).

## Prüf-Vorgehen
1. ARIA statt nativem Element? `role="button"` auf `<div>` → durch `<button>` ersetzen.
2. Redundante Rollen entfernen: `role="navigation"` auf `<nav>`, `role="list"` auf `<ul>`, `role="button"` auf `<button>`.
3. Referenzen prüfen: jede `aria-labelledby`/`aria-describedby`/`aria-controls`-`id` muss existieren und eindeutig sein.
4. Zustände prüfen: `aria-expanded`/`aria-checked`/`aria-selected` werden bei Interaktion aktualisiert, nicht nur initial gesetzt.
5. Verbotene Kombinationen: `aria-hidden="true"` auf fokussierbaren Elementen; `role` widerspricht nativer Semantik.
6. `aria-label`/`aria-labelledby` nicht auf Elemente ohne unterstützte Rolle (z.B. `<div>` ohne Rolle).

## Output
Je Finding:
- **Problem:** falsches/überflüssiges ARIA.
- **Ort:** Element/Attribut.
- **Fix:** Snippet (Attribut entfernen oder natives Element).
- **Priorität:** hoch (kaputte Referenz/falsche Rolle) / mittel / niedrig (redundant).

## Gotchas
- Redundante Rollen sind nicht harmlos — sie können native Semantik verdecken.
- `aria-labelledby` mit fehlender `id` → Element bleibt unbeschriftet (fällt still aus).
- `role="presentation"`/`aria-hidden` entfernt Kinder aus dem Baum — nicht auf Container mit interaktivem Inhalt.
- `title` ist kein zuverlässiger Ersatz für `aria-label` (auf Touch/Keyboard unsichtbar).
