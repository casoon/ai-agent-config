---
name: web-design-workflow
description: Creative-Director-Prozess für individuelles Webdesign — Strategie → Designsystem → Layout → Inhalte → Code, statt sofort HTML zu erzeugen. Erzwingt Markenanalyse, 3–5 bewusst unterschiedliche Designkonzepte und ein fertiges Designsystem VOR dem ersten Layout. Nutzen bei neuer Website/Relaunch, wenn das Ergebnis nach Marke aussieht, nicht nach Template. NICHT für kleine Einzelseiten/Copy-only (→ landing-and-site-builder) oder reine Ästhetik-Fragen (→ frontend-design).
---

# Web-Design-Workflow

Führe wie ein Creative Director durch den Prozess — Schritt für Schritt, nicht sofort HTML.

## Kernproblem
„Entwickle ein modernes Webdesign" erzeugt fast immer das **statistische Durchschnitts-Internet**: Hero + Überschrift + Button + 3 Features + Testimonials + FAQ + Footer; oder Cards, viel Weißraum, leichtes Blau, Border-Radius, Schatten. Hübsch, aber keine Marke — weil der KI **Strategie** fehlt (Marke, Zielgruppe, Wettbewerb, Inhalt, Conversion-Ziel, Stil, spätere Contentmenge).

**Reihenfolge umdrehen:** nicht *Design → Inhalt*, sondern **Strategie → Designsystem → Layout → Inhalte → Feinheiten**. Code zuletzt.

## Die 10 Phasen

| # | Phase | Ergebnis |
|---|---|---|
| 1 | Unternehmen analysieren | Markenprofil (Branche, Premium/günstig, regional/international, emotional/sachlich, innovativ/konservativ, B2B/B2C) |
| 2 | Zielgruppe definieren | Persona + Nutzungsszenarien (Alter, Vorwissen, Entscheidungsdauer, mobil/Desktop, Vertrauen/Preis/Qualität) |
| 3 | Wettbewerb analysieren | Differenzierungsmerkmale (was gefällt/nicht, wovon abgrenzen) |
| 4 | Contentumfang bestimmen | Inhaltsarchitektur + Prioritäten (welche Seiten, wie viel Text, Bilder vorhanden?) |
| 5 | Designrichtung wählen | passender Stil → [[design-directions]] |
| 6 | Designsystem entwickeln | Farben, Typografie, Grid, Komponenten, Bildsprache |
| 7 | Wireframes erstellen | Seitenlayouts mit **Platzhaltern** und verschiedenen Content-Dichten |
| 8 | Design bewerten | Markenwirkung, Barrierefreiheit, Responsivität, SEO, Lesbarkeit, Skalierbarkeit |
| 9 | Inhalte generieren | Texte, Bilder, Illustrationen — passend zum System |
| 10 | Code generieren | Umsetzung des **freigegebenen** Designs |

## Kern-Erweiterung: erst Konzepte, dann Ausarbeitung
Nach Phase 5 **nicht sofort ein Designsystem** bauen. Zuerst **3–5 bewusst unterschiedliche Designkonzepte** entwerfen, die sich in **Markenwirkung, Typografie, Bildsprache und Layoutphilosophie** klar unterscheiden — nicht 5× dieselbe Variante. Dann wählt der Mensch **ein** Konzept; erst danach Designsystem → Wireframes → Inhalte → Code. Das ist die Arbeitsweise professioneller UX-/Branding-Agenturen und verhindert das Standardlayout. Für die Konzept-Auswahl/-Bewertung → [[llm-council]] (unabhängige Perspektiven statt erster Idee).

## Verzahnung
- **Phase 1–2 (Marke/Stimme):** [[brand-voice-dna]] extrahiert die funktionale Markenstimme aus Bestandstexten.
- **Phase 5 (Stil):** [[design-directions]].
- **Phase 6 (Designsystem):** [[ui-design]] (Hierarchie/CTA-Stufen/Micro-Details), [[tailwind-ui]] (Tokens), [[motion-design]], [[darkmode]]; ästhetische Richtung + Anti-Template-Disziplin → [[frontend-design]].
- **Phase 8 (Bewertung):** [[accessibility-audit]], [[seo]] (+ [[local-business-seo]] regional), [[web-performance]].
- **Phase 9 (Inhalte):** [[landingpage-from-briefing]], [[anti-ai-copy]], [[content-clarity-a11y-check]].
- **Phase 10 (Bau):** [[landing-and-site-builder]] übernimmt die Umsetzung im Vertical-Slice-Loop. Für Claude-design-Handoff dessen Modus B nutzen.

## Gotchas
- **Nicht mit Code/HTML starten.** Wer in Phase 1 schon Markup erzeugt, hat das statistische Template schon gewählt.
- **Wireframes mit Platzhaltern**, nicht mit echtem Content — echter Content erst Phase 9, wenn Marke/Schrift/Bildsprache stehen.
- **Konzepte müssen sich wirklich unterscheiden** — sonst ist die „Auswahl" eine Scheinwahl.
- **Der Mensch entscheidet** Richtung und Konzept; die KI liefert begründete Optionen, keine Vorab-Festlegung.
- Jede Phase liefert ein **freigegebenes Artefakt**, bevor die nächste startet (Markenprofil → Persona → … → Designsystem). Kein Überspringen nach vorn.
