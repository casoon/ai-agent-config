---
name: accessibility-report-summary
description: Erstellt aus technischen Audit-Rohdaten (Lighthouse, axe, Pa11y, auditmysite, manuelle Prüfung) eine verständliche Zusammenfassung für Endkunden. Nutzen, wenn ein ganzer Report/Scan kundenfreundlich zusammengefasst werden soll.
---

# Accessibility Report Summary

Fasst einen kompletten Scan oder Audit in eine kundengerechte Übersicht zusammen — gruppiert, priorisiert, ohne rohen Tool-Output.

## Wann verwenden
Für einen ganzen Report/Scan. Für ein einzelnes Finding → `accessibility-finding-explainer`. Für den Maßnahmenplan → `accessibility-action-plan`. Für die begleitende Kunden-Mail → `client-email-after-audit`.

## Input
- Audit-Rohdaten (Tool-Export oder Notizen)
- Geprüfter Umfang (welche Seiten/Templates)
- Zielgruppe des Reports (Geschäftsleitung vs. Technik)

## Vorgehen
1. Findings nach Thema gruppieren (z. B. Kontrast, Tastaturbedienung, Formulare, Struktur/Semantik).
2. Pro Gruppe die typische Nutzerauswirkung in einem Satz beschreiben.
3. Technische Details vereinfachen — Häufigkeit nennen statt jede Instanz auflisten.
4. Risiken sachlich einordnen, keine reine Tool-Wiedergabe.

## Output
```
## Kurzfazit
<2–3 Sätze: Gesamtbild und Grundtenor>

## Wichtigste Auffälligkeiten
- <Thema>: <Beschreibung + betroffene Nutzer + ungefährer Umfang>
- …

## Empfohlene Maßnahmen
- <Maßnahme je Thema, umsetzungsnah>

## Priorisierung
<Was zuerst und warum>
```

## Gotchas
- Findings gruppieren, nicht die Tool-Liste abtippen — 30 Kontrast-Meldungen sind ein Thema.
- Zielgruppe beachten: Geschäftsleitung will Fazit + Risiko, Technik will Details.
- Scores (z. B. Lighthouse) nur als Orientierung nennen, nicht als Note verkaufen — sie decken nur einen Teil ab.
- Automatische Tests finden nicht alles: auf ergänzende manuelle Prüfung hinweisen.

## Bevorzugte Formulierungen
- „Es gibt Hinweise auf Barrieren."
- „Die Prüfung zeigt Auffälligkeiten bei …"
- „Eine manuelle Prüfung sollte das ergänzen."
- „Aus technischer Sicht besteht Handlungsbedarf."

## Nicht verwenden
- „nicht barrierefrei" (absolut), „gesetzeswidrig", „abmahngefährdet" (außer ausdrücklich als allgemeines Risiko eingeordnet)
- absolute Aussagen ohne Prüfung, Schuldzuweisungen, Panikmache, übertriebenes Marketing
