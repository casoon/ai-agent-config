# Changelog

All notable changes to this project are documented in this file. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/). The repository is a periodically
re-exported snapshot without version tags, so all changes so far are listed under
Unreleased, with the date of each export.

## [Unreleased]

### Added

- Project website and documentation under `site/` and `docs/`, published to GitHub Pages.
- `.nosecretsignore` with the reviewed placeholder findings in the Cloudflare reference docs;
  the pre-commit secret scan now runs on every commit (2026-08-26).
- `social-pulse` skill (2026-08-26).
- `complexity-judgment` skill; the `context7` MCP server in `codex-config.example.toml`
  (2026-08-26).
- `video-watch` skill (2026-08-26).
- 12 generic skills from the private baseline: `content-qa`, `design-systems`,
  `ai-ux-patterns`, `ux-patterns`, `visual-trends`, `cloudflare-one`,
  `cloudflare-one-migrations`, `turnstile-spin`, `native-html-ui`,
  `sandbox-migrate-to-next`, `sandbox-next`, `sandbox-stable` (2026-08-26).
- `web-design-workflow` and `design-directions` skills (2026-07-04).
- 33 general skills for accessibility consulting and review, content and marketing, research
  and workflow, among them `deep-research`, `llm-council`, `systematic-debugging`, `handoff`,
  `conversation-retrospective`, `anti-ai-copy` and `knowledge-base` (2026-07-03).
- Initial public snapshot: `GLOBAL.md`, five subagents, 31 skills, the link scripts for
  Claude Code, Codex and Mistral Vibe, the Codex agent renderer, the pre-commit hook and
  `codex-config.example.toml` (2026-07-01).

### Changed

- Cloudflare reference docs tightened: flagship, pipelines, r2-data-catalog, r2-sql
  (2026-08-26).
- `skill-authoring`, `agent-config-authoring` and `i18n` synced with the private baseline
  (2026-08-26).
- `anti-ai-copy` extended with further patterns from blader/humanizer and a false-positive
  guardrail; it now applies to any text, not only customer copy (2026-08-26).
- `agent-config-authoring` synced with the private baseline (2026-07-06).
- `motion-design`, `ui-design`, `frontend-design`, `post-audit` and `skill-authoring` updated
  (2026-07-03).
