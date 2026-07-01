---
name: image-to-webp
description: Use when converting PNG/JPG images to WebP for web deployment — covers dimension limits by use-case, quality settings, batch conversion, reference updates in Astro files, and cleanup of originals.
---

# Image → WebP Conversion

## Dimension presets

| Use case | Max width | Notes |
|---|---|---|
| Content / beside-text | 1200px | Standard für Seiten-Bilder |
| Team / Portrait | 800px | Quadratische Darstellung, 800 reicht |
| Hero / full-bleed | 1920px | Nur wenn wirklich vollflächig |
| Wide content | 1600px | Gruppenfotos, Panoramas |

## Quality

- **85** — Standard für Fotos (gutes Verhältnis, keine sichtbaren Artefakte)
- **90** — Wenn Kunde auf Schärfe besteht
- **75** — Logos/Grafiken mit Flächen (artefakte weniger sichtbar)

## Workflow

1. Dimensionen der Quell-Bilder prüfen: `python3 -c "from PIL import Image; ..."`
2. Konvertieren mit `scripts/convert.py`
3. Referenzen in `.astro`-Dateien aktualisieren (grep → sed)
4. Original-PNGs löschen

## Gotchas

- Pillow muss installiert sein: `pip3 install Pillow` — auf macOS meist vorhanden
- `method=6` in Pillow = langsamste aber beste WebP-Kompression — vertretbar für einmalige Konvertierung
- PNG mit Transparenz (RGBA): erst in RGB konvertieren, sonst WebP-Fehler: `img.convert('RGB').save(...)`
- Nach dem Löschen der PNGs: git-tracked PNGs brauchen `git rm`, untracked einfach `rm`

## Script
