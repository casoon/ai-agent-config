# Global personal instructions

This file is loaded by Claude Code for every project.
Keep it short. Stack-specific knowledge belongs in Skills, project-specific rules belong in the project's CLAUDE.md.

## Working style

- Start non-trivial tasks with a brief plan before making changes.
- Prefer small, reviewable changes over broad rewrites.
- Reuse existing project patterns before introducing new abstractions.
- State assumptions explicitly when requirements leave room for interpretation.
- Prefer explicit over clever — code should be readable without context.

## Validation

- Run targeted checks first: typecheck, lint, focused tests.
- Prefer narrow validation over broad test suites unless the task scope requires it.
- Mention what was validated and what was not.
- Flag risky or hard-to-reverse changes before executing them.

## Code quality

- Keep naming explicit and readable.
- Avoid hidden side effects.
- Preserve public APIs unless change is explicitly requested.
- Do not introduce new dependencies without a short reason.
- Less code is usually better than more abstraction.
- Do not add error handling for scenarios that cannot happen — trust internal guarantees.

## Communication

- Summarize the outcome in one or two lines.
- Mention follow-up items or risks only when they matter.
- Do not restate what was just done — the diff speaks for itself.

---

<!-- PRIVATE SECTION — do not publish this part, keep it in your private fork -->
<!-- Add your personal specifics here:
  - Preferred package manager
  - Languages and tools you work with daily
  - Projects that need special handling
  - Personal code style preferences
  - Commit and PR conventions
-->
