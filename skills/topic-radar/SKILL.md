---
name: topic-radar
description: Scannt periodisch eine kuratierte Quellen-Liste (Wettbewerber-Blogs, WCAG/BFSG-News, Astro-/Cloudflare-Releases, Branchen-Feeds), filtert Neues nach Relevanz + Aktualität und liefert gerankte Content-Chancen. Nutzen für Blog-Themenfindung und um [[linkedin-post-from-content]] / [[newsletter-from-audit]] zu speisen. NICHT für eine einmalige, gezielte Recherche zu einem Thema — dafür [[deep-research]].
---
# Topic-Radar
Läuft in Claude Code über WebFetch + RSS/Atom — kein externes Binary. Holt Feeds, dedupliziert gegen einen persistenten Seen-Store, filtert hart und mappt jedes Item auf eine konkrete Content-Aktion.

## Gotchas (zuerst lesen)
- **Seen-Store liegt AUSSERHALB des Skill-Ordners** (`~/.casoon-agent-data/topic-radar/seen.json`), sonst löscht ein Skill-Update den State. Gesehene Items nie doppelt melden — vor dem Ranking gegen den Store prüfen und neue IDs sofort nachtragen.
- **Rauschen hart filtern.** Nicht jede Release-Note ist ein Post. Patch-Releases, Marketing-Wiederholungen, Off-Topic raus.
- **Feed-Etikette:** sequenziell holen, nicht parallel hämmern; `If-Modified-Since`/ETag respektieren; bei 429/Fehler überspringen, nicht retry-spammen.
- **Jedes Item muss auf eine konkrete Content-Aktion mappen** (welcher Skill speist es), sonst weglassen — auch wenn es „interessant" ist.

## Quellen-Konfiguration
Liste in `~/.casoon-agent-data/topic-radar/sources.json` (URL + Kategorie + Gewicht):
```json
[
  { "url": "https://astro.build/rss.xml",        "category": "astro",      "weight": 3 },
  { "url": "https://blog.cloudflare.com/rss/",    "category": "cloudflare", "weight": 3 },
  { "url": "https://www.w3.org/blog/news/feed",   "category": "wcag-bfsg",  "weight": 5 },
  { "url": "https://competitor.example/blog/feed", "category": "wettbewerb", "weight": 2 }
]
```
Kategorien: `astro`, `cloudflare`, `wcag-bfsg`, `wettbewerb`, `branche`. Gewicht 1–5 (höher = wichtiger für uns).

## Vorgehen
1. `sources.json` und `seen.json` laden.
2. Jeden Feed per WebFetch holen (RSS/Atom), Einträge parsen (Titel, Link, Datum, Zusammenfassung).
3. **Deduplizieren:** Item-ID (GUID oder Link) gegen `seen.json` prüfen; Bekanntes verwerfen.
4. **Filtern nach Aktualität:** älter als ~30 Tage raus (außer WCAG/BFSG-Grundsätzliches).
5. **Relevanz bewerten:** Quellen-Gewicht × Themen-Passung (Astro/Cloudflare/BFSG/Agentur-Themen). Rauschen fällt hier.
6. Für **nicht-Feed-Quellen** (Newsseiten ohne Feed, Gesetzestexte, Konkurrenz ohne RSS): kein Scraping-Gebastel — auf [[deep-research]] für gezielte Recherche verweisen.
7. Überlebende Items ranken und jedem eine Content-Aktion zuordnen.
8. Neue Item-IDs in `seen.json` schreiben.

## Output
Gerankte Liste neuer Items:
```
[1] BFSG-Übergangsfrist für Kleinunternehmen präzisiert  (wcag-bfsg, Score 15)
    Quelle: w3.org · 2026-06-28
    Warum relevant: betrifft Beratungs-Positionierung direkt.
    → speist: [[newsletter-from-audit]] + Blog-Thema

[2] Astro 6.2: neue Content-Loader-API                    (astro, Score 9)
    Quelle: astro.build · 2026-06-25
    Warum relevant: Stack-Update, das wir aktiv nutzen.
    → speist: [[linkedin-post-from-content]]
```

## Nicht verwenden
- Für eine tiefe, einmalige Recherche zu genau einem Thema → [[deep-research]].
- Als Feed-Reader ohne Content-Ziel — Items ohne konkrete Aktion gehören nicht in den Output.
