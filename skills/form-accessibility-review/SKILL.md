---
name: form-accessibility-review
description: Prüft Formulare auf Labels, Fehlermeldungen und Validierung und macht die Validierung barriereärmer. Nutzen beim Review von Formularen und Eingabefeldern.
---
# Form-Accessibility-Review

Prüft Formulare auf zugängliche Beschriftung, Fehlerbehandlung und Validierung — und macht die Validierung barriereärmer.

## Wann verwenden
- Ein Formular oder einzelne Eingabefelder sollen geprüft werden.
- Validierungs-/Fehlerlogik soll barriereärmer werden.

## Input
- Formular-Markup (oder Pfad) inkl. Validierungslogik.

## Prüf-Vorgehen
1. Jedes Feld hat ein `<label for>` passend zur `id` (oder umschließt das Feld). Kein Feld nur mit Placeholder.
2. Pflichtfelder: `required` und (bei Bedarf) `aria-required="true"`, sichtbar als Text markiert (nicht nur `*` ohne Erklärung).
3. Fehler: Meldung textlich, mit `aria-describedby` am Feld verknüpft, Container `role="alert"` oder `aria-live`.
4. Fehlerzustand nicht nur über Farbe — Text/Icon ergänzen, `aria-invalid="true"` am Feld.
5. `autocomplete`-Attribute für Standardfelder (Name, E-Mail, Adresse) gesetzt.
6. Zusammengehörige Felder (Radios, Adressblöcke) in `<fieldset>` mit `<legend>`.
7. Fokus springt bei Fehler-Submit zum ersten fehlerhaften Feld.

## Output
Je Finding:
- **Problem:** fehlende Beschriftung/Fehlerkopplung/etc.
- **Ort:** Feld/Element.
- **Fix:** Snippet (`label`, `aria-describedby`, `role="alert"`).
- **Priorität:** hoch (Feld unbenutzbar/Fehler unbemerkt) / mittel / niedrig.

## Gotchas
- `placeholder` ist kein Label — er verschwindet bei Eingabe und hat oft schlechten Kontrast.
- Fehler nur in Rot ist für viele Nutzer unsichtbar; immer Text ergänzen.
- Fehlermeldung ohne `aria-describedby`/`role="alert"` wird vom Screenreader nicht angesagt.
- `aria-required` ersetzt nicht `required` (Validierung), sondern ergänzt es semantisch.
