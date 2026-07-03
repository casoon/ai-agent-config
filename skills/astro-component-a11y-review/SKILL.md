---
name: astro-component-a11y-review
description: Prüft eine einzelne Astro-/React-/HTML-Komponente auf typische Barrierefreiheitsprobleme und liefert konkrete Fixes. Nutzen beim a11y-Review einer Komponente. Für WCAG-Patterns siehe accessibility-audit.
---
# Astro-Komponenten-a11y-Review

Prüft eine konkrete Komponente auf Barrierefreiheitsprobleme und liefert Findings mit Code-Fix. Die WCAG-Patterns selbst stehen im Skill `accessibility-audit` — hier geht es um das Prüf-Vorgehen und das Finding-Format.

## Wann verwenden
- Eine einzelne Komponente (`.astro`, `.tsx`, `.svelte`, HTML-Snippet) soll auf a11y geprüft werden.
- Nicht für ganze Seiten oder Tool-Output — dafür `content-clarity-a11y-check` bzw. `lighthouse-axe-result-explainer`.

## Input
- Der Komponenten-Code (oder Pfad).
- Optional: Kontext (wo eingesetzt, welche Props, interaktiv?).

## Prüf-Vorgehen
Pro interaktivem/strukturellem Block prüfen:
1. Semantisches Element genutzt? (`<button>`, `<a>`, `<nav>`, `<label>` statt `<div>`/`<span>`).
2. Bedienbar per Tastatur? Kein `div` mit `onclick` ohne Rolle + Key-Handler + `tabindex`.
3. Fokus sichtbar? `:focus-visible`-Style vorhanden, kein `outline:none` ohne Ersatz.
4. Zugängliche Beschriftung? Icon-only-Buttons/Links haben `aria-label`; Inputs haben `<label>`.
5. Kontrast plausibel? Text/Interaktion ≥ Schwellwert (Detail in accessibility-audit).
6. ARIA nur wenn nötig und korrekt? Kein redundantes/kaputtes ARIA (siehe `aria-usage-review`).
7. Touch-Target ≥ 44×44px bei klickbaren Elementen.
8. Bilder mit sinnvollem `alt` bzw. `alt=""` wenn dekorativ (siehe `alt-text-generator`).

## Output
Finding-Liste, je Finding:
- **Problem:** kurze Beschreibung.
- **Ort:** Zeile/Selektor/Element.
- **Fix:** konkretes Code-Snippet (vorher → nachher).
- **Priorität:** hoch (blockiert Nutzung) / mittel / niedrig.

## Gotchas
- Natives Element vor ARIA: `<button>` statt `<div role="button">` — bringt Fokus, Enter/Space und Rolle gratis.
- `div` mit `onclick` ist unsichtbar für Tastatur und Screenreader.
- Icon-only ohne `aria-label` ist für Screenreader leer.
- `placeholder` ersetzt kein `<label>`.
- `aria-label` überschreibt sichtbaren Text — nicht bei Elementen mit lesbarem Inhalt setzen.
