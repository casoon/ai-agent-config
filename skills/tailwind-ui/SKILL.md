---
name: tailwind-ui
description: Tailwind CSS v4 guidance — Vite plugin setup, CSS-first @theme configuration, v4 syntax changes, container queries, dark-mode custom variant, logical properties, and design-token discipline.
---

# Tailwind UI

## Principles

- Prefer consistency over one-off styling experiments.
- Keep class lists readable — extract repeated patterns into components.
- Use arbitrary values only when justified.
- Preserve visible focus and interaction states (hover, focus, disabled, active).
- Design tokens (CSS custom properties) first, Tailwind utilities on top.

## Setup

Tailwind v4 uses a Vite plugin, not PostCSS:

```javascript
// astro.config.mjs
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  vite: { plugins: [tailwindcss()] },
});
```

CSS entry:

```css
/* src/styles/app.css */
@import 'tailwindcss';
@import '@fontsource/inter/latin-400.css';
```

## CSS-first configuration

Tailwind v4 is configured via CSS, not `tailwind.config.js`:

```css
@import 'tailwindcss';

@theme {
  --color-primary: oklch(58% 0.18 220);
  --color-accent:  oklch(68% 0.16 250);
  --font-sans:     'Inter', ui-sans-serif, system-ui, sans-serif;
}
```

Keep a shared `@theme` block that registers your design tokens, then reference them via `var()` in component styles and via the matching Tailwind utilities (e.g. `bg-accent`).

## v4 syntax changes (from v3)

### Renamed classes

```
bg-gradient-to-r   → bg-linear-to-r
bg-gradient-to-br  → bg-linear-to-br

flex-shrink-0      → shrink-0
flex-grow          → grow

aspect-[3/2]       → aspect-3/2

grayscale-[30%]    → grayscale-30
```

### Container queries (built in)

```html
<div class="@container">
  <div class="@sm:flex @md:grid @md:grid-cols-2 @lg:grid-cols-3">
    <!-- Responds to the container, not the viewport -->
  </div>
</div>
```

### Native CSS nesting

```css
.card {
  background: var(--color-surface);

  &:hover { box-shadow: var(--shadow-md); }
  & h2 { font-weight: 700; }
}
```

## Design tokens

Typical token groups to define in `@theme` (or a shared `variables.css`):

- Colors — `--color-bg`, `--color-surface`, `--color-text`, `--color-text-secondary`, `--color-border`, `--color-accent`, `--color-accent-hover`, `--color-success`, `--color-warning`, `--color-error`, `--color-info`.
- Spacing — `--space-xs` … `--space-3xl`.
- Typography — `--font-sans`, `--font-serif`, `--font-mono`.
- Radii — `--radius-sm` … `--radius-full`, plus component-specific `--card-radius`, `--button-radius`, `--input-radius`.
- Shadows — `--shadow-sm` … `--shadow-xl`.
- Transitions — `--transition-fast` (150 ms), `--transition-base` (200 ms), `--transition-slow` (300 ms).
- Z-index scale — `--z-dropdown` … `--z-tooltip`.

Use `var(--token)` inside scoped `<style>` blocks; use the matching Tailwind utility in markup. Never hard-code color values.

## Dark mode

Class-based, with a custom variant in the CSS entry:

```css
@custom-variant dark (&:where(.dark, .dark *));
```

Both mode-aware tokens and explicit `dark:` utilities are fine:

```html
<div class="bg-white dark:bg-neutral-900 text-neutral-900 dark:text-neutral-100">
```

Prefer tokens for structural colors (`var(--color-bg)` flips automatically when `.dark` is set) and `dark:` utilities for one-offs.

## Tailwind v4.2 features

### Font-feature utilities

```html
<code class="font-variant-[ligatures_contextual]">fn() =&gt; {}</code>
<td class="tabular-nums">1,234.56</td>
<span class="small-caps">Section Title</span>
```

Apply ligatures and tabular numbers to `code`/`pre` and heading elements in a global stylesheet.

### New neutral color palettes

v4.2 adds `mauve`, `taupe`, `olive`, `mist` alongside `gray`, `slate`, `zinc`, `stone`. No config needed — they behave like any Tailwind color:

```html
<div class="bg-mist-50 dark:bg-mist-950 text-taupe-900">
```

### Logical properties (i18n / RTL-ready)

Prefer logical utilities for inline-axis spacing so layouts survive RTL:

```
pl-4 / pr-4   →  ps-4 / pe-4        (padding-inline-start/end)
ml-4 / mr-4   →  ms-4 / me-4        (margin-inline-start/end)
border-l-*    →  border-s-*         (border-inline-start)
```

Physical block-axis utilities (`pt-*`, `pb-*`, `mt-*`, `mb-*`) remain unchanged.

### Webpack plugin

`@tailwindcss/webpack` is first-class in v4.2 — irrelevant for Vite/Astro projects.

## Best practices

1. Design tokens for everything — `var(--color-*)` over hardcoded values.
2. Scoped component styles in `<style>` blocks for component-specific CSS.
3. Tailwind for utility-scale adjustments directly in markup.
4. Mobile-first: `sm:`, `md:`, `lg:` breakpoints ascending.
5. OKLCH for colors — predictable lightness across themes.
6. No `tailwind.config.js` — everything via CSS or tokens.

## Review checklist

- Is the class list still readable? Extract component classes where it isn't.
- Are repeated patterns extracted into reusable components?
- Are responsive rules consistent (same breakpoints, same order)?
- Are hover, focus, disabled, and active states complete?
- Are all colors sourced from tokens — not hex values — so light/dark stay in sync?
- Are inline-axis spacings using logical utilities (`ps-*`/`pe-*`) where RTL support matters?
