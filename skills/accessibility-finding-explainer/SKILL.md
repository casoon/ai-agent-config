---
name: accessibility-finding-explainer
description: Übersetzt ein einzelnes technisches Barrierefreiheits-Finding (axe, Lighthouse, Pa11y, manuelle WCAG-Prüfung) in sachliche, verständliche Kundensprache. Nutzen, wenn ein Finding kundengerecht mit Auswirkung, Maßnahme und Priorität erklärt werden soll.
---

# Accessibility Finding Explainer

Macht ein einzelnes technisches Finding für Kunden verständlich — mit konkreter Nutzerauswirkung und klarer Maßnahme, ohne Fachjargon und ohne Dramatisierung.

## Wann verwenden
Für ein einzelnes Finding. Für einen ganzen Report → `accessibility-report-summary`. Für einen Umsetzungsplan → `accessibility-action-plan`. Fachliche Fix-Details (ARIA, Kontrast, Fokus, Astro-Patterns) stehen in `accessibility-audit` — dort nachschlagen statt hier duplizieren.

## Input
- Das Finding (Tool-Ausgabe oder manuelle Notiz)
- Betroffene Seite / Komponente
- WCAG-Kriterium (nur falls tatsächlich belegt)
- Schweregrad
- Technischer Kontext (optional)

## Vorgehen
1. Kern des Findings erfassen: was genau fehlt/bricht.
2. Konkrete Nutzergruppe identifizieren (z. B. Screenreader-, Tastatur-, Sehbehinderte Nutzer).
3. Eine umsetzbare technische Maßnahme formulieren.
4. Priorität aus Schweregrad × Nutzerauswirkung ableiten.

## Output
Exakt diese Struktur:

```
### Problem
<Was ist auffällig — eine sachliche Beschreibung>

### Auswirkung
<Welche Nutzergruppen sind betroffen und wie konkret>

### Empfehlung
<Konkrete technische Maßnahme>

### Priorität
<Niedrig | Mittel | Hoch> — <kurze Begründung>
```

## Gotchas
- WCAG-Kriterium nur nennen, wenn es wirklich belegt ist — kein Rateraten der SC-Nummer.
- Nutzerauswirkung konkret machen („Tastatur-Nutzer erreichen den Button nicht"), nicht abstrakt („schlechte UX").
- Nicht dramatisieren: ein einzelnes Finding ist ein Hinweis, kein Weltuntergang.
- Priorität begründen, nicht nur vergeben.

## Bevorzugte Formulierungen
- „Es gibt Hinweise auf Barrieren."
- „Die Prüfung zeigt Auffälligkeiten bei …"
- „Eine manuelle Prüfung sollte das ergänzen."
- „Aus technischer Sicht besteht Handlungsbedarf."

## Nicht verwenden
- „nicht barrierefrei" (absolut), „gesetzeswidrig", „abmahngefährdet" (außer ausdrücklich als allgemeines Risiko eingeordnet)
- absolute Aussagen ohne Prüfung, Schuldzuweisungen, Panikmache, übertriebenes Marketing
