---
name: web-performance
description: Performance patterns for Astro sites — responsive images, CSS containment, minimal client JS, font loading, and Core Web Vitals targets. Use when optimizing page load, bundle size, or diagnosing slow pages.
---

# Web performance

## Images

### Responsive variants

Generate multiple widths (e.g. 378 w, 756 w, 1200 w) in WebP. Source images at 1024×1024 for blog teasers, 1200×630 for OG images.

### Lazy loading

```html
<img src="image.webp" loading="lazy" decoding="async" width="756" height="504" alt="…" />
```

Only hero / above-the-fold images use `loading="eager"`. Always set `width` and `height` to prevent CLS.

### Format

Prefer WebP (or AVIF for larger hero images). Let Astro's image service handle format negotiation where possible.

## CSS performance

### `content-visibility` for long pages

```css
.article-card {
  content-visibility: auto;
  contain-intrinsic-size: 0 300px;
}
```

Browsers skip rendering of off-screen cards; `contain-intrinsic-size` prevents layout shift.

### CSS containment

```css
.card { contain: layout paint style; }
```

Isolates layout and paint calculations to the element.

### Animation cost

- Avoid `filter: blur()` on moving elements.
- Use `transform: translate3d()` for GPU compositing.
- Keep `will-change` to the minimum of elements that actually need it.
- Prefer CSS `animation-timeline: view()` over JS scroll handlers.

## JavaScript

### Minimize client JS

Astro renders zero JS by default — keep it that way.

- Use `<script>` only when truly needed.
- Prefer CSS-only solutions: `:has()`, `<details>`, popover, `<dialog>`.
- Hydrate islands with `client:visible` or `client:idle` instead of `client:load`.

### Scroll handlers

```javascript
// Bad — runs every scroll frame
window.addEventListener('scroll', handler);

// Better — passive
window.addEventListener('scroll', handler, { passive: true });

// Best — CSS scroll-driven animation, no JS
/* .element { animation-timeline: view(); } */
```

## Font loading

```css
@import '@fontsource/inter/latin-400.css';
```

- Self-host via `@fontsource` — no external requests, optimal caching.
- `font-display: swap` is already set by `@fontsource`.
- Subset to the scripts you actually need (`latin`, `latin-ext`, etc.).

## Build optimization

- Run `@casoon/astro-post-audit` after the build to validate assets, duplicates, and structure.
- Review Vite's bundle output for large chunks: unintended npm packages in client bundles, duplicate component instances, inline SVGs that should be external.

## Core Web Vitals

| Metric | Target | Common fix |
|---|---|---|
| LCP | < 2.5 s | Preload hero image, inline critical CSS |
| CLS | < 0.1 | Explicit `width`/`height` on images, `contain-intrinsic-size` for off-screen cards |
| INP | < 200 ms | Move work off main thread, reduce JS, prefer CSS interactions |

## Edge / Cloudflare

- Static assets: automatic edge caching.
- Workers: minimize cold starts — avoid heavy npm deps in Worker entry.
- Images: use cache-control headers consistent with build fingerprints.
- Sharp is not available on Workers — use Astro's `noop` image service there.

## Review checklist

- Above-the-fold image preloaded; below-the-fold lazy.
- All images have explicit `width`/`height`.
- No JS framework shipped for a component that could be pure HTML/CSS.
- Islands hydrated with the lightest directive that works.
- Fonts self-hosted, subset, `font-display: swap`.
- Core Web Vitals measured on a realistic field run, not just lab.
