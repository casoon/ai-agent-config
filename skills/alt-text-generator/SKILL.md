---
name: alt-text-generator
description: Erzeugt sachliche, kontextpassende Alt-Texte und erkennt dekorative Bilder (leeres alt). Nutzen, wenn Alt-Texte für Bilder gebraucht werden.
---
# Alt-Text-Generator

Erzeugt sachliche, kontextpassende Alt-Texte und erkennt dekorative Bilder, die `alt=""` bekommen.

## Wann verwenden
- Bilder brauchen `alt`-Texte oder vorhandene sollen geprüft werden.
- Entscheidung nötig, ob ein Bild informativ oder dekorativ ist.

## Input
- Bild (oder Beschreibung) plus Kontext: Wo steht es? Welche Funktion? Ist es ein Link/Button?

## Prüf-Vorgehen
1. Funktion klären: informativ, dekorativ, funktional (Link/Button) oder Text-im-Bild?
2. Dekorativ (rein schmückend, Info steht im Text daneben) → `alt=""`.
3. Informativ → beschreibe, was im Kontext relevant ist, knapp und sachlich.
4. Funktional (Bild in Link/Button) → beschreibe das Ziel/die Aktion, nicht das Bild.
5. Text-im-Bild → den Text 1:1 in `alt`.
6. Logo → Firmenname (in Link zur Startseite: Firmenname genügt).

## Output
Je Bild:
- **Ort:** Datei/Selektor.
- **Empfehlung:** `alt="…"` (oder `alt=""` bei dekorativ).
- **Begründung:** knapp, warum dieser Text.
- **Priorität:** hoch (funktional/informativ ohne alt) / niedrig (Feinschliff).

## Gotchas
- Kein „Bild von …" / „Grafik zeigt …" — Screenreader sagen die Rolle bereits an.
- Kontext entscheidet: dasselbe Bild braucht in Artikel und Teaser oft unterschiedliches `alt`.
- Fehlendes `alt` (Attribut ganz weg) ≠ `alt=""` — ohne Attribut liest der Screenreader oft den Dateinamen vor.
- Bei funktionalen Bildern beschreibt `alt` das Ziel, nicht das Motiv.
- Redundanz vermeiden: steht die Info schon als Fließtext daneben, ist das Bild oft dekorativ.
