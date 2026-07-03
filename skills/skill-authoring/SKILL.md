---
name: skill-authoring
description: Conventions for skills in this repo — folder structure, description writing, gotcha-first content, categories taxonomy, and governance. Use when reviewing an existing skill for quality or deciding where a new skill belongs. For creating a skill from scratch or running evals, use skill-creator instead.
---

# Skill authoring

## What a skill actually is

A skill is a **folder**, not a file. It can contain documentation, scripts,
data, and config — not just prose. An agent can discover, read, combine, and
execute these contents. Value comes from pairing knowledge with runnable tools,
not text alone.

## Folder structure

```
skills/my-skill/
├── SKILL.md          # required — description frontmatter + core knowledge
├── scripts/          # executable helpers the agent can run
├── examples/         # concrete usage examples
├── docs/             # supplementary reference (API docs, specs)
└── assets/           # data files, schemas, config templates
```

The agent reads selectively. Structure enables progressive disclosure: load
`SKILL.md` first, pull from `scripts/` or `docs/` only when needed.

## The description field is a trigger condition

```yaml
description: When to use this skill and what it covers — written for the
             agent, not for humans. Conditions and trigger logic, not marketing.
```

The agent uses `description` to decide **whether** to load this skill. Write it
as a condition ("Use when X", "Covers Y") not a caption. Vague or overly broad
descriptions cause the skill to be loaded always or never.

## Content priorities

### 1. Gotchas first

Document **real failures before standard usage**. The agent already knows
standard patterns; what it lacks is project-specific edge cases, version
quirks, and footguns. A list of gotchas is often the highest-value content a
skill can carry.

### 2. Code over prose

Prefer scripts over explanations. Scripts save tokens, skip interpretation
steps, and compose with other tools. A 10-line shell script beats three
paragraphs describing what you'd do manually.

### 3. Don't document the obvious

Skip what the agent already knows from training. Focus on:
- Internal conventions that differ from the public norm
- Integration quirks specific to this stack
- Things that broke in practice

## Skill categories (taxonomy)

| Category | Purpose | High-value content |
|---|---|---|
| Library & API reference | Agent uses tools correctly | Gotchas, versioned examples, non-obvious options |
| Verification & testing | Validate output, not just generate | Test flows, assertions, browser automation — highest impact |
| Data access & analysis | Agent works with real data | Queries, data models, dashboard mappings |
| Business process | Automate recurring tasks | Workflow steps, system integration, output formats |
| Code templates & scaffolding | Standardize structure | Generators, best-practice templates, migration patterns |
| Code quality & review | Enforce standards | Review rules, style guides, automated check configs |
| CI/CD & deployment | Build/release automation | Deploy pipelines, rollback logic, merge conditions |
| Runbooks | Systematic incident handling | Diagnosis steps, tool mappings, alert responses |
| Infrastructure & ops | Standardize operations | Cleanup scripts, cost analysis, security checks |

Keep each skill in **one** category. Mixed-purpose skills confuse the agent
about when to load them and dilute the content quality.

## Persistence

For skills that track state across runs:
- Use a log file, JSON, or SQLite in a **dedicated directory outside the skill
  folder** — skill files can be overwritten on update.
- Keep the schema simple; the agent should be able to read and write it without
  a library.

## Hooks and modes

Only activate hooks inside a skill when there's a clear trigger:
- Security / write-protection mode: `on_write` hooks
- Verification mode: `post_run` hooks

Unconditional hooks add latency and noise. The agent must opt in via the skill's
documented conditions, not by default.

## Sizing and governance

- **One skill per concern.** If a skill description requires more than two
  clauses, split it.
- **Fewer skills with depth beat many shallow skills.** Skill count grows
  context cost; each skill description is always loaded.
- **Measure usage.** Unused skills waste context. Log invocations via a hook;
  prune skills that never fire.
- **Iterate from real problems.** The best skills are extracted from actual
  failures, not designed up front.

## Anti-pattern catalog (named)

- **Kitchen Sink** — one skill covering many concerns. Split it.
- **Orphan** — a skill nothing triggers / never loads. Delete or merge.
- **Clone** — a narrow sibling of an existing skill. Extend the existing one instead.
- **Script without Skill** — a `scripts/` folder with no SKILL.md saying when/how to use it.

## Before writing: peer-match

`ls` the target category and read 2–3 neighbouring SKILL.md first, to match tone
and structure. **Prefer extending an existing skill over creating a narrow sibling.**

## Frontmatter options

- `description` names the trigger CLASS ("Use when debugging…") **plus** an explicit
  **counter-trigger** ("Not for…") — this sharpens matching more than any keyword list.
- `disable-model-invocation: true` for skills that should fire only when the user
  explicitly asks (e.g. handoff, council-style) — prevents accidental auto-firing.

## Checklist for a new skill

- [ ] Single category, clear `description` trigger
- [ ] Gotchas documented before standard usage
- [ ] Runnable scripts where prose would do the same work
- [ ] Internal specifics only — nothing the agent already knows
- [ ] Folder structure used where sub-documents add value
- [ ] No overly rigid rules that eliminate the agent's judgment
- [ ] `description` has a counter-trigger ("Not for…")
- [ ] Peer-matched — extends rather than clones an existing skill
- [ ] Verified after writing: frontmatter valid, path correct, committed
