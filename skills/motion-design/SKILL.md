---
name: motion-design
description: Motion design system for Astro + Tailwind v4 + Svelte 5 — animation tokens, component state patterns, scroll reveals, performance rules, and modern CSS 2025/2026 features. Use this skill whenever adding any animation, transition, hover effect, scroll reveal, micro-interaction, or motion to any component or page. Also use when the user mentions "animation", "transition", "hover effect", "motion", "scroll reveal", "fade in", "entrance animation", "interactive feel", or wants a page to feel "more alive", "more polished", or "like Stripe/Apple/Linear/Vercel".
---

# Motion Design System

Animation is communication. Every motion in the UI must earn its place by answering: does this help the user understand what just happened, where focus is, or what they can do next? If the answer is no, remove it.

## Core principles

1. **Purpose over decoration** — animation guides attention, confirms actions, and reveals hierarchy. It does not add sparkle for its own sake.
2. **Orientation** — motion should reinforce spatial relationships. Things that slide in from the right came from the right. Things that expand grew from a point. Misleading direction confuses.
3. **Speed feels quality** — slow animations feel cheap and in the way. Responsive interfaces feel fast because their transitions are fast.
4. **Mobile first, touch always** — hover effects are an enhancement, not a requirement. Test on touch.
5. **Accessibility is not optional** — `prefers-reduced-motion: reduce` must always be handled. Users with vestibular disorders and epilepsy rely on this. No exceptions.
6. **Core Web Vitals** — animations must never trigger layout (CLS), delay interactivity (INP), or block paint (LCP). Animate only composited properties.

---

## Animation Design Tokens

Define once in the shared CSS entry (`src/styles/app.css` or equivalent). Every component imports these — no ad-hoc `duration-[237ms]` arbitrary values.

```css
@theme {
  /* Durations */
  --duration-instant:  100ms;
  --duration-fast:     150ms;
  --duration-normal:   300ms;
  --duration-slow:     500ms;
  --duration-slower:   700ms;

  /* Easing */
  --ease-standard:   cubic-bezier(0.4, 0, 0.2, 1);   /* material standard */
  --ease-decelerate: cubic-bezier(0, 0, 0.2, 1);      /* entering elements */
  --ease-accelerate: cubic-bezier(0.4, 0, 1, 1);      /* exiting elements */
  --ease-emphasized: cubic-bezier(0.2, 0, 0, 1);      /* Apple/Linear feel */
  --ease-bounce:     cubic-bezier(0.34, 1.56, 0.64, 1); /* spring-like pop */
  --ease-spring:     cubic-bezier(0.175, 0.885, 0.32, 1.275);

  /* Stagger delay multiplier — multiply by child index */
  --stagger-unit: 50ms;
}
```

Use in Tailwind with `transition-[duration:var(--duration-fast)]` or directly in scoped CSS via `var()`.

---

## Performance rules

### Animate ONLY these properties (GPU-composited, zero layout cost)

| Property | Use case |
|---|---|
| `transform` | movement, scale, rotation, skew |
| `opacity` | fade in/out, reveal |
| `filter` | blur, brightness, drop-shadow |
| `clip-path` | shape reveals (GPU in modern browsers) |

### NEVER animate these (trigger layout — kills performance and CLS)

`width`, `height`, `top`, `left`, `right`, `bottom`, `margin`, `padding`, `border-width`, `font-size`, `line-height`

### `will-change` guidance

Add `will-change: transform, opacity` **only** on elements that are known to animate imminently (e.g., a nav drawer that opens). Remove it after the animation with JavaScript. Applying it broadly wastes GPU memory and can slow the page down.

### GPU acceleration

`translateZ(0)` or `translate3d(0,0,0)` forces GPU layer promotion. Use sparingly — only when you observe compositor jank on a real device.

---

## Apple / Linear / Stripe motion rules

Study these sites before inventing something new. Their shared rules:

- **Small movements** — translate by `4px`–`12px` max. Large travel distances feel unprofessional.
- **Scale conservatively** — `scale(1.02)` for hover lift, `scale(1.05)` maximum. Never beyond.
- **No gratuitous rotation** — max `3deg` for a tilt effect. Zero for most components.
- **Shadow is subtle** — animate shadow size and opacity gently; avoid abrupt shadow jumps.
- **Combine opacity + transform** — a fade that also moves `8px` upward reads as intentional, not accidental. A raw opacity fade alone looks like a mistake.
- **Stagger reveals** — grid items, nav links, and list items should enter with a `50ms` offset per item, not all at once.
- **Exits are faster than entrances** — entering: `300ms ease-decelerate`. Exiting: `200ms ease-accelerate`.

