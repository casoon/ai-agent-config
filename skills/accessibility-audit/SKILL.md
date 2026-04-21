---
name: accessibility-audit
description: WCAG 2.2 AA patterns for Astro pages, forms, and interactive components — semantics, keyboard, focus, labels, contrast, motion. Use when building or reviewing accessible UI.
---

# Accessibility audit

Barrierefreiheit ist Baseline, kein Feature. Jedes Pattern muss ohne Maus, ohne Sehen und ohne perfekte Motorik nutzbar sein.

## Focus areas

- Semantic HTML first — use native elements (`<button>`, `<a>`, `<details>`, `<dialog>`) where possible.
- Keyboard access and visible focus indicators on all interactive elements.
- Labels, landmarks, and sensible heading hierarchy.
- Contrast and motion preferences respected in light and dark mode.

## Page structure

- One `<h1>` per page, no skipped heading levels.
- Landmarks: `<nav aria-label="…">`, `<main id="main">`, `<article>`, `<section aria-labelledby="…">`, `<aside>`, `<footer>`.
- Skip link to `#main` in the layout.
- Set `lang` on `<html>`; derive per locale where i18n is in use.

## Interactive elements

### Links

- Links distinguishable by underline, not color alone.
- External links with `target="_blank"` need `rel="noopener noreferrer"` and a screen reader hint (`<span class="sr-only">(opens in new tab)</span>`).
- Icon-only links need `aria-label`; the icon inside gets `aria-hidden="true"`.
- Never use `<a>` without `href` for actions — use `<button type="button">`.

### Buttons

- Icon-only buttons must have `aria-label`; inner icon `aria-hidden="true"`.
- Always set `type="button"` or `type="submit"` explicitly.
- Never `<div onclick>` — use `<button>`.

### Keyboard navigation

```css
/* Global focus style — never remove without a visible alternative */
:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}
```

- Focus order follows visual layout — don't use positive `tabindex`.
- Custom interactive elements need `tabindex="0"`, appropriate `role`, and keyboard event handlers.

### Touch targets (WCAG 2.5.8)

Minimum 44×44 px for all interactive elements. Apply padding or `min-h-[44px] min-w-[44px]`.

## Forms

```astro
<div>
  <label for="email" class="text-sm font-semibold">
    Email <span aria-hidden="true">*</span>
  </label>
  <input
    type="email"
    id="email"
    name="email"
    required
    autocomplete="email"
    aria-invalid={!!inputError?.email}
    aria-describedby={inputError?.email ? 'email-error' : undefined}
  />
  {inputError?.email && (
    <span id="email-error" class="text-xs text-error" role="alert">
      {inputError.email}
    </span>
  )}
</div>
```

Checklist:

| Requirement | Implementation |
|---|---|
| Associated label | `<label for="id">` matching `<input id="id">` |
| Required indicator | Visual `*` with `aria-hidden="true"` plus `required` |
| Error state | `aria-invalid={true}` on invalid input |
| Error message | `<span role="alert">` linked via `aria-describedby` |
| Autocomplete | `autocomplete="name\|email\|tel\|..."` |
| Grouped inputs | `<fieldset>` + `<legend>` for radios/checkboxes/address blocks |
| Success feedback | `<div role="status">` |

## Tables

- `<caption>` for purpose, `<th scope="col">` for columns, `<th scope="row">` for row headers.
- Never use tables for layout.

## Images

- All `<img>` need `alt`. Decorative: `alt=""` plus `aria-hidden="true"`.
- Always set `width` and `height` to prevent layout shift.
- SVG icons: `aria-hidden="true" focusable="false"` when decorative.

## Color & contrast

| Text type | Minimum ratio |
|---|---|
| Normal text (< 18 px) | 4.5:1 |
| Large text (>= 18 px bold / 24 px) | 3:1 |
| UI components, borders, icons, focus rings | 3:1 |

- Never use color as the sole indicator — pair with icon, text, or pattern.
- Every color class needs an explicit `dark:` counterpart; both modes must independently meet contrast.
- Avoid low-contrast muted grays on white (e.g. `text-neutral-400`).

