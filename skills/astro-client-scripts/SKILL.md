---
name: astro-client-scripts
description: Client-side script patterns in Astro — when to use scoped <script> vs is:inline, ClientRouter behavior, define:vars, and when to reach for a Svelte island instead. Use when adding or reviewing <script> tags in .astro files.
---

# Astro client scripts

## Core rule — prefer scoped `<script>` over `is:inline`

Astro's default `<script>` (without `is:inline`) is a module script that gets:

- Bundled, deduplicated, and tree-shaken by Vite.
- TypeScript support inside the block.
- No global function-name collisions.
- Automatic `defer` (no `DOMContentLoaded` wrapper needed).

Always use `<script>` unless you have a specific reason for `is:inline`.

## Migration pattern

### Before (anti-pattern)

```html
<script is:inline>
  function initMyComponent() {
    const el = document.querySelector('.my-el');
    // ...
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMyComponent);
  } else {
    initMyComponent();
  }
</script>
```

### After

```html
<script>
  const el = document.querySelector('.my-el');
  if (el) {
    // ...logic directly at module top level
  }
</script>
```

Steps:

1. Remove `is:inline`.
2. Unwrap `initXyz()` — module code runs at top level.
3. Drop `DOMContentLoaded` (modules are deferred by default).
4. Add TypeScript casts where needed (`as HTMLElement`, `as TouchEvent`).
5. Remove `typeof window` guards — modules only run in the browser.

## When `is:inline` IS required

### 1. Theme / FOUC prevention in `<head>`

Must execute synchronously before first paint:

```html
<script is:inline>
  function getStoredTheme() {
    try {
      return document.cookie.match(/(?:^|;\s*)theme=(dark|light)(?:;|$)/)?.[1]
        || localStorage.getItem('theme');
    } catch { return null; }
  }

  function applyTheme() {
    document.documentElement.classList.remove('no-js');
    const stored = getStoredTheme();
    if (stored === 'dark' || (!stored && matchMedia('(prefers-color-scheme: dark)').matches)) {
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

### 2. Scripts using `define:vars`

`define:vars` requires `is:inline`:

```html
<script is:inline define:vars={{ baseColor, endpoint }}>
  console.log(baseColor, endpoint);
</script>
```

### 3. Third-party snippets that must not be bundled

Analytics, tracking pixels, classic scripts:

```html
<script is:inline src="https://analytics.example.com/script.js"></script>
```

## `ClientRouter` (SPA) considerations

When `<ClientRouter />` is active (Astro v6 SPA transitions):

- `is:inline` scripts re-run on every navigation by default.
- Module `<script>` tags run once and persist across navigations.
- Use `astro:after-swap` for code that must re-run after SPA navigation.
- Use `astro:page-load` for code that should run on every page, including the initial load.

```html
<script>
  document.addEventListener('astro:page-load', () => {
    const el = document.querySelector('.my-el');
    if (el) {
      // re-initialize on every navigation
    }
  });
</script>
```

## Prefer a Svelte island for real interactivity

For anything beyond simple DOM manipulation, reach for a Svelte 5 island:

```svelte
<script lang="ts">
  let dark = $state(document.documentElement.classList.contains('dark'));

  function toggle() {
    dark = !dark;
    document.documentElement.classList.toggle('dark', dark);
    const theme = dark ? 'dark' : 'light';
    document.cookie = `theme=${theme}; path=/; max-age=31536000; SameSite=Lax`;
    localStorage.setItem('theme', theme);
  }
</script>

<button onclick={toggle} aria-label="Toggle theme">
  {dark ? 'Light' : 'Dark'}
</button>
```

```astro
<ThemeToggle client:load />
```

## Decision tree

```
Need client-side JS?
├─ Simple DOM query / manipulation → <script> (no is:inline)
├─ Reactive state / complex UI → Svelte 5 island (client:load/idle/visible)
├─ Must run before paint (theme / FOUC) → <script is:inline> in <head>
├─ Needs define:vars → <script is:inline define:vars={…}>
└─ Third-party snippet → <script is:inline src="…">
```

## Common mistakes

| Mistake | Fix |
|---|---|
| `is:inline` "just to be safe" | Remove it — modules are better in every way |
| `DOMContentLoaded` wrapper in a module script | Drop it — modules are deferred |
| `typeof window !== 'undefined'` in a module | Remove — browser-only by definition |
| Global function names in `is:inline` | Use scoped `<script>` or an IIFE |
| Multiple `is:inline` scripts that could merge | Combine into one scoped `<script>` |
| `is:inline` for Astro lifecycle listeners | Only needed in `<head>`, otherwise use a module |