---

## Component animation states

Every interactive component defines these eight states. Define them all, even if some are identity transforms. Consistency means no surprises.

| State | CSS trigger | Typical motion |
|---|---|---|
| idle | default | static |
| hover | `:hover` / `group-hover` | lift, glow, scale |
| focus | `:focus-visible` | focus ring, no scale |
| active | `:active` | press-down (scale 0.97) |
| loading | JS class `.is-loading` | spinner, pulse |
| disabled | `[disabled]` / `.is-disabled` | opacity 0.4, no hover |
| enter | `@starting-style` / JS class | fade-up, scale-in |
| exit | JS class `.is-exiting` | fade-out, scale-down |

---

## Button patterns

```css
/* Tailwind v4 @utility — define once, use as class */
@utility btn-motion {
  transition:
    transform var(--duration-fast) var(--ease-standard),
    box-shadow var(--duration-fast) var(--ease-standard),
    background-color var(--duration-fast) var(--ease-standard);

  &:hover:not([disabled]) {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px oklch(0% 0 0 / 15%);
  }

  &:active:not([disabled]) {
    transform: translateY(0) scale(0.97);
    box-shadow: none;
    transition-duration: var(--duration-instant);
  }

  &:focus-visible {
    outline: 2px solid var(--color-primary);
    outline-offset: 3px;
  }

  &[disabled], &.is-disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }
}
```

Loading spinner — avoid layout shift by keeping the button the same size:

```astro
<button class="btn-motion relative" class:list={[isLoading && 'is-loading']}>
  <span class:list={[isLoading ? 'opacity-0' : 'opacity-100', 'transition-opacity duration-150']}>
    {label}
  </span>
  {isLoading && (
    <span class="absolute inset-0 flex items-center justify-center">
      <span class="size-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
    </span>
  )}
</button>
```

---

## Card patterns

```css
@utility card-lift {
  transition:
    transform var(--duration-normal) var(--ease-emphasized),
    box-shadow var(--duration-normal) var(--ease-emphasized);

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 32px oklch(0% 0 0 / 12%);
  }
}

@utility card-glow {
  transition: box-shadow var(--duration-normal) var(--ease-standard);

  &:hover {
    box-shadow: 0 0 0 1px var(--color-primary), 0 8px 24px oklch(from var(--color-primary) l c h / 20%);
  }
}
```

Image zoom within card (contain zoom inside card bounds):

```html
<div class="overflow-hidden rounded-xl">
  <img class="transition-transform duration-500 ease-[--ease-emphasized] group-hover:scale-[1.04]" … />
</div>
```

---

## Navigation patterns

Dropdown — use `@starting-style` for enter + `transition-behavior: allow-discrete` for display toggle:

```css
.dropdown-menu {
  display: none;
  opacity: 0;
  transform: translateY(-6px);
  transition:
    opacity var(--duration-fast) var(--ease-decelerate),
    transform var(--duration-fast) var(--ease-decelerate),
    display var(--duration-fast) allow-discrete;

  @starting-style {
    opacity: 0;
    transform: translateY(-6px);
  }
}

.dropdown-menu.is-open {
  display: block;
  opacity: 1;
  transform: translateY(0);
}
```

Mobile drawer:

```css
.drawer {
  transform: translateX(-100%);
  transition: transform var(--duration-slow) var(--ease-emphasized);

  &.is-open {
    transform: translateX(0);
  }
}
```

Overlay backdrop:

```css
.backdrop {
  opacity: 0;
  transition: opacity var(--duration-normal) var(--ease-standard);

  &.is-open { opacity: 1; }
}
```

---

## Hero entrance sequence

Stagger the headline, paragraph, and CTA with CSS custom property delays. No JavaScript needed.

```astro
---
// Hero.astro
---
<section class="hero">
  <h1 class="hero-headline" style="--delay: 0ms">...</h1>
  <p class="hero-body" style="--delay: 100ms">...</p>
  <a class="hero-cta" style="--delay: 200ms">...</a>
</section>

<style>
  .hero-headline,
  .hero-body,
  .hero-cta {
    animation: fade-up var(--duration-slow) var(--ease-decelerate) var(--delay, 0ms) both;
  }

  @keyframes fade-up {
    from {
      opacity: 0;
      transform: translateY(16px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  @media (prefers-reduced-motion: reduce) {
    .hero-headline,
    .hero-body,
    .hero-cta {
      animation: none;
    }
  }
</style>
```

