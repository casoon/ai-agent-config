---
name: design-systems
description: Design-System-Grundlagen — Token-Architektur (Farbe/Spacing/Typografie als benannte Variablen), Komponentenbibliotheken strukturieren, Variable Themes, responsive Component-Patterns. Nutzen beim Aufbau oder der Erweiterung eines Design-Tokens-Sets bzw. einer Komponentenbibliothek. Für die konkrete Dark-Mode-Implementierung siehe darkmode, für Animations-Tokens siehe motion-design, für die 7 UI-Kernregeln siehe ui-design.
---

# Design-System-Grundlagen

## Token-Architektur — drei Ebenen

| Ebene | Beispiel | Zweck |
|---|---|---|
| **Primitive** | `--blue-500: oklch(...)` | Rohwerte, nie direkt in Komponenten referenzieren |
| **Semantic** | `--color-accent: var(--blue-500)` | Bedeutung statt Farbe — das wird in Komponenten benutzt |
| **Component** | `--button-bg: var(--color-accent)` | Optional, nur wenn eine Komponente vom Semantic-Token abweichen muss |

Warum drei Ebenen: Ein Rebrush (Primitives ändern sich) bricht nichts, weil Komponenten nie direkt auf Primitives zeigen. Ein Theme-Wechsel (Semantic ändert sich) reicht für die meisten Fälle.

## Typische Fehler
- Komponenten referenzieren Primitives direkt (`bg-blue-500` statt `bg-accent`) → ein Themewechsel erfordert Suchen-und-Ersetzen über die ganze Codebase.
- Zu viele Semantic-Tokens ("Inflation") — jedes neue Feature bekommt einen eigenen Token statt bestehende wiederzuverwenden. Vor jedem neuen Token prüfen: passt ein bestehender?
- Tokens ohne Namenskonvention (`--blue`, `--primaryColor`, `--btn-color` gemischt) — eine Konvention projektweit durchziehen (z. B. `--{category}-{role}-{variant}`).

## Komponentenbibliothek strukturieren
- Atomic-Ansatz nur so weit treiben, wie er echten Wiederverwendungsnutzen bringt — eine "Atom/Molekül/Organismus"-Taxonomie als Ordnerstruktur ist bei kleinen Projekten oft mehr Overhead als Nutzen.
- Pragmatischer Standard: `primitives/` (Button, Input, Badge — keine Business-Logik) vs. `patterns/` (ComposedCard, FormGroup — kombinieren Primitives) vs. `sections/` (Hero, Pricing — seitenspezifisch, nicht wiederverwendet).
- Jede Primitive-Komponente exponiert Varianten über Props (`variant="primary"|"secondary"`), nicht über Klassennamen, die von außen zusammengesetzt werden — sonst entstehen ungültige Kombinationen.

## Variable Themes
- Themes sind Sets von Semantic-Token-Werten, nicht eigene Komponentenversionen.
- Umsetzung über CSS Custom Properties + Klassen-/Attribut-Scope (`[data-theme="dark"]`, `.brand-b`), nicht über JS-Runtime-Style-Injection.
- Ein Theme-Wechsel darf nie Primitive-Tokens anfassen müssen — sonst ist die Trennung aus dem Token-Modell oben nicht sauber.

## Responsive Component-Patterns
- Container Queries statt Media Queries für Komponenten, die in unterschiedlichen Kontexten (Sidebar vs. Hauptspalte) unterschiedlich breit sind — die Komponente kennt ihren eigenen Container, nicht den Viewport.
- Fluid Typography über `clamp()` statt fester Breakpoint-Sprünge, wo Werte kontinuierlich skalieren sollen.
- Komponenten-API bleibt über Breakpoints stabil — kein `MobileCard`/`DesktopCard`-Duplikat, stattdessen eine Komponente mit responsivem CSS.

## Gotchas
- Ein Design-System ist nur so gut wie seine Durchsetzung — ungenutzte Primitives ("keiner hält sich dran") sind ein Zeichen, dass die Tokens die echten Bedürfnisse nicht treffen, nicht dass Disziplin fehlt.
- Dark-Mode-spezifische Umsetzung (Toggle, FOUC-Vermeidung, Kontrastpaare) → [[darkmode]].
- Animations-/Timing-Tokens → [[motion-design]].
- Die inhaltlichen Farb-/Spacing-/Typografie-Regeln (60/30/10, 8px-Grid, Type-Scale) → [[ui-design]].
