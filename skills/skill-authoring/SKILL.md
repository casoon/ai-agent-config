---
name: skill-authoring
description: How to build effective agent skills — folder structure, description writing, gotcha-first content, categories taxonomy, and governance. Use when creating, reviewing, or improving a skill in this repo.
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

## Checklist for a new skill

- [ ] Single category, clear `description` trigger
- [ ] Gotchas documented before standard usage
- [ ] Runnable scripts where prose would do the same work
- [ ] Internal specifics only — nothing the agent already knows
- [ ] Folder structure used where sub-documents add value
- [ ] No overly rigid rules that eliminate the agent's judgment
