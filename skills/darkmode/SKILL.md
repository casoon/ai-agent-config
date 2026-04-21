---
name: darkmode
description: Dark mode implementation for Astro + Tailwind v4 — class-based toggle, FOUC-free init script, cookie/localStorage persistence, and contrast-safe light/dark token pairing.
---

# Dark mode

## Activation

### Class-based (recommended — supports a toggle)

Tailwind v4 custom variant in the CSS entry:

```css
@custom-variant dark (&:where(.dark, .dark *));
```

FOUC-free init script in `<head>` — must be `is:inline` to run before paint:

```html
<script is:inline>
  function getStoredTheme() {
    try {
      return document.cookie.match(/(?:^|;\s*)theme=(dark|light)(?:;|$)/)?.[1]
        || localStorage.getItem('theme');
    } catch (e) {
      return null;
    }
  }

  function applyTheme() {
    var t = getStoredTheme();
    document.documentElement.classList.remove('no-js');
    if (t === 'dark' || (!t && matchMedia('(prefers-color-scheme: dark)').matches)) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }

  applyTheme();
  if (window.__applyThemeHandler) {
    document.removeEventListener('astro:after-swap', window.__applyThemeHandler);
  }
  window.__applyThemeHandler = applyTheme;
  document.addEventListener('astro:after-swap', window.__applyThemeHandler);
</script>
```

Re-registering on `astro:after-swap` matters for `ClientRouter` (SPA transitions) so the theme persists across navigations.

### OS-only (no toggle)

Tailwind v4 uses `prefers-color-scheme` by default — no configuration needed, just use `dark:` utilities.

## Persistence

### Cookie

```javascript
document.cookie = 'theme=' + value + ';path=/;max-age=31536000;SameSite=Lax';
```

Technical cookie — no consent banner required (UI preference, not tracking). Add `domain=` only when cross-subdomain persistence is a real requirement.

### localStorage fallback

```javascript
localStorage.setItem('theme', value);
```

## Toggle

```javascript
btn.addEventListener('click', function () {
  var isDark = document.documentElement.classList.toggle('dark');
  var v = isDark ? 'dark' : 'light';
  document.cookie = 'theme=' + v + ';path=/;max-age=31536000;SameSite=Lax';
  try { localStorage.setItem('theme', v); } catch (e) {}
});
```

Use the Cookie Store API only if your target browsers support it. Plain `document.cookie` remains the compatibility path.

## CSS patterns

### Scoped styles (Astro / Svelte)

```css
<style>
  .card { background: #f8f9fa; color: #1f2937; }
  :global(html.dark) .card { background: #2a3234; color: #d2cdc8; }
</style>
```

### Tailwind utilities

```html
<div class="bg-white dark:bg-slate-800 text-gray-900 dark:text-gray-100">
```

## Color guidelines

| Principle | Light | Dark |
|---|---|---|
| Background | Warm off-white | Warm dark (never pure black) |
| Text | Near-black | Off-white (never pure white) |
| Borders | Light gray | Muted dark |
| Accents | Adjust brightness | Lighten or warm up |

### Contrast minimums (WCAG AA)

- Body text: 4.5:1.
- Large text (≥ 18 px bold / 24 px): 3:1.
- Interactive elements: 3:1.

Both modes must independently meet these — see the accessibility-audit skill for full pairing tables.

## Logo handling

```html
<img src="/logo.svg"      class="block dark:hidden" alt="Logo" />
<img src="/logo-dark.svg" class="hidden dark:block" alt="Logo" />
```

## Common mistakes

| Mistake | Fix |
|---|---|
| `#000` background | Use warm dark, e.g. `#1e2628`, `#222a2c` |
| `#fff` text on dark | Use off-white, e.g. `#e6e1dc`, `#d2cdc8` |
| Cold grays in dark mode | Use warm-tinted grays (teal/sand undertone) |
| Same accent in both modes | Lighten or warm the accent on dark surfaces |
| `@media (prefers-color-scheme)` inside scoped styles | Use `:global(html.dark)` for class-based toggle |
| Forgetting `dark:border-*` | Borders are very visible in dark mode — always pair |
