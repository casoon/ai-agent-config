---
name: semantic-html-improver
description: Ersetzt div/span-Suppe durch semantisch korrektes HTML (Landmarks, Überschriftenhierarchie, native Elemente). Nutzen, wenn Markup semantisch verbessert werden soll.
---
# Semantic-HTML-Improver

Ersetzt bedeutungsloses `<div>`/`<span>`-Markup durch semantisch korrekte Elemente: Landmarks, saubere Überschriftenhierarchie, native Steuerelemente.

## Wann verwenden
- Markup ist funktional, aber semantisch arm (`<div>`-Suppe, `<span>` als Button).
- Screenreader-Navigation oder Landmark-Struktur soll verbessert werden.

## Input
- Das zu verbessernde Markup (oder Pfad).
- Optional: welche Rolle jeder Block auf der Seite hat.

## Prüf-Vorgehen
1. Rolle jedes Blocks bestimmen: Navigation? Hauptinhalt? Nebeninfo? Fußzeile? Klickbar?
2. Passendes natives Element wählen:
   - `<header>` / `<nav>` / `<main>` / `<aside>` / `<footer>` für Landmarks.
   - `<button>` für Aktionen, `<a href>` für Navigation.
   - `<ul>`/`<ol>`/`<li>` für Listen, `<figure>`/`<figcaption>` für Medien.
3. Überschriftenhierarchie prüfen: genau eine `<h1>` pro Seite, keine Ebene überspringen.
4. Ergebnis als Vorher/Nachher-Snippet zeigen.

Beispiel:
```html
<!-- vorher -->
<div class="nav"><div class="item" onclick="go()">Start</div></div>
<!-- nachher -->
<nav aria-label="Hauptnavigation"><a href="/">Start</a></nav>
```

## Output
Je Änderung:
- **Problem:** was semantisch fehlt.
- **Ort:** Element/Zeile.
- **Fix:** Vorher/Nachher-Snippet.
- **Priorität:** hoch / mittel / niedrig.

## Gotchas
- Genau eine `<h1>` pro Seite; Ebenen nicht überspringen (h2 → h4 ist falsch).
- Mehrere `<nav>`/`<section>` brauchen `aria-label`/`aria-labelledby` zur Unterscheidung.
- `<section>` ohne zugängliche Beschriftung ist kein Landmark — dann besser `<div>`.
- Nicht alles zu `<article>` machen: nur eigenständig sinnvolle Inhalte.
- `<main>` genau einmal pro Seite.
