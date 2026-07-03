---
name: landing-and-site-builder
description: End-to-end-Workflow, um eine Website oder Landingpage im Astro-Stack zu planen und zu bauen — oder als Design-Brief an Claude design zu übergeben. Orchestriert die vorhandenen Design-, Content-, SEO- und A11y-Skills über einen Vertical-Slice-Loop mit Council-Entscheidungs-Gate. Nutzen beim Start einer neuen Site/Landing, beim Umstrukturieren oder wenn aus einem Briefing eine gebaute Seite werden soll.
---

# Landing- & Site-Builder

Prozess-Skill: verwandelt ein Briefing in eine gebaute, geprüfte Seite — ohne
mit Code zu starten und ohne die erste Idee ungeprüft zu übernehmen. Er baut
nicht selbst alles, sondern **dirigiert** die Fach-Skills des Repos.

## Zwei Modi
- **A · In Claude Code bauen** — direkt im Astro-Projekt implementieren
  (Standard, wenn ein Repo existiert).
- **B · An Claude design übergeben** — statt zu implementieren einen
  Design-Brief + einen self-contained Prototyp erzeugen (eine HTML-Datei, CSS
  inline, keine externen Assets → lauffähig als Artifact / in Claude design).
  Danach das freigegebene Design nach Astro zurückportieren (Slice für Slice,
  s.u.). Frage zu Beginn, welcher Modus gewünscht ist.

## Vor dem Bauen: Council-Gate
Die strategischen Weichen NICHT aus dem Bauch stellen. Für **Positionierung,
Seitenstruktur und Design-Richtung** [[llm-council]] anwenden (unabhängige
Perspektiven → Kritik → Synthese). Verhindert, dass Layout und Copy die erste,
womöglich voreingenommene Idee zementieren. Ergebnis: eine begründete Richtung
+ erster Schritt.

## Der Workflow (Vertical-Slice-Loop)
Nicht horizontal (erst alle Layouts, dann aller Content). Sondern der kleinste
nutzbare Ausschnitt end-to-end, dann iterieren. Pro Slice:

1. **Brainstorming** — Was soll die Seite leisten? Ziel, Zielgruppe, eine
   gewünschte Aktion. Noch nicht bauen.
2. **Alignment** — Erst Rückfragen stellen, nicht raten: Angebot, Zielgruppe,
   Tonalität, Pflichtinhalte, rechtliche Grenzen, ein oder mehrere CTAs?
3. **Slice wählen** — kleinster nutzbarer Ausschnitt zuerst, z.B. Hero + ein
   CTA. Rest (Features, FAQ, Footer) bewusst später.
4. **Plan** — kleine, testbare Schritte für genau diesen Slice.
5. **Definition of Done** — Akzeptanzkriterien festlegen (Baseline unten).
6. **Implementieren** — NUR diesen Slice, kein Zusatz-Scope.
7. **Testen** — A11y, SEO, Visuell, Responsive (s. QA-Skills).
8. **Recap** — kurz erklären, was gebaut wurde und wo die Grenzen sind.
9. **Refactoring** — zuerst fragen „was können wir weglassen?", nicht nur
   „verbessern". Verhalten unverändert lassen.
10. **Commit** — atomar, temporäre Planungs-MDs wieder entfernen.

Danach nächster Slice (Problem/Lösung → Social Proof → FAQ → CTA-Wiederholung).

## Slice-Gates (Qualität pro Slice)
- **Approval-Gate im Alignment:** nach den Rückfragen eine klare Entscheidung
  einholen — ✅ Approve · 🔄 Revise · ❓ Clarify · ❌ Cancel. Erst bei ✅ bauen.
- **Zwei-Stufen-Review pro Slice** (stärker als ein DoD-Häkchen): erst
  **Spec-Compliance** (deckt der Build das Briefing? Kein Scope-Creep?), dann
  **Code-Qualität** — jeweils durch einen *frischen* Subagent (`Agent`-Tool).
  Grundsatz: **kein Agent prüft seine eigene Arbeit.** Ergänzt das Council-Gate
  um eine QA-Achse.

## Welchen Skill wann (Orchestrierung)
- **Struktur & Copy:** [[landingpage-from-briefing]] (Abschnitts-Copy),
  [[content-clarity-a11y-check]] (verständliche Texte, gute Linktexte).
- **Ästhetik & Richtung:** [[frontend-design]] (Richtung, nicht templated),
  [[ui-design]] (Hierarchie, Abstände, CTA-Stufen), [[tailwind-ui]] (v4-Setup),
  [[motion-design]] (Micro-Interactions), [[darkmode]].
- **Bau:** [[astro-architecture]] (Seiten/Layouts/Rendering),
  [[mdx-content]] (Content Collections), [[i18n]] (mehrsprachig),
  [[image-to-webp]] / [[web-performance]] (Bilder, CWV).
- **QA je Slice:** [[accessibility-audit]], [[seo]] (+ [[local-business-seo]]
  bei regionalen Seiten), [[playwright]] (E2E/axe), [[post-audit]] (Build-Audit).

## Landing vs. Website
- **Landing:** ein Ziel, ein primäres CTA, minimale/keine Navigation, eine
  Seite. Alles zahlt auf die eine Aktion ein.
- **Website:** mehrseitig, Navigation, Sitemap, wiederkehrende Layouts,
  interne Verlinkung. Council-Gate zusätzlich für die Informationsarchitektur.

## Definition of Done (Web-Baseline)
- **A11y:** semantisches HTML, Kontrast, Tastaturbedienung, Labels, ein `<h1>`,
  Fokus sichtbar (→ accessibility-audit).
- **SEO:** Title ≤ 60, Meta-Description ≤ 160 Zeichen, OG-Tags, Canonical,
  passendes JSON-LD, `lang` gesetzt (→ seo).
- **Performance:** responsive Bilder (WebP), keine Layout-Shifts, kein
  render-blockierender Ballast.
- **Klarheit:** ein erkennbares Ziel / CTA; Nutzen vor Features.

## Gotchas
- Nicht mit Implementierung starten — erst Brainstorming + Rückfragen.
- Ein Ziel pro Landing; mehrere CTAs verwässern die Conversion.
- Nutzen vor Features formulieren; konkrete statt generischer Claims.
- Weglassen vor Hinzufügen — Agents bauen tendenziell zu viel.
- Modus B: Prototyp strikt self-contained (Inline-CSS, Data-URIs), sonst läuft
  er in Claude design / als Artifact nicht.
- Temporäre Planungs-Markdown nach dem Commit wieder entfernen.
- Der Mensch bleibt fachlicher Entscheider.
