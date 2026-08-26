---
name: social-pulse
description: Recherchiert, was gerade öffentlich über ein Thema gesagt wird — Reddit, Hacker News, X/Twitter, YouTube, Foren, allgemeines Web — zeitlich eingegrenzt (Standard letzte 30 Tage). Nutzen für Sentiment-Checks, „was denkt die Community über X", Launch-/Release-Reaktionen, Wettbewerber-Buzz. NICHT für faktengeprüfte Tiefenrecherche (→ deep-research) oder periodisches Monitoring kuratierter Quellen (→ topic-radar).
---

# Social Pulse

Ad-hoc-Schnappschuss der öffentlichen Diskussion zu einem Thema in einem Zeitfenster — kein Dauer-Monitoring, kein Scraper-Unterbau. Läuft komplett über WebSearch/WebFetch.

## Gotcha zuerst
Das Vorbild für diesen Skill (last30days-skill) verlangt ein Dutzend optionale API-Keys — ScrapeCreators, Apify, X-Auth-Token/CT0, Bluesky-App-Passwort, TruthSocial-Token — für dedizierte Plattform-Scraper, plus eigene Node/Python-Toolchain. Für den normalen Fall ist das Overkill: WebSearch deckt Reddit/HN/YouTube/X-Diskussion über `site:`-Operatoren und die Suchmaschinen-Indexierung ausreichend ab, ohne Auth, ohne Wartung. Nur wenn eine Plattform nachweislich zu dünn indexiert ist (v. a. X ohne Login lückenhaft, YouTube-Kommentare ohne API unsichtbar), das als Lücke benennen statt sie stillschweigend zu füllen.

## Vorgehen
1. **Zeitfenster festlegen.** Standard 30 Tage; explizit übernehmen, wenn der User ein anderes nennt.
2. **Parallele Plattform-Suchen** (WebSearch, pro Plattform ein eigener, blinder Winkel — verhindert Tunnelblick):
   - `site:reddit.com <thema>` (+ Datum/Sortierung neu)
   - `site:news.ycombinator.com <thema>`
   - `site:x.com OR site:twitter.com <thema>`
   - `site:youtube.com <thema>` (nur Titel/Beschreibung — Kommentare sind ohne API nicht zugänglich)
   - allgemeines Web ohne site-Filter (News, Foren, Blogs)
3. **Pro Treffer:** Datum gegen das Zeitfenster prüfen (älter raus), Quelle mit WebFetch abrufen statt aus dem Suchschnipsel zu zitieren.
4. **Rauschen filtern:** Bots, Spam, reine Werbung, Duplikate raus. Nur Beiträge mit echtem Diskurs (Antworten, Upvotes, Zitate, Reaktionen) behalten.
5. **Synthese statt Liste:** Konsens vs. Kontroverse benennen, 5–10 repräsentative O-Töne mit Link/Datum zitieren, Stimmungsbild pro Plattform nur dann getrennt ausweisen, wenn es tatsächlich abweicht.

## Fakten-Rigor
Gleiche Grundregel wie [[deep-research]]: nie aus dem Gedächtnis zitieren, jede Quelle abrufen, die Aussage muss vom Post/Snippet wirklich getragen sein — nicht nur thematisch passen. Liefert eine Plattform keine Treffer im Zeitfenster, das explizit als `[KEIN SIGNAL]` markieren statt Stille als Zustimmung oder Desinteresse zu interpretieren.

## Output
Kurzes Stimmungsbild (2–4 Sätze) + 5–10 repräsentative Belegstellen mit Link/Datum, nach Plattform gruppiert, mit Konsens/Kontroverse-Einordnung am Ende. Kein Rohtreffer-Dump.

## Verzahnung
- Tiefe, faktengeprüfte Recherche zu einem Thema → [[deep-research]].
- Dauerhaftes Monitoring eigener kuratierter Quellen → [[topic-radar]].
- Ergebnis in Content überführen → [[linkedin-post-from-content]].

## Nicht verwenden
- Faktenrecherche/Whitepaper-Fragen ohne Sentiment-Bezug → [[deep-research]].
- Laufendes Feed-Monitoring eigener kuratierter Quellen → [[topic-radar]].
- Wenn Plattform-Zugriff nicht-öffentliche Inhalte braucht (private Communities, gelöschte/geschützte Posts) — dieser Skill deckt nur öffentlich indexierte Inhalte ab.
