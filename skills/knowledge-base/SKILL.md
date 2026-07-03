---
name: knowledge-base
description: Belegte, kompoundierende Wissensbasis für Kunden-/Domänenfakten (Projektfakten, wiederkehrende A11y-Muster, BFSG-Stand) als untereinander verlinkte Markdown-Seiten mit Quellen-Herkunft. Kompiliert Wissen einmal statt pro Query neu (RAG-Alternative). Nutzen, wenn Fakten aus Quellen dauerhaft abgelegt, verlinkt, gelintet oder abgefragt werden sollen, oder wenn Case-Study/FAQ/Artikel belegtes Projektwissen brauchen. NICHT für konversationelle Auto-Memory (MEMORY.md), einmalige Lookups oder flüchtige Notizen.
---

# Knowledge Base

Eine dauerhafte, kompoundierende Wissensbasis als untereinander verlinkte Markdown-Seiten.
Statt pro Query neu zu recherchieren (RAG), wird Wissen **einmal kompiliert** und aktuell
gehalten: Querverweise stehen schon da, Widersprüche sind schon markiert, jede Aussage
trägt ihre Herkunft.

Speist [[case-study-from-audit]], [[faq-from-issues]], [[seo-article-from-audit-data]].
Wird von [[deep-research]] befüllt.

## Gotchas (zuerst lesen)

- **Kein Fakt ohne Herkunft.** Jede Aussage trägt einen Quellen-Marker zurück auf `raw/`.
  Aussagen ohne belegbare Quelle gehören nicht in die Basis — raus damit oder als solche kennzeichnen.
- **Contested-Fakten markieren, nicht raten.** Widersprechen sich zwei Quellen, werden
  BEIDE Positionen mit Datum und Quelle notiert und `contested: true` gesetzt. Niemals
  stillschweigend auflösen oder überschreiben.
- **Lint vor Vertrauen.** Vor jeder Nutzung (Case Study, FAQ, Artikel) linten: Orphans,
  tote Links, `stale`-Inhalte, Widersprüche. Ungelintetes Wissen ist nicht belastbar.
- **Basis schlank halten.** Kein Wiki-Wildwuchs. Eine Seite entsteht nur für Fakten, die
  **mehrfach** gebraucht werden oder zentral für ein Projekt sind — nicht für Einmal-Details.

## Abgrenzung zur Auto-Memory

Das ist **Projektwissen** (belegt, verlinkt, geteilt), nicht die konversationelle
Auto-Memory (`MEMORY.md`). MEMORY.md hält flüchtige Session-Präferenzen und Korrekturen
des Agenten fest; die Knowledge Base hält belegte Kunden-/Domänenfakten mit Quellen-Herkunft.
Faustregel: braucht ein anderer Mensch/Agent das mit Beleg → Knowledge Base. Ist es eine
Verhaltensregel für mich → MEMORY.md.

## Drei Schichten

```
kb/
├── SCHEMA.md          # Konventionen, Tag-Taxonomie, Index-Regeln
├── index.md           # Katalog: eine Zeile pro Seite (Wikilink + Kurzfassung)
├── raw/               # Schicht 1: immutable Originalquellen (nie ändern)
│   ├── audits/        #   Audit-Exports, Scan-Rohdaten
│   ├── projects/      #   Projektnotizen, Briefings, Verträge
│   └── refs/          #   BFSG-/WCAG-Texte, externe Belege
├── projects/          # Schicht 2: Projektfakten je Kunde (agent-geschrieben)
├── patterns/          # Schicht 2: wiederkehrende A11y-Muster
└── compliance/        # Schicht 2: BFSG-/WCAG-Stand, Fristen
```

- **Schicht 1 (`raw/`):** unveränderliche Quellen. Der Agent liest, ändert nie. Korrekturen
  leben in Schicht 2.
- **Schicht 2 (Seiten):** agent-eigene MD-Seiten, untereinander per `[[wikilink]]` verlinkt.
- **Schicht 3 (`SCHEMA.md` + `index.md`):** Regeln und Katalog.

## Seiten-Frontmatter

```yaml
---
title: Kunde X — Formular-A11y
updated: YYYY-MM-DD
sources: [raw/audits/kunde-x-2026.md]     # Herkunft; Pflicht
confidence: high | medium | low            # wie gut belegt
contested: false                           # true bei ungelöstem Widerspruch
---
```

Im Fließtext trägt jede belegte Aussage einen Marker zurück auf die Quelle:
`… Kontrast lag bei 3.1:1 ^[raw/audits/kunde-x-2026.md]`.

## raw/-Frontmatter (Drift erkennen)

Jede Quelle in `raw/` bekommt einen kleinen Block, damit Re-Ingest Änderungen erkennt:

```yaml
---
source: https://…   oder  Herkunft/Empfänger
ingested: YYYY-MM-DD
sha256: <hex des Inhalts unter dem Frontmatter>
---
```

Bei Re-Ingest den `sha256` über den Body neu berechnen und vergleichen: identisch → nichts
tun; abweichend → Quelle hat sich geändert, abhängige Schicht-2-Seiten (via `sources:`)
neu prüfen und ggf. `updated` bumpen.

## Operationen

**Ingest** — Quelle nach `raw/` speichern (mit `sha256`), prüfen was schon existiert
(index.md + Suche), dann Schicht-2-Seiten schreiben/ergänzen: Herkunfts-Marker setzen,
mindestens 2 `[[wikilinks]]`, `confidence` ehrlich, Widersprüche → `contested: true` mit
beiden Positionen. index.md aktualisieren.

**Query** — index.md lesen, relevante Seiten lesen, Antwort synthetisieren und die genutzten
Seiten zitieren (`Laut [[kunde-x]] …`). Substanzielle Ergebnisse zurück in eine Seite ablegen.

**Lint (vor jeder Nutzung)** — prüfen und mit Pfaden berichten:
- Orphans (Seiten ohne eingehenden `[[wikilink]]`)
- tote Links (`[[…]]` zeigt auf nicht existierende Seite)
- fehlende Herkunft (Aussage/Seite ohne `sources:` bzw. `^[raw/…]`)
- `stale` (Seite älter als die jüngste sie betreffende Quelle)
- Widersprüche (alle `contested: true`)
- Source-Drift (`sha256` in `raw/` neu berechnen, Mismatches melden)
