---
name: component-doc-writer
description: Schreibt Nutzungs-, Props- und Accessibility-Dokumentation für eine Komponente. Nutzen, wenn eine Komponente dokumentiert werden soll.
---
# Component-Doc-Writer

Schreibt kompakte Komponenten-Doku: Zweck, Props, Verwendung, Accessibility-Hinweise, Varianten.

## Wann verwenden
- Eine Komponente (`.astro`, `.tsx`, `.svelte`) soll dokumentiert werden.
- Vorhandene Doku soll um Props/a11y ergänzt werden.

## Input
- Komponenten-Code (oder Pfad), inkl. Props/Signatur.

## Prüf-Vorgehen
1. Zweck aus Code/Verwendung ableiten (1–2 Sätze, kein Marketing).
2. Props aus Signatur/`interface`/`Astro.props` extrahieren.
3. Mindestens ein copy-paste-fähiges Verwendungsbeispiel bauen.
4. a11y-Anforderungen ableiten: braucht die Komponente ein Label? Verwaltet sie Fokus? Erwartet sie `alt`?
5. Varianten/Zustände auflisten (Größen, Farb-/Disabled-/Loading-States).

## Output
Markdown mit Struktur:
- **Zweck**
- **Props** — Tabelle: Name / Typ / Default / Pflicht / Beschreibung.
- **Verwendung** — lauffähiges Beispiel.
- **Accessibility** — was der Aufrufer sicherstellen muss (z.B. „braucht sichtbares Label oder `aria-label`").
- **Varianten** — Liste mit Kurzbeschreibung.

## Gotchas
- a11y-Verantwortung explizit dokumentieren: was muss der Aufrufer liefern (Label, `alt`, eindeutige `id`)?
- Beispiele müssen ohne Anpassung lauffähig sein — echte Prop-Namen, keine Platzhalter wie `...`.
- Defaults aus dem Code lesen, nicht raten.
- Pflicht-Props deutlich kennzeichnen; fehlende führen sonst zu stillen Fehlern.
