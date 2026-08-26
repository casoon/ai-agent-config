---
name: native-html-ui
description: Native browser/HTML features that replace common JS-library UI patterns — popover API, <details name> accordion groups, <dialog> modals, declarative Shadow DOM, fetchpriority, and <datalist> autocomplete. Use this BEFORE reaching for a JS library or hand-rolled component whenever building a modal, popover, tooltip, dropdown, accordion/FAQ, autocomplete input, or a Web Component — check whether plain HTML/CSS already solves it with less code, better accessibility, and no bundle-size cost. Also relevant when reviewing UI code that manually implements focus traps, click-outside listeners, or z-index stacking for overlays.
---

# Native HTML UI features

Browsers now ship declarative primitives for UI patterns that used to require a JS library. Before pulling in a library or writing custom JS for a modal, popover, accordion, or autocomplete, check if one of these covers it. They're mostly free: less JS shipped, native keyboard/focus handling, native top-layer stacking (no z-index fights).

Support is broad across current evergreen browsers (Chrome/Edge, Firefox, Safari) as of 2026 for all six features below. Still worth a quick caniuse check if the project has a hard requirement on older browsers — these are the newest primitives in this list, so check first: Declarative Shadow DOM and the Popover API.

## Decision guide

| Need | Reach for | Not |
|---|---|---|
| Floating menu/tooltip that must sit above everything, dismiss on outside click/ESC | `popover` attribute | Popper.js, Floating UI, custom z-index+click-outside JS |
| FAQ/accordion where only one item is open at a time | `<details name="group">` | Accordion component, `useState` open-index |
| Modal dialog with focus trap, ESC-to-close, backdrop | `<dialog>` + `showModal()` | Custom `<div>` overlay + focus-trap library |
| Server-rendered Web Component with no FOUC/hydration flash | `<template shadowrootmode="open">` | Client-only `attachShadow()` |
| Hint the browser which image/script to fetch first (LCP) | `fetchpriority="high"` | Manual preload juggling |
| Text input with suggestions but still free-form | `<datalist>` | react-select / downshift for simple cases |

## 1. Popover API

```html
<button popovertarget="my-menu">Toggle Menu</button>

<div id="my-menu" popover>
  <p>Native top-layer, light-dismiss on outside click / ESC.</p>
</div>
```

- `popovertarget` on the trigger wires click-to-toggle automatically — no JS.
- The element gets promoted to the browser's top layer, so it renders above everything regardless of CSS `z-index`. No stacking-context debugging.
- `popover="manual"` disables light-dismiss if you need to control open/close yourself (e.g. `el.showPopover()` / `hidePopover()`).
- Astro: this is plain HTML behavior, survives View Transitions without any script — no `astro:page-load` wiring needed since there's no JS state to re-init.

## 2. Accordion groups via `<details name="...">`

```html
<details name="faq">
  <summary>What is modern HTML?</summary>
  <p>A living standard evolving directly inside browser engines.</p>
</details>

<details name="faq">
  <summary>Do I still need JavaScript?</summary>
  <p>Much less of it than you used to.</p>
</details>
```

Give multiple `<details>` elements the same `name` and the browser enforces "only one open at a time" — the classic accordion behavior — with zero JS state. Different `name` values create independent groups on the same page.

Gotcha: this is exclusive-open only (radio-button semantics). If the design needs multiple sections open simultaneously, just omit `name` and use plain `<details>` — don't fight the grouping behavior with JS.

## 3. Modals via `<dialog>`

```html
<dialog id="user-modal">
  <h2>Confirm Action</h2>
  <form method="dialog">
    <button value="cancel">Cancel</button>
    <button value="confirm">Delete</button>
  </form>
</dialog>

<button onclick="document.getElementById('user-modal').showModal()">
  Open Modal
</button>
```

```css
dialog::backdrop {
  background-color: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
}
```

- `.showModal()` (not `.show()`) is what gives you the modal behavior: top-layer rendering, inert background, native focus trap, and ESC-to-close.
- `<form method="dialog">` closes the dialog automatically on submit and sets `dialog.returnValue` to the clicked button's `value` — no manual close handler needed for the common case.
- `.show()` (non-modal) does NOT trap focus or disable the background — use `.showModal()` unless you specifically want a non-modal dialog.
- Astro: `showModal()`/`close()` calls live in a regular `<script>`, not `is:inline` — see the `astro-client-scripts` skill for the scoped-script-over-inline rule. If the trigger button and dialog persist across View Transitions, listen on `astro:page-load` to re-attach the open handler after SPA navigation.

## 4. Declarative Shadow DOM

```html
<user-card>
  <template shadowrootmode="open">
    <style>
      h3 { color: #3b82f6; }
    </style>
    <h3>Jane Doe</h3>
    <p>Senior Frontend Engineer</p>
  </template>
</user-card>
```

The browser parses `<template shadowrootmode="open">` and attaches it as a shadow root during HTML parsing — before any JS runs. This is what makes SSR/SSG of Web Components work without a hydration flash (previously `attachShadow()` had to run client-side, causing FOUC).

Mainly relevant if the project hand-rolls custom elements (`customElements.define`) rather than Astro/Svelte components — for ordinary Astro component encapsulation, scoped `<style>` already handles this without touching Shadow DOM at all. Reach for this only when a real Web Component (used outside Astro, e.g. embedded widget) is the actual requirement.

## 5. `fetchpriority`

```html
<img src="hero-banner.webp" fetchpriority="high" alt="Product Hero">
<img src="avatar.webp" fetchpriority="low" alt="User avatar">
<script src="app.js" fetchpriority="high"></script>
```

Explicit hint to the browser's network scheduler about resource importance — complements `loading="lazy"` and `async`/`defer`, doesn't replace them. Use `fetchpriority="high"` on the actual LCP element (usually the hero image) when the browser's default heuristic guesses wrong, and `low` on non-critical images competing for bandwidth early in the load. Don't mark everything `high` — that defeats the point.

## 6. Native autocomplete via `<datalist>`

```html
<label for="framework">Choose or type a framework:</label>
<input list="frameworks" id="framework" name="framework" placeholder="e.g. Next.js">

<datalist id="frameworks">
  <option value="Next.js"></option>
  <option value="SvelteKit"></option>
  <option value="Astro"></option>
</datalist>
```

Zero-JS suggestion list that still allows free-text entry — the browser handles filtering, keyboard nav, and OS-native styling. Good fit for "suggest but don't restrict" inputs. Not a full replacement for combobox components that need custom rendering per option (icons, descriptions, async search) — those still need a real JS component (e.g. `<Combobox>`-style ARIA pattern).

## When NOT to reach for these

- Need custom rendering inside options (icons, multi-line, async-loaded suggestions) → `<datalist>` isn't enough, build a proper combobox.
- Need multiple dialogs open simultaneously, or non-modal floating panels with complex positioning logic (anchoring to a specific element, flipping on overflow) → Popover API's anchor positioning is more limited than Floating UI; check if `popover` + CSS anchor positioning covers the case before reaching for a library.
- Old custom-element codebase already using imperative `attachShadow()` client-side → no need to migrate existing working code to declarative Shadow DOM just for its own sake.
