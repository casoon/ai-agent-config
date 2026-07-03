---
name: client-email-after-audit
description: Generiert eine Kunden-E-Mail nach einem Accessibility-Audit — sachlich, lösungsorientiert, ohne Panikmache. Nutzen, wenn Audit-Ergebnisse per E-Mail an den Kunden gehen.
---

# Client E-Mail after Audit

Formuliert die Kunden-Mail, die ein Audit begleitet: sachlicher Kernbefund, klarer nächster Schritt, ein Call-to-Action.

## Wann verwenden
Wenn Audit-Ergebnisse per Mail an den Kunden gehen. Für die zugrunde liegende Zusammenfassung → `accessibility-report-summary`. Für die Entschärfung rechtlicher Formulierungen → `bfsg-risk-language-softener`.

## Input
- Kunde (Name, ggf. Anrede)
- Audit-Kurzergebnis
- Die größten 2–3 Punkte
- Nächster Schritt / Angebot
- Gewünschter Ton: eher technisch oder eher geschäftlich

## Vorgehen
1. Betreff knapp und sachlich formulieren.
2. Einstieg: Bezug herstellen, freundlich.
3. Was geprüft wurde (Umfang in einem Satz).
4. Kernergebnis sachlich — 2–3 Punkte, keine Finding-Flut.
5. Empfohlener nächster Schritt + Gesprächsangebot.

## Output
```
Betreff: <sachlich, z. B. „Ergebnisse der Barrierefreiheits-Prüfung Ihrer Website">

Hallo <Name>,

<Einstieg / Bezug>

wir haben <Umfang> geprüft. <1 Satz zum Grundtenor>

Die wichtigsten Punkte:
- <Punkt 1>
- <Punkt 2>
- <Punkt 3>

<Empfohlener nächster Schritt>

<Gesprächsangebot / CTA>

Viele Grüße
<Absender>
```

Bei Bedarf zwei Varianten: **technisch** (konkrete Maßnahmen) vs. **geschäftlich** (Nutzen/Risiko im Vordergrund).

## Gotchas
- Nicht mit Findings überladen — max. 2–3 Punkte, Details gehören in Report/Anhang.
- Genau ein klarer Call-to-Action, nicht drei konkurrierende.
- Keine Panikmache, kein Rechtsdruck; Risiko nur sachlich und allgemein benennen.
- Anrede/Ton an bestehende Kundenbeziehung anpassen (Du/Sie).

## Bevorzugte Formulierungen
- „Es gibt Hinweise auf Barrieren."
- „Die Prüfung zeigt Auffälligkeiten bei …"
- „Eine manuelle Prüfung sollte das ergänzen."
- „Aus technischer Sicht besteht Handlungsbedarf."

## Nicht verwenden
- „nicht barrierefrei" (absolut), „gesetzeswidrig", „abmahngefährdet" (außer ausdrücklich als allgemeines Risiko eingeordnet)
- absolute Aussagen ohne Prüfung, Schuldzuweisungen, Panikmache, übertriebenes Marketing
