---
name: conversation-retrospective
description: Prüft eine oder mehrere vergangene Sessions auf wiederkehrende Reibung und Korrekturen und wandelt jedes Muster in eine konkrete System-Verbesserung (neuer/erweiterter Skill, Memory-Eintrag, Guardrail). Nutzen für Retrospektiven ("was lief schief", "welche Skills fehlen", "Loop straffen", "System smarter machen"). NICHT für inhaltliche Zusammenfassungen einer Session oder einmalige Task-Komplexität.
---

# Conversation Retrospective

Reflexions-Loop, der die Skill-Sammlung SELBST verbessert. Ziel ist kein Vibe-Recap,
sondern: Stellen finden, an denen der Agent zu viel Nachfragen brauchte, eine
Nutzer-Vorgabe verletzte oder den passenden Skill/das Tool nicht hatte — und daraus
das kleinste Delta ableiten, das denselben Fehler nächste Woche verhindert.

## Zwei Leitprinzipien (nicht verhandelbar)

- **Korrekturen in ausführbare Regeln wandeln, nicht "sei vorsichtiger".** Eine
  Maßnahme, die sich nicht als Trigger, Checkliste, Skript oder triggerbarer Skill
  formulieren lässt, ist keine Maßnahme.
- **Dieselbe Korrektur zweimal = System-Anforderung, kein Zufall.** Ein einzelner
  Ausrutscher wird NICHT zur Systemänderung. Erst Wiederholung oder hohe Schwere
  rechtfertigt ein Delta.

## Delta-Typen

Jeder Reibungspunkt wird auf genau einen Typ gemappt:

- **Fehlender Workflow-Skill** — der Nutzer musste denselben Modus, dieselbe
  Sequenz, Branch-/Test-/Review-Policy wiederholt vorgeben.
- **Fehlender Domain-Skill** — der Nutzer korrigierte Fakten, Doku,
  Projektkonventionen oder Architektur-Annahmen.
- **Fehlendes Tool/Skript** — der Agent machte wiederholt mechanische Arbeit von
  Hand, die deterministisch sein sollte.
- **Fehlender Guardrail** — Dateien während Exploration angefasst, "nicht"-Vorgabe
  ignoriert, überbaut, falscher Root, benannte Dateien nicht zuerst gelesen.
- **Memory-Update nötig** — eine dauerhafte Nutzer-Präferenz, die getragen statt
  wieder entdeckt werden soll (siehe MEMORY.md Auto-Memory).

## Ablauf

1. **Fenster setzen.** Session(s) festlegen: die aktuelle, die letzten N, oder ein
   Datumsbereich. Ohne Angabe: die aktuelle Session plus die letzten paar.
2. **Reibung sammeln.** Session(s) durchgehen und Reibungspunkte notieren:
   Korrekturen, Rückfrage-Schleifen, verletzte Vorgaben, wiederholte Handarbeit,
   falsche Annahmen. Beleg (Turn/Zitat) je Punkt festhalten — Evidenz, keine
   Vermutung.
3. **Mappen.** Je Punkt: Delta-Typ + eine konkrete, überprüfbare Maßnahme
   (neuer/erweiterter Skill, Memory-Eintrag, Guardrail). Nicht "besser aufpassen".
4. **Filtern & priorisieren.** Einzelfälle streichen — nur wiederkehrende Muster
   (oder hohe Schwere) behalten. Nach eingespartem Aufwand / Häufigkeit ordnen.

## Output

Knappe Liste, ein Eintrag je Muster:

```
Reibung → Delta-Typ → konkrete Maßnahme
```

Beispiel:

```
Nutzer musste 3× "nicht committen" nachschieben
  → Fehlender Guardrail
  → Trigger in Workflow-Skill: bei Skill-Erstellung nie automatisch committen
```

Danach die Maßnahmen dorthin verzahnen, wo sie umgesetzt werden:

- **Skill-Lücken** (neuer/erweiterter Skill) → an `skill-creator` (Erstellung/Eval)
  bzw. `skill-authoring` (Konventionen, Ablageort).
- **Memory-Deltas** (dauerhafte Präferenz) → in die Auto-Memory (MEMORY.md +
  passende Notiz-Datei).

## Gotchas

- **Nur Zusammenfassen ist Fehlschlag.** Output MUSS das System verbessern, nicht
  die Session nacherzählen.
- **Einmalige Task-Komplexität ≠ fehlender Skill.** Wiederholung oder Schwere ist
  Pflicht, sonst kein Delta.
- **Jede Maßnahme muss ausführbar und überprüfbar sein.** Kein "sei vorsichtiger",
  kein "mehr testen" — sondern Trigger, Checkliste, Skript oder Skill mit
  Auslösebedingung.
- **Verletzte Nutzer-Vorgaben sind erstklassige Retro-Items**, nicht Randnotizen.
```
