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

## Invocation: model vs. user, and the router pattern

A skill is reached one of two ways, and each way spends a different budget:

- **Model-invoked** (default: `description` present) — the agent can fire the
  skill on its own, and any other skill can reach it too. The cost is
  **context load**: the description sits in the window on every turn, whether
  or not the skill fires this session.
- **User-invoked** (`disable-model-invocation: true`) — only a human typing
  the skill's name can reach it; nothing else can. Zero context load, but the
  cost moves to the human: **cognitive load** — *you* become the index that
  has to remember the skill exists and when to reach for it.

Neither cost is free, so the choice is deliberate, not default-model-invoked:
pick model-invocation when the agent genuinely needs to reach the skill
without being told, or when another skill needs to invoke it. If it only ever
fires by hand — a one-off orchestration, a destructive or opinionated flow the
user should trigger consciously — make it user-invoked and stop paying for a
description no one needed loaded.

This repo currently has no user-invoked skill (no `disable-model-invocation`
in active use), which is fine while the count per concern stays low. The
tripwire: once user-invoked skills multiply past what a person can hold in
their head, that cognitive load is the signal to add a **router skill** — one
user-invoked skill whose only job is to name the others and when to reach for
each. It can only point, never fire them (user-invoked skills have no
description for anything else to call) — but it turns "remember 15 skill
names" into "remember one".

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

### 4. Checkable completion criteria

Every ordered step should end on a condition the agent can actually check —
"every modified page listed", not "produce an overview". A vague criterion
invites premature completion: the agent decides it's done before it is. Where
it matters, make the criterion exhaustive too ("every affected route", not "a
few examples") — that's what turns a step into real legwork instead of a
token gesture at one.

## Leading words

A **leading word** is a compact, already-pretrained concept the agent thinks
with while running a skill — *gotcha*, *tracer bullet*, *fog of war*. Used
consistently, it replaces a paragraph of restated qualifiers with one token
that recruits behaviour the model already associates with it, and it anchors
invocation too: the same word in the `description`, in your prompts, and in
project docs links them all to the same skill.

Reach for an existing word before coining one — a made-up term carries no
priors, so you pay in definition tokens what a pretrained word gives for
free. When a skill restates one quality across several sentences ("fast,
low-overhead, deterministic loop"), that's a candidate to collapse into a
single leading word instead.

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

Structural (shape of the skill or the repo):

- **Kitchen Sink** — one skill covering many concerns. Split it.
- **Orphan** — a skill nothing triggers / never loads. Delete or merge.
- **Clone** — a narrow sibling of an existing skill. Extend the existing one instead.
- **Script without Skill** — a `scripts/` folder with no SKILL.md saying when/how to use it.

Prose-level (inside a `SKILL.md` that's otherwise well-shaped):

- **Sediment** — stale content that accumulated because adding felt safe and
  removing felt risky. Any skill without an active pruning pass settles into
  this by default; the fix is deleting, not further editing.
- **No-Op** — a line the agent would already do without being told ("be
  thorough"). Test: does it change behaviour versus the default? If not, cut
  it or replace the weak word with a stronger leading word ("thorough" →
  "relentless").
- **Negation** — steering by prohibition ("don't do X") tends to name X and
  make it more salient, not less. State the target behaviour positively
  instead; keep a bare prohibition only for a hard guardrail that can't be
  phrased as a positive instruction, and even then pair it with what to do
  instead.

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
- [ ] Invocation deliberate — model-invoked only if the agent must reach it
      unprompted; otherwise `disable-model-invocation: true`
- [ ] Gotchas documented before standard usage
- [ ] Runnable scripts where prose would do the same work
- [ ] Internal specifics only — nothing the agent already knows
- [ ] Folder structure used where sub-documents add value
- [ ] Ordered steps end on a checkable (and, where it matters, exhaustive)
      completion criterion
- [ ] No overly rigid rules that eliminate the agent's judgment; prohibitions
      phrased as the positive target where possible
- [ ] `description` has a counter-trigger ("Not for…")
- [ ] Peer-matched — extends rather than clones an existing skill
- [ ] Verified after writing: frontmatter valid, path correct, committed