## Motion

All animations must respect `prefers-reduced-motion`:

```css
.animate-fade-in { animation: fadeIn 0.3s ease-out; }

@media (prefers-reduced-motion: reduce) {
  .animate-fade-in { animation: none; }
}
```

- No blinking or flashing effects (WCAG 2.3.1 — max 3 flashes/sec).
- Tailwind: use `motion-safe:` and `motion-reduce:` variants.
- Scroll-driven animations: provide `@supports` fallback plus reduced-motion override.

## ARIA patterns

### Navigation with `aria-current`

```astro
<a href={href} aria-current={isActive ? 'page' : undefined}>{label}</a>
```

### Disclosure / accordion

Prefer native `<details>` + `<summary>`. For custom accordions use `aria-expanded` and `aria-controls`.

### Tabs

- `role="tablist"` with `aria-label` on container.
- `role="tab"` + `aria-selected` on each tab; inactive tabs `tabindex="-1"`.
- `role="tabpanel"` + `aria-labelledby` on each panel.
- Arrow-key navigation left/right.

### Dialog

Prefer native `<dialog>`. For custom modals:

- `role="dialog"` + `aria-modal="true"` + `aria-labelledby`.
- Focus trap, Escape closes, return focus to trigger on close.

### Live regions

- `aria-live="polite"` for non-urgent status.
- `role="alert"` for errors (assertive).
- `role="status"` for success messages.

## Lists

Tailwind's `list-none` strips list semantics in Safari — add `role="list"` when you need the semantic back.

## Anti-patterns

```html
<!-- WRONG -->  <div class="cursor-pointer" onclick="…">Click me</div>
<!-- RIGHT -->  <button type="button">Click me</button>

<!-- WRONG -->  <button><svg>…</svg></button>
<!-- RIGHT -->  <button aria-label="Close menu"><svg aria-hidden="true">…</svg></button>

<!-- WRONG -->  <span class="text-red-500">Error</span>
<!-- RIGHT -->  <span class="text-red-500">⚠ Error: email is required</span>

<!-- WRONG -->  <p class="text-neutral-700">Text</p>
<!-- RIGHT -->  <p class="text-neutral-700 dark:text-neutral-300">Text</p>
```

## New page checklist

- `lang` set on `<html>`.
- Single `<h1>`, sensible heading hierarchy.
- Semantic landmarks in place, skip link works.
- All images have `alt` (or `alt=""` + `aria-hidden`).
- All links have visible underline (or button styling is intentional).
- Icon-only buttons/links have `aria-label`.
- Form inputs: `<label>`, `aria-invalid`, `aria-describedby`, `autocomplete`.
- Fieldset + legend for grouped inputs.
- Error messages use `role="alert"`; success uses `role="status"`.
- Focus indicators visible, no keyboard traps, all interactive elements reachable.
- Contrast meets 4.5:1 / 3:1 and holds in dark mode.
- No color-only signals.
- Touch targets ≥ 44×44 px.
- Animations respect reduced motion.
- External links: `rel="noopener noreferrer"`.
- Tables: `<caption>` and `<th scope>`.

## Testing

### Automated (axe-core + Playwright)

```typescript
import AxeBuilder from '@axe-core/playwright';

test('page has no a11y violations', async ({ page }) => {
  await page.goto('/new-page');
  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag22aa'])
    .analyze();
  expect(results.violations).toEqual([]);
});
```

### Build-time

[`@casoon/astro-post-audit`](https://github.com/casoon/astro-post-audit) checks after every build for missing alt text, missing labels, empty button text, missing skip link, and heading hierarchy violations.

### Manual

- Tab through the page — verify focus order and visibility.
- Screen reader (VoiceOver / NVDA / Orca).
- Zoom to 200 % — content must reflow without horizontal scroll.
- Enable `prefers-reduced-motion` in DevTools — animations must stop.
- DevTools Accessibility tab — check computed roles and names.
