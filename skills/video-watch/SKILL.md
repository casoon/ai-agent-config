---
name: video-watch
description: Lässt Claude ein Video tatsächlich sehen und hören — Frames extrahieren und Read()en, Transkript aus Captions oder Whisper-Fallback. Nutzen, wenn eine Frage sich auf ein konkretes Video/eine Aufnahme bezieht (URL oder lokale Datei) — Bug-Screen-Recording diagnostizieren, Video zusammenfassen, Hook/Struktur eines Konkurrenz-Videos analysieren, "was passiert bei Minute X". NICHT für reine Audio-Transkription ohne visuellen Bezug oder wenn ein Text-Transkript bereits vorliegt.
---

# Video Watch

Vereinfachter Nachbau von [bradautomates/claude-video](https://github.com/bradautomates/claude-video). Kernversprechen erhalten (Frames + Transkript an Claude, echtes Sehen+Hören statt Titel-Raten), Infrastruktur radikal reduziert.

## Gotcha zuerst
Das Original braucht ~12 optionale API-Keys (ScrapeCreators, Apify, X-Auth/CT0, Groq, OpenRouter, Perplexity, Parallel, Bluesky, TruthSocial …), drei Detail-Stufen mit Szenenerkennung und eine eigene Marketplace-Distribution. Dieser Nachbau deckt denselben Kernfall — Captions/Whisper-Transkript + budgetierte, deduplizierte Frames — mit **einem** Python-Skript ohne Fremdpakete ab, das nur `yt-dlp`, `ffmpeg`/`ffprobe` und optional `curl` + `OPENAI_API_KEY` braucht. Wer die Original-Plattformbreite (TikTok-Kommentare, X ohne Login, Xiaohongshu) wirklich braucht, ist beim Original besser aufgehoben — das hier ist bewusst der Kern, nicht der Vollausbau.

## Voraussetzungen
- `ffmpeg` + `ffprobe` immer nötig (`brew install ffmpeg` / `apt install ffmpeg`).
- `yt-dlp` nur für URLs, nicht für lokale Dateien (`brew install yt-dlp`).
- `OPENAI_API_KEY` optional — nur falls ein Video weder manuelle noch Auto-Captions hat und trotzdem ein Transkript gebraucht wird (Whisper-Fallback über die OpenAI-API, `whisper-1`). Ohne Key: Analyse rein visuell, Transkript-Sektion sagt das explizit.
- Das Skript prüft Abhängigkeiten selbst und bricht mit einer konkreten Install-Anweisung ab, statt etwas automatisch zu installieren.

## Vorgehen
1. **Aufrufen:**
   ```bash
   python3 scripts/watch.py "<url-oder-pfad>" [--start MM:SS] [--end MM:SS] [--no-frames]
   ```
   - URL: alles, was `yt-dlp` unterstützt (YouTube, Loom, TikTok, X, Instagram, Vimeo, …).
   - Lokaler Pfad: `.mp4`/`.mov`/`.mkv`/`.webm` etc., kein `yt-dlp` nötig.
   - `--start`/`--end`: fokussiertes Zeitfenster (nennt der User einen Zeitpunkt — "bei 2:30", "die letzten 30 Sekunden" — hier eintragen). Deutlich dichtere Abtastung (bis 2 fps) als ein Full-Scan.
   - `--no-frames`: nur Transkript, kein Video-Download/keine Frame-Extraktion.
2. **Ausgabe lesen:** Skript druckt `TRANSCRIPT`-Block (mit `[MM:SS]`-Zeitstempeln) und `FRAMES`-Block (Dateipfad + `t=MM:SS.f` pro Zeile) auf stdout.
3. **Jeden gelisteten Frame-Pfad mit `Read` laden** — die JPEGs rendern direkt als Bild im Kontext. Nicht raten, nicht nur den Dateinamen interpretieren.
4. **Antworten, grounded in Frames + Transkript** — nicht "vermutlich zeigt das Video…", sondern was tatsächlich zu sehen/hören war, mit Zeitbezug.
5. **Aufräumen:** Die letzte Zeile nennt das Arbeitsverzeichnis. Ohne absehbare Anschlussfragen `rm -rf` darauf ausführen.

## Frame-Budget (automatisch, keine manuelle Detail-Stufe)
| Dauer | Frames | Modus |
|---|---|---|
| ≤ 30 s | 30 | gleichmäßig über volle Länge |
| ≤ 1 min | 40 | gleichmäßig |
| ≤ 3 min | 60 | gleichmäßig |
| ≤ 10 min | 80 | gleichmäßig |
| > 10 min | 100 (Cap) | dünn — Hinweis auf stderr, `--start`/`--end` für dichten Pass nutzen |
| `--start`/`--end` gesetzt | bis 2 fps, min. 4 | fokussiert, dichter |

Erster und letzter Frame werden immer behalten, unabhängig vom Dedup.

## Dedup (einfacher als das Original, gleiches Prinzip)
Für jeden Frame ein 16×16-Graustufen-Thumbnail per `ffmpeg` erzeugen, mittlere absolute Pixel-Differenz zum zuletzt **behaltenen** Frame berechnen (nicht zum direkten Vorgänger — fängt langsame Übergänge, die frame-zu-frame nie über die Schwelle kommen). Unter Schwelle (2.0) → Duplikat, verwerfen. Reines stdlib+ffmpeg, keine Bildbibliothek nötig. Die `FRAMES`-Zeile meldet, wie viele Duplikate rausgeflogen sind.

## Transkript-Priorität
1. `yt-dlp` zieht vorhandene Captions (manuell bevorzugt, sonst Auto-Captions) als VTT — kostenlos, sofort.
2. Auto-Captions wiederholen bei YouTube oft dieselbe Zeile über mehrere Cues hinweg (Rolling-/Karaoke-Stil) — exakte Folge-Duplikate werden beim Parsen automatisch rausgeworfen.
3. Keine Captions gefunden + `OPENAI_API_KEY` gesetzt → Audio extrahieren (16 kHz mono, ~64 kbit/s), an `whisper-1` schicken, Segmente mit Zeitstempeln übernehmen.
4. Weder Captions noch Key → Transkript-Sektion sagt das explizit, keine Erfindung.

## Nicht verwenden
- Reine Audio-Transkription ohne dass der visuelle Inhalt eine Rolle spielt — dafür reicht Whisper direkt, der Frame-Overhead lohnt nicht.
- Wenn bereits ein vollständiges, korrektes Transkript vorliegt und nur Text-Analyse gefragt ist.
- Private/geschützte Inhalte, auf die `yt-dlp` ohne Login keinen Zugriff hat.
