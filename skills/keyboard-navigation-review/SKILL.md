---
name: keyboard-navigation-review
description: Prüft Tastaturbedienbarkeit: Fokusreihenfolge, sichtbarer Fokus, Tastatur-Fallen, vollständige Bedienung ohne Maus. Nutzen, wenn Keyboard-Access geprüft werden soll.
---
# Keyboard-Navigation-Review

Prüft, ob eine Komponente/Seite vollständig und nachvollziehbar per Tastatur bedienbar ist.

## Wann verwenden
- Interaktive UI (Menüs, Modals, Tabs, Dropdowns, Formulare) soll auf Tastaturzugang geprüft werden.

## Input
- Komponenten-Code oder Seite (Pfad).
- Optional: erwartete Bedien-Flows.

## Prüf-Vorgehen
1. Alle interaktiven Elemente per Tab erreichbar und in visueller Reihenfolge?
2. Sichtbarer Fokus: `:focus-visible`-Style vorhanden, kein `outline:none` ohne gleichwertigen Ersatz.
3. Kein positiver `tabindex` (`tabindex="1+"` zerstört die Reihenfolge). Erlaubt: `0` und `-1`.
4. Keine Tastatur-Falle: Fokus lässt sich immer weiterbewegen (v.a. iframes, Custom-Widgets).
5. Modals/Overlays: Focus-Trap aktiv, ESC schließt, Fokus kehrt danach zum Auslöser zurück.
6. Custom-Widgets: erwartete Tasten implementiert (Enter/Space bei Buttons, Pfeiltasten bei Menü/Tabs).
7. Kein Fokusverlust nach Interaktion (z.B. Element entfernt → Fokus fällt auf `<body>`).

## Output
Je Finding:
- **Problem:** was per Tastatur nicht geht.
- **Ort:** Element/Interaktion.
- **Fix:** Snippet (Handler, `tabindex`, Focus-Management).
- **Priorität:** hoch (nicht bedienbar) / mittel / niedrig.

## Gotchas
- `outline:none` ohne Ersatz ist der häufigste Fehler — Fokus wird unsichtbar.
- `div`/`span` als Button: braucht `role`, `tabindex="0"` UND Key-Handler für Enter und Space.
- Nach Schließen eines Modals muss der Fokus zurückgesetzt werden, sonst springt er an den Seitenanfang.
- Positiver `tabindex` gewinnt gegen DOM-Reihenfolge — verwirrend und fehleranfällig.
- Hover-only-Interaktionen sind per Tastatur nicht erreichbar.
