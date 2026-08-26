---
name: visual-trends
description: Aktuelle visuelle UI-Trend-Stilmittel — Glassmorphism, Neomorphism, Gradient-Systeme, Icon-Systeme, Illustration vs. Fotografie, Bento-Grids — mit Einsatzkriterien und Fallstricken. Ergänzt die festen Regeln aus ui-design um dosiert einsetzbare Trend-Stilmittel. Nutzen bei der visuellen Gestaltung einzelner Komponenten/Sections. NICHT für die Kernregeln zu Spacing/Typografie/Farbsystem (→ ui-design) und NICHT für die grundsätzliche Stilrichtung einer ganzen Seite (→ design-directions/frontend-design).
---

# Visuelle Trend-Stilmittel

Diese Stilmittel sind **Werkzeuge, kein Zwang** — nur einsetzen, wenn sie die gewählte Design-Richtung ([[design-directions]]) stützen. Wahllos kombiniert wirken sie wie ein Trend-Sampler statt wie ein System.

## Glassmorphism
- Merkmale: transluzenter Hintergrund (`backdrop-filter: blur()`), dünner heller Rand, leichte Transparenz.
- Passend für: Overlays, Nav-Bars über Bewegtbild/Bild, Karten über komplexem Hintergrund.
- Fallstricke: Performance (blur ist teuer, sparsam einsetzen), Kontrast/Lesbarkeit von Text auf variablem Untergrund — immer gegen den worst-case Hintergrund prüfen, nicht nur gegen die Mockup-Farbe.
- Nicht einsetzen: auf reinem Solid-Hintergrund (Effekt unsichtbar/sinnlos) oder bei WCAG-kritischem Fließtext.

## Neomorphism
- Merkmale: weiche Schatten nach innen/außen aus derselben Grundfarbe, wirkt "geprägt".
- Passend für: einzelne Akzent-Controls (Toggle, Slider) in reduzierten, farbarmen Interfaces.
- Fallstricke: sehr kontrastarm → Accessibility-Risiko, skaliert nicht auf ganze Interfaces, wirkt schnell datiert (Trend-Peak war 2020).
- Empfehlung: höchstens punktuell, nie als flächendeckendes System.

## Gradient-Systeme
- Merkmale: definierte Verlaufs-Tokens statt Ad-hoc-Gradients pro Komponente.
- Passend für: Hero-Hintergründe, Akzent-Flächen, Branding-Elemente (Buttons, Badges).
- Fallstricke: zu viele unterschiedliche Gradients im selben View wirken beliebig; Text auf Gradient braucht Kontrastprüfung an der dunkelsten UND hellsten Stelle des Verlaufs.
- Umsetzung: 2–3 definierte Gradient-Tokens (`--gradient-hero`, `--gradient-accent`), nicht pro Komponente neu erfinden.

## Icon-Systeme
- Merkmale: ein Icon-Set, eine Stroke-Width, eine Größe pro Kontext.
- Fallstricke: Mischen von Icon-Sets (unterschiedliche Stroke-Width/Ecken-Radius fällt sofort auf), Icons ohne Text bei nicht selbsterklärenden Aktionen.
- Umsetzung: ein Icon-Set projektweit festlegen, Icon-only-Buttons brauchen `aria-label` + sichtbaren Tooltip bei Bedarf, Mindest-Hit-Area 40×40px (siehe [[ui-design]]).

## Illustration vs. Fotografie
- Illustration passt zu: erklärbedürftigen/abstrakten Themen (SaaS, Prozesse), jüngeren/verspielten Marken, konsistentem Stil über viele Assets hinweg (Foto-Sets sind teurer konsistent zu halten).
- Fotografie passt zu: Vertrauensaufbau (Personen, echte Umgebungen), B2B/seriösen Marken, Case Studies/Referenzen.
- Fallstricke: Stockfoto-Ästhetik (generische Hände-am-Laptop-Bilder) untergräbt Glaubwürdigkeit stärker als gar kein Bild; Illustrationsstil wechselt zwischen Seiten.

## Bento-Grids
- Merkmale: asymmetrisches Grid aus unterschiedlich großen Kacheln, jede Kachel ein Inhalts-Häppchen.
- Passend für: Feature-Übersichten, Dashboards, "Was wir bieten"-Sections mit ungleich wichtigen Punkten.
- Fallstricke: Kachelgrößen ohne Bedeutung gewählt (Größe sollte Wichtigkeit/Inhaltsmenge widerspiegeln, nicht nur Layout-Ästhetik); auf Mobile bricht das Grid oft in eine Spalte — dort geht die visuelle Hierarchie verloren, wenn sie nur über Kachelgröße transportiert wurde.

## Gotchas
- Trend-Stilmittel verfallen — vor Einsatz prüfen, ob es zur gewählten [[design-directions]] passt oder nur "gerade überall zu sehen" ist.
- Die Kernregeln aus [[ui-design]] (Kontrast, Spacing, Hierarchie) gelten weiter, egal welches Stilmittel obendrauf kommt.
- Nicht mehr als 1–2 Trend-Stilmittel pro Seite kombinieren — sonst wirkt es wie ein Showcase, nicht wie ein Produkt.
