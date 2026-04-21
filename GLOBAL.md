# Global personal instructions

This file is loaded by Claude Code for every project.
Keep it short. Stack-specific knowledge belongs in Skills, project-specific rules belong in the project's CLAUDE.md.

## Core principles

- Do exactly what is asked — no more, no less.
- Prefer modifying existing code over adding new files.
- Minimize surface area of changes.
- Avoid speculative improvements unless explicitly requested.

## Working style

- Start non-trivial tasks with a brief plan before making changes.
- Break work into small, reviewable steps.
- Reuse existing project patterns before introducing new abstractions.
- State assumptions explicitly when requirements are unclear.
- Stop and ask if multiple valid approaches exist with different trade-offs.

## Validation

- Run targeted checks first: typecheck, lint, focused tests.
- Avoid running full test suites unless necessary.
- Mention what was validated and what was not.
- Flag risky, destructive, or hard-to-reverse changes before executing them.

## Code quality

- Prefer explicit, readable code over cleverness.
- Keep naming consistent with the surrounding codebase.
- Avoid hidden side effects and implicit behavior.
- Preserve public APIs unless explicitly asked to change them.
- Do not introduce new dependencies without a clear justification.
- Prefer deletion over addition when possible.
- Do not add defensive code for impossible states — trust invariants.

## Scope control

- Do not fix unrelated issues.
- Do not reformat unrelated code.
- Do not upgrade dependencies unless required.
- Do not refactor outside the task scope.

## Communication

- Summarize outcome in 1–2 lines.
- Only mention risks or follow-ups if they matter.
- Do not explain obvious changes.
- Do not restate the diff.

## Output

- Prefer minimal, direct answers.
- Avoid long explanations unless explicitly requested.
- Show only relevant code snippets, not entire files.

---

<!-- PRIVATE SECTION — do not publish this part, keep it in your private fork -->
<!-- Add your personal specifics here:
  - Preferred package manager
  - Languages and tools you work with daily
  - Projects that need special handling
  - Personal code style preferences
  - Commit and PR conventions
-->
