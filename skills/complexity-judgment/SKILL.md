---
name: complexity-judgment
description: Gegengewicht zu reinen Minimal-Code-/YAGNI-Regeln (eigenes CLAUDE.md, Ponytail-artige "so wenig Code wie möglich"-Skills) — wann eine Zeile mehr, eine Abstraktion, oder mehr Sorgfalt tatsächlich richtig ist. Nutzen als kurze Gegenfrage VOR dem Schreiben stark komprimierten/minimalen Codes, bei Refactoring-Entscheidungen, oder wenn eine "kürzer ist besser"-Regel im Einzelfall falsch wirkt. NICHT als Rechtfertigung für Over-Engineering oder spekulative Abstraktion ohne konkreten, genannten Bedarf — Minimalismus bleibt der Default, dieser Skill ist die Ausnahme-Prüfung davor.
---

# Complexity Judgment

## Gotcha zuerst
Minimal-Code-Regeln sind ein guter Default, aber ein Hook oder eine Leiter, die bei jedem Prompt gleich feuert, kennt den Einzelfall nicht. Dieser Skill ersetzt den Default nicht — er ist die kurze Gegenfrage, bevor eine Kompression tatsächlich umgesetzt wird. Nur wenn eine der vier Achsen unten klar zutrifft, gegen den Minimal-Default gehen; sonst bleibt Minimal richtig.

## Die vier Prüf-Achsen

### 1. Lesbarkeit ≠ Zeilenzahl
Ein Ein-Zeiler ist nicht automatisch klarer als drei Zeilen. Test: Kann jemand die Zeile in unter 5 Sekunden ohne Nachdenken lesen? Verschachtelte Ternaries, Method-Chains über mehrere Zwecke hinweg, dichte Regex ohne Kommentar — typische Fälle, in denen „eine Zeile" gegen „verständlich" verliert. Regel: **kürzer gewinnt nur, wenn es genauso klar bleibt** — sonst gewinnt klar.

### 2. Rule of Three (Abstraktions-Timing)
YAGNI heißt: keine Abstraktion vor Bedarf. Aber „Bedarf" heißt nicht „erster Anwendungsfall". Faustregel: **beim ersten Duplikat kopieren, beim dritten Vorkommen abstrahieren.** Vor dem dritten Vorkommen abstrahieren ist spekulativ. Danach nicht abstrahieren erzeugt versteckte Dopplung, die sich bei jeder fachlichen Änderung an mehreren Stellen fortpflanzt (Shotgun-Surgery-Geruch: eine Änderung erzwingt Edits an mehr als zwei Stellen).

### 3. Reversibilität der Entscheidung
Zwei-Wege-Tür (leicht rückgängig zu machen: interne Hilfsfunktion, Formatierung, lokale Variable) vs. Ein-Wege-Tür (schwer rückgängig: öffentliche API, Datenmodell/Migration, Security-Boundary, Dateiformat). Bei Ein-Wege-Türen mehr Sorgfalt und Struktur rechtfertigen, auch wenn es mehr Zeilen kostet — der Preis eines späteren Umbaus übersteigt den Preis der zusätzlichen Zeilen jetzt.

### 4. Erweiterung ist bereits angekündigt, nicht nur vorstellbar
YAGNI gilt für erfundene Zukunft. Kündigt der User im selben Auftrag schon eine zweite oder dritte Variante an („das brauchen wir gleich auch für Y"), ist das kein spekulatives Bauen mehr, sondern ein bekannter, naher Bedarf — dafür zu strukturieren ist kein Over-Engineering.

## Checkliste vor dem Komprimieren
- [ ] Bleibt die Lesbarkeit gleich oder besser? Wenn nein: nicht komprimieren.
- [ ] Ist das die 1. oder 2. Duplizierung? Dann kopieren, nicht abstrahieren.
- [ ] Ist das die 3.+ Duplizierung? Dann abstrahieren, nicht weiter kopieren.
- [ ] Ist die Entscheidung eine Ein-Wege-Tür (API/Datenmodell/Security)? Dann mehr Sorgfalt, nicht das Minimum.
- [ ] Hat der User eine nahe Erweiterung explizit angekündigt? Dann dafür bauen, nicht ignorieren.

## Verhältnis zu bestehenden Regeln
- Ersetzt NICHT den Minimal-Default aus dem globalen CLAUDE.md — ist die Ausnahme-Prüfung davor, kein Freifahrtschein.
- `/simplify` und `/code-review` prüfen NACH dem Schreiben auf Vereinfachungspotenzial — dieser Skill wirkt VOR dem Schreiben, als Gegenfrage zur Kompression.
- Kein Ponytail-Nachbau — keine Leiter, kein Hook-Zwang, keine Metrik-Jagd auf LOC-Reduktion.

## Nicht verwenden
- Als Rechtfertigung für spekulative Architektur ohne konkreten, genannten Bedarf.
- Bei trivialem, offensichtlich einmaligem Code — da bleibt der Minimal-Default richtig.
- Wenn der User explizit „so kurz wie möglich" oder einen Ponytail-artigen Modus verlangt — dann gilt dessen Vorgabe.
