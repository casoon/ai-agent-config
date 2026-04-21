---
name: ui-design
description: Seven core UI rules for consistent, hierarchical, readable interfaces — colors, spacing, typography, and CTA tiers. Use when designing or reviewing pages, components, and layouts.
---

# UI design rules

Apply these seven rules whenever building or reviewing UI. Most bad UIs fail not on technical grounds, but on consistency, hierarchy, and missing systems.

## 1. No pure black / white

- `#000` on `#fff` is harsh and tiring.
- Soften to `#111` / `#f5f5f5`, or OKLCH equivalents such as `oklch(18% 0 0)` on `oklch(98% 0 0)`.
- Use tokens — `var(--color-text)` and `var(--color-bg)` — so both modes flip cleanly.

## 2. Consistent spacing — 8 px system

- Avoid arbitrary values (13 px, 22 px, 7 px).
- Stick to a scale: 8, 16, 24, 32, 48, 64 …
- Tailwind: `p-2` (8 px), `p-4` (16 px), `p-6` (24 px), `p-8` (32 px).
- Use `--space-sm`, `--space-md`, `--space-lg` tokens where defined.

## 3. Max 2 typefaces

- Many fonts = visual noise.
- 1–2 families plus varied weights.
- Typical split: UI sans (Inter), editorial serif (Lora) for long-form, monospace (Fira Code) for code.
- Vary weight and size before reaching for another family.

## 4. Color system — 60 / 30 / 10

| Share | Role | Examples |
|---|---|---|
| 60 % | Background | `--color-bg`, `--color-bg-secondary` |
| 30 % | Surfaces | `--color-surface`, cards, panels |
| 10 % | Accent | `--color-accent`, buttons, highlights |

Accent is reserved for actions and focal points — overusing it removes its meaning.

## 5. Clear type hierarchy

- Headings must step visually, not just in markup.
- Minimum 1.25×–1.5× step between levels.
- `h1` dominant, `h2` clearly smaller, `h3` body-adjacent.
- Use the defined text-scale tokens; don't freestyle sizes.

## 6. Readable line length

- Full-width running text fatigues the eye.
- Target 50–75 characters per line → `max-w-prose` (65 ch) in Tailwind.
- Apply to article/blog body text. Navigation and UI elements are exempt.

## 7. Visual hierarchy — the most important rule

Every interactive element needs a tier:

| Tier | Usage | Style |
|---|---|---|
| Primary | One dominant CTA per view | Filled, accent color, high contrast |
| Secondary | Supporting actions | Outlined or muted |
| Ghost / tertiary | Low-priority actions | Text-only or subtle border |

Never have two primary buttons competing on the same screen. If everything shouts, nothing does.

## Quick checklist for new pages

- [ ] No pure `#000` / `#fff` — design tokens in use?
- [ ] Spacing follows the 8 px grid?
- [ ] Max 2 font families?
- [ ] Accent color on ≤ 10 % of the surface?
- [ ] Heading sizes step clearly between levels?
- [ ] Body text constrained to ~65 ch?
- [ ] Only one primary CTA visible per section?