---

## Scroll animation patterns

### Option A — Scroll-driven animations (CSS only, modern browsers)

No JavaScript, no IntersectionObserver. Uses `animation-timeline: view()`.

```css
.reveal {
  animation: fade-up-reveal linear both;
  animation-timeline: view();
  animation-range: entry 0% entry 30%;
}

@keyframes fade-up-reveal {
  from {
    opacity: 0;
    transform: translateY(24px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

Named view timeline for precise control:

```css
.product-image {
  view-timeline-name: --product;
  view-timeline-axis: block;
}

.product-copy {
  animation: slide-in linear both;
  animation-timeline: --product;
  animation-range: contain 20% contain 60%;
}
```

### Option B — IntersectionObserver (broader support)

For Svelte 5 components, use an action:

```ts
// shared/src/utils/animate.ts
export function reveal(node: Element, { delay = 0, y = 16 } = {}) {
  const motion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (motion) return {};

  node.style.cssText = `opacity:0;transform:translateY(${y}px);transition:opacity 0.5s,transform 0.5s`;

  const io = new IntersectionObserver(([entry]) => {
    if (!entry.isIntersecting) return;
    setTimeout(() => {
      node.style.opacity = '1';
      node.style.transform = 'translateY(0)';
    }, delay);
    io.disconnect();
  }, { threshold: 0.15 });

  io.observe(node);
  return { destroy: () => io.disconnect() };
}
```

```svelte
<script>
  import { reveal } from '$lib/utils/animate';
</script>

<div use:reveal={{ delay: 100 }}>...</div>
```

### Stagger grid

```astro
---
const items = [...];
---
<ul class="grid grid-cols-3 gap-6">
  {items.map((item, i) => (
    <li class="reveal" style={`--delay: ${i * 50}ms`}>
      <Card {item} />
    </li>
  ))}
</ul>
```

### Available patterns

| Pattern | `translateY` | `scale` | `filter` | Notes |
|---|---|---|---|---|
| fade-up | `24px → 0` | — | — | Default for most content |
| fade-left | — | — | — | `translateX(24px → 0)` |
| fade-right | — | — | — | `translateX(-24px → 0)` |
| scale-in | — | `0.92 → 1` | — | Good for cards |
| blur-in | — | — | `blur(8px) → 0` | Hero images |
| product-reveal | `16px → 0` | `0.96 → 1` | — | Combine for product pages |
| timeline-reveal | `8px → 0` | — | — | Items along a timeline |
| stagger-grid | `24px → 0` | — | — | Grid with `--delay` per item |

---

## Modern CSS 2025/2026 features

### `@starting-style` — enter transitions without JavaScript

```css
dialog {
  opacity: 1;
  transform: scale(1);
  transition: opacity 0.2s, transform 0.3s var(--ease-bounce),
    overlay 0.3s allow-discrete, display 0.3s allow-discrete;

  @starting-style {
    opacity: 0;
    transform: scale(0.92);
  }

  &:not([open]) {
    opacity: 0;
    transform: scale(0.92);
  }
}
```

### `transition-behavior: allow-discrete`

Required when transitioning `display` or `visibility` from `none` to `block`. Without it, the element snaps immediately.

```css
.popover {
  display: none;
  transition: opacity 0.2s, display 0.2s allow-discrete;

  &.is-visible {
    display: block;
    opacity: 1;
  }
}
```

### `:has()` for state-based animation

```css
/* Animate card when its checkbox is checked */
.card:has(input:checked) {
  transform: scale(1.02);
  box-shadow: 0 0 0 2px var(--color-primary);
}

