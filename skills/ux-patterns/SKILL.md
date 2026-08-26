---
name: ux-patterns
description: UX-Pattern-Bibliothek für Interaktionsdesign — Progressive Disclosure, Empty States, Onboarding-Flows, Microcopy, Lade-/Fehlerzustände, Navigation, User Flows. Mit Einsatzkriterien und typischen Fehlern pro Pattern. Nutzen bei Entscheidungen zu Interaktionsverhalten und UI-Zuständen. NICHT für visuelle Gestaltung (→ ui-design/frontend-design) oder Animation (→ motion-design).
---

# UX Patterns

Patterns für Interaktionsverhalten und UI-Zustände — nicht für Aussehen (dafür [[ui-design]]/[[frontend-design]]) oder Bewegung (dafür [[motion-design]]).

## Progressive Disclosure
- Warum: Reduziert kognitive Last, indem Komplexität erst bei Bedarf sichtbar wird.
- Wann: komplexe Formulare, Settings mit Advanced-Optionen, Erstnutzer-Flows.
- Typische Fehler: alles hinter einem "Mehr anzeigen" verstecken, das nie geöffnet wird; wichtige Pflichtfelder verstecken.
- Umsetzung: Standardansicht zeigt die 80%-Fälle, "Erweitert"/"Mehr Optionen" klappt den Rest auf, State bleibt nach Interaktion erhalten (kein Re-Collapse beim nächsten Render).

## Empty States
- Warum: Ein leerer Bildschirm ohne Erklärung wirkt wie ein Fehler, nicht wie ein Ausgangspunkt.
- Wann: erster Login, leere Listen/Suchergebnisse, nach Filterung ohne Treffer.
- Typische Fehler: nur "Keine Daten vorhanden" ohne Handlungsaufforderung; derselbe Empty State für "noch nie befüllt" und "gefiltert, 0 Treffer" — das sind unterschiedliche Situationen mit unterschiedlicher CTA.
- Umsetzung: kurzer Erklärtext + primäre Handlung (z. B. "Ersten Eintrag anlegen"), bei Filterung: "Filter zurücksetzen" statt Anlege-CTA.

## Onboarding-Flows
- Warum: Erste Minuten entscheiden über Aktivierung.
- Wann: neue Nutzer, neues Feature mit Erklärungsbedarf.
- Typische Fehler: Tour mit 8+ Tooltip-Schritten, die niemand zu Ende klickt; Onboarding blockiert die eigentliche Nutzung (Modal-Zwang).
- Umsetzung: aufgabenbasiert statt Tour-basiert — zeigen, was als Nächstes zu tun ist, nicht alles auf einmal erklären. Überspringen muss immer möglich sein.

## Microcopy
- Warum: Button-/Fehler-/Leerzustand-Texte sind die am häufigsten gelesenen Wörter im Produkt.
- Wann: überall — Buttons, Tooltips, Fehlermeldungen, Bestätigungen.
- Typische Fehler: generisches "Error occurred" / "Erfolgreich"; Button-Label beschreibt nicht die Handlung ("OK" statt "Löschen bestätigen").
- Umsetzung: Verb + Objekt im Button ("Änderungen speichern", nicht "Speichern"), Fehlermeldungen sagen was schiefging UND was zu tun ist.

## Ladezustände
- Warum: Wahrgenommene Geschwindigkeit ≠ tatsächliche Geschwindigkeit.
- Wann: jede asynchrone Operation über ~300ms.
- Typische Fehler: Spinner für Inhalte mit bekannter Struktur (Skeleton wäre passender); Layout-Sprung wenn Content nachlädt.
- Umsetzung: < 300ms kein Indikator nötig, 300ms–2s Skeleton/Spinner, > 2s zusätzlich Fortschritt/Kontext ("Wird generiert…"). Skeleton reserviert den finalen Platz, keine Layout-Shifts.

## Error States
- Warum: Fehler sind der Moment mit dem höchsten Frustrationspotenzial — hier entscheidet sich Vertrauen.
- Wann: Formularvalidierung, fehlgeschlagene Requests, 404/500.
- Typische Fehler: technische Fehlermeldung 1:1 durchreichen (Stacktrace/HTTP-Code an Endnutzer); Fehler ohne Recovery-Pfad.
- Umsetzung: menschliche Sprache, konkrete nächste Handlung ("Erneut versuchen", "Support kontaktieren"), Formularfehler inline am Feld, nicht nur als Sammel-Banner oben.

## Navigation vereinfachen
- Warum: Jede zusätzliche Ebene/Option erhöht Entscheidungsaufwand.
- Wann: IA-Entscheidungen, Hauptnavigation, Filter-/Kategorie-Strukturen.
- Typische Fehler: mehr als 7±2 Hauptpunkte; Navigation, die Systemstruktur statt Nutzerintention abbildet.
- Umsetzung: nach Nutzerzielen benennen, nicht nach internen Modulnamen; aktueller Standort immer erkennbar (Breadcrumb/aktiver State).

## User Flows optimieren
- Warum: Jeder zusätzliche Schritt kostet Konversion.
- Wann: Checkout, Signup, mehrstufige Formulare.
- Typische Fehler: Schritte addieren ohne zu prüfen ob sie zusammenlegbar sind; Fortschrittsanzeige fehlt bei mehr als zwei Schritten.
- Umsetzung: Schritte zählen und jeden rechtfertigen, Fortschrittsindikator bei Mehrschritt-Flows, Zurück-Navigation ohne Datenverlust.

## Gotchas
- Diese Patterns beschreiben **Verhalten und Zustände**, nicht Look — die visuelle Umsetzung folgt [[ui-design]] und [[frontend-design]], Übergänge zwischen Zuständen folgen [[motion-design]].
- Empty State und "0 Suchergebnisse" sind unterschiedliche States mit unterschiedlicher CTA — nicht zusammenlegen.
- Onboarding-Erfolg misst sich an Aktivierung, nicht an Tour-Abschluss-Rate.
