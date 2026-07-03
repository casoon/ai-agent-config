---
name: handoff
description: Erzeugt am Ende einer Session einen kopierbaren Übergabe-Prompt, mit dem eine frische Session (leerer Kontext) nahtlos weitermacht. Nutzen, wenn eine Session übergeben oder der Kontext resettet werden soll, oder wenn man später/mit einem anderen Agenten weiterarbeiten will. NICHT für laufende Arbeit oder ein reines Ergebnis-Fazit — dafür ist der Recap-Schritt da.
---
# Handoff — Session-Übergabe

Baut EINEN kopierbaren Prompt, den eine neue Session mit leerem Kontext einfügt und direkt weiterarbeitet.

## Gotchas (zuerst lesen)
- **Keine Secrets in den Handoff.** Keine Tokens, Keys, `.env`-Werte, Passwörter, private URLs. Nur Pfade und Namen.
- **Kein Verlauf.** Kein Gesprächstranskript, keine Begründungs-Historie, keine Emotionen ("war zäh"). Nur der aktuelle Stand.
- **Selbst-tragend.** Keine Verweise auf "unser Gespräch oben" — die neue Session hat davon nichts.
- **Git-State ist die Wahrheit**, nicht das Gedächtnis. Immer gegen den Filesystem-Stand prüfen.
- **Proportional halten.** Quick-Fix → 10–15 Zeilen. Feature → 30–50. Nicht mehr als nötig.

## Einordnung
Passt in den Vertical-Slice-Workflow [[landing-and-site-builder]] direkt **nach dem Recap-Schritt (8)**: Recap erklärt, was gebaut wurde; Handoff verpackt den offenen Rest für die nächste Session. Vor einem geplanten Kontext-Reset oder Tool-Wechsel ausführen.

## Schritt 1 — Git-State einsammeln
```bash
git branch --show-current
git log --oneline -8
git status --short      # dirty files = was ist in Arbeit
git diff --stat
git stash list
```
Fokus auf die **dirty files**: sie sind der fragilste Teil der Übergabe. Jede uncommittete Datei mit einer kurzen Notiz nennen, was und warum geändert wurde. Bei großem Diff die Absicht zusammenfassen, nicht Zeilen listen.

## Schritt 2 — Session synthetisieren
Aus der Session herausziehen — knapp:
- **Ziel** — was soll am Ende erreicht sein (großes Bild).
- **Erledigt** — konkret: welche Dateien, welche Commits.
- **Offen** — was fehlt noch.
- **Nächster Schritt** — EINE unmissverständliche Anweisung, die sofort ausführbar ist (nicht "Refactor weitermachen", sondern "`src/parser.ts` auf `TokenStream` umstellen").
- **Stolpersteine** — bekannte Bugs, Unsicherheiten, was leicht schiefgeht.

## Schritt 3 — Übergabe-Prompt ausgeben
Alles in EINEN Markdown-Codeblock. Sektionen weglassen, die nicht gebraucht werden.

````markdown
```
Projekt: <name> — <ein Satz>
Pfad: <absoluter Pfad>
Branch: <branch>

## Ziel
<großes Bild>

## Erledigt
- <konkret: Dateien / Commits>

## Aktueller Stand
<sauber oder dirty? Fehlschlagende Tests?>
Dirty files:
- <pfad — was geändert und warum>

## Nächster Schritt
1. <sofort ausführbare Anweisung>
2. <danach>

## Kontext & Entscheidungen
- <Stack / Architektur, nicht offensichtlich; getroffene Entscheidungen mit Grund>

## Stolpersteine
- <was leicht schiefgeht>
```
````

## Output
- Prompt in einem fenced Codeblock — leicht kopierbar.
- Uncommittete Änderungen **außerhalb** des Blocks als Warnung erwähnen, damit die neue Session sie nicht verwirft oder doppelt.
- Optional: `pbcopy` oder Speichern nach `.handoff.md` vorschlagen.
