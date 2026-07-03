---
name: accessibility-action-plan
description: Formt aus priorisierten Findings einen konkreten, umsetzbaren Maßnahmenplan mit Prioritäts- und Aufwandseinordnung. Nutzen, wenn aus einem Audit ein Umsetzungsplan werden soll.
---

# Accessibility Action Plan

Macht aus Findings einen umsetzbaren Plan: geclustert, priorisiert nach Impact × Aufwand, Quick Wins zuerst.

## Wann verwenden
Wenn aus einem Audit ein konkreter Umsetzungsplan werden soll. Für die kundenfreundliche Report-Übersicht → `accessibility-report-summary`. Fachliche Fix-Details → `accessibility-audit`.

## Input
- Findings mit Schweregrad
- Optional: technische Rahmenbedingungen (Stack, Komponentenstruktur)

## Vorgehen
1. Findings nach Thema clustern (eine Kontrast-Korrektur deckt oft viele Instanzen ab).
2. Je Cluster Impact (Nutzerauswirkung) und Aufwand grob einschätzen.
3. Nach Impact × Aufwand sortieren — hoher Nutzen bei geringem Aufwand zuerst (Quick Wins).
4. Abhängigkeiten benennen (z. B. „Fokus-Styles erst nach Design-Token-Anpassung").

## Output
Maßnahmentabelle:

| Maßnahme | Betroffene Bereiche | Priorität | Aufwand | Nutzen |
|---|---|---|---|---|
| Kontraste in Buttons/Links anheben | Global, alle Templates | Hoch | Mittel | Bessere Lesbarkeit für sehbeeinträchtigte Nutzer |
| Formularfelder mit Labels verknüpfen | Kontakt, Checkout | Hoch | Niedrig | Bedienbarkeit per Screenreader |
| Fokus-Indikatoren ergänzen | Global | Mittel | Niedrig | Tastaturnavigation nachvollziehbar |

Darunter kurz: **Quick Wins zuerst** und offene **Abhängigkeiten**.

## Gotchas
- Aufwand nur grob schätzen (Niedrig/Mittel/Hoch) — keine Stunden-/Preiszusagen ohne Grundlage.
- Abhängigkeiten explizit machen, sonst wird in falscher Reihenfolge gearbeitet.
- Nicht jedes Finding einzeln listen — clustern, sonst wird der Plan unlesbar.
- Manuell zu prüfende Punkte kennzeichnen, nicht als „erledigt automatisch" behandeln.

## Bevorzugte Formulierungen
- „Es gibt Hinweise auf Barrieren."
- „Die Prüfung zeigt Auffälligkeiten bei …"
- „Eine manuelle Prüfung sollte das ergänzen."
- „Aus technischer Sicht besteht Handlungsbedarf."

## Nicht verwenden
- „nicht barrierefrei" (absolut), „gesetzeswidrig", „abmahngefährdet" (außer ausdrücklich als allgemeines Risiko eingeordnet)
- absolute Aussagen ohne Prüfung, Schuldzuweisungen, Panikmache, übertriebenes Marketing