/* Stagger only when section is in viewport */
.section:has(.is-visible) .item {
  animation: fade-up 0.4s var(--ease-decelerate) both;
}
```

### `color-mix()` for OKLCH hover tints

```css
.badge {
  background: var(--color-accent);
  transition: background var(--duration-fast);

  &:hover {
    background: color-mix(in oklch, var(--color-accent) 85%, white);
  }
}
```

### CSS Nesting — keep animation rules co-located

```css
.card {
  transition: transform 0.3s, box-shadow 0.3s;

  &:hover { transform: translateY(-4px); }
  &:active { transform: translateY(-1px) scale(0.98); }

  & .card-image {
    transition: transform 0.5s var(--ease-emphasized);
  }

  &:hover .card-image { transform: scale(1.04); }
}
```

---

## Tailwind v4 implementation patterns

### `motion-safe` and `motion-reduce` variants

Always pair these — define the reduced-motion state first as the default, enhance for `motion-safe`:

```html
<!-- Default: instant, motion-safe: animated -->
<div class="opacity-0 motion-safe:animate-fade-up">...</div>

<!-- Or: always show, but remove hover motion for reduce -->
<button class="motion-safe:hover:-translate-y-0.5 motion-safe:transition-transform">...</button>
```

### Custom `@utility` animations

```css
@utility animate-fade-up {
  animation: fade-up var(--duration-slow) var(--ease-decelerate) var(--delay, 0ms) both;
}

@utility animate-scale-in {
  animation: scale-in var(--duration-normal) var(--ease-bounce) var(--delay, 0ms) both;
}

@keyframes fade-up {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}

@keyframes scale-in {
  from { opacity: 0; transform: scale(0.92); }
  to   { opacity: 1; transform: scale(1); }
}
```

### `group-hover` for compound effects

```html
<div class="group card-lift">
  <img class="transition-transform duration-500 group-hover:scale-[1.04] overflow-hidden" />
  <span class="transition-opacity duration-200 opacity-0 group-hover:opacity-100">View</span>
</div>
```

---

## `prefers-reduced-motion` — non-negotiable

Every animation must have a reduced-motion fallback. Use one of these three approaches — pick the one that fits the context:

**CSS media query (scoped styles):**
```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

**Tailwind variant (per element):**
```html
<div class="motion-safe:animate-fade-up">...</div>
```

**JavaScript (runtime check for Svelte actions / JS-driven animations):**
```ts
const prefersReduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
if (prefersReduced) return; // skip animation setup entirely
```

Do not merely slow down animations for reduced-motion — remove them. The preference is about vestibular impact, not aesthetics.

---

## Micro-interaction details (polish)

Exact values — these are thresholds, not suggestions:

- **Never `transition: all`.** Always name the properties: `transition-property: transform, opacity`. `all` animates unintended properties and can trigger layout.
- **Scale on press: `scale(0.96)`.** Never below `0.95` — anything smaller feels exaggerated. (`0.97` idle-press elsewhere in this doc is fine; `0.96` is the tactile default for buttons.)
- **Interruptible vs one-shot.** Use CSS **transitions** for interactive state changes (hover/active/focus) — they can be interrupted mid-flight. Reserve **`@keyframes`** for staged sequences that run once (hero entrance, toast). Don't drive interactive state with keyframes.
- **Icon swaps: cross-fade, don't toggle `display`.** Animate `opacity 0→1`, `scale 0.25→1`, `blur 4px→0`. With a motion library: `spring, duration 0.3, bounce 0` (bounce always 0). Without one: keep both icons in the DOM (one `absolute`) and cross-fade with `cubic-bezier(0.2, 0, 0, 1)`.
- **Skip entrance animation on first paint** where a reveal would otherwise replay on load/tab-restore (e.g. `initial={false}` in AnimatePresence). Reveals must enhance already-visible content — never gate visibility on a transition that pauses on hidden tabs.

## Quality checklist

Before delivering any animation code, verify each item:

- [ ] **Purposeful** — does this motion communicate something the user needs to know?
- [ ] **GPU-only** — animates only `transform`, `opacity`, `filter`, or `clip-path`
- [ ] **Reduced-motion handled** — fallback defined at CSS, Tailwind, or JS layer
- [ ] **Duration on-token** — uses `--duration-*` variables, not arbitrary values
- [ ] **Scale within bounds** — `≤ scale(1.05)` for hover, `≤ scale(1.02)` for idle pulse
- [ ] **Movement within bounds** — translate `≤ 12px` except for intentional drawer/modal slides
- [ ] **Touch-friendly** — hover effects are additive, not required for usability
- [ ] **No layout animation** — no `width`, `height`, `margin`, `padding`, `top`, `left`
- [ ] **Exit faster than enter** — exit transition `≤ 66%` of enter duration
- [ ] **No will-change abuse** — only on elements that will animate within 100ms
