---
name: svelte-5
description: Svelte 5 Runes for interactive islands in Astro — $state, $derived, $effect, $props, event syntax, shared state in .svelte.ts. Use when creating or modifying Svelte 5 components.
---

# Svelte 5

## Role

Svelte 5 is used for **interactive islands** hydrated via Astro's `client:*` directives. Keep Svelte components focused on actual interactivity; leave presentational markup in `.astro`.

## Runes API

Svelte 5 replaces stores and reactive declarations with Runes.

```svelte
<script lang="ts">
  let count = $state(0);
  let doubled = $derived(count * 2);

  $effect(() => {
    console.log('count changed:', count);
  });
</script>
```

### Runes reference

| Svelte 4 | Svelte 5 | Notes |
|---|---|---|
| `let x = 0` (reactive) | `let x = $state(0)` | Explicit reactivity |
| `$: doubled = x * 2` | `let doubled = $derived(x * 2)` | Computed values |
| `$: { sideEffect() }` | `$effect(() => { sideEffect() })` | Side effects |
| `export let prop` | `let { prop } = $props()` | Component props |
| `$$restProps` | `let { ...rest } = $props()` | Rest props |
| `on:click={handler}` | `onclick={handler}` | All DOM events |
| `createEventDispatcher()` | Callback props | Custom events |
| `writable()` store | `$state()` in `.svelte.ts` | Shared state |

## Component patterns

### Basic interactive component

```svelte
<script lang="ts">
  let { label, variant = 'default' }: { label: string; variant?: 'default' | 'primary' } = $props();
  let active = $state(false);
</script>

<button
  onclick={() => (active = !active)}
  class="btn"
  class:active
  type="button"
>
  {label}
</button>

<style>
  .btn { /* scoped styles */ }
  .active { /* active state */ }
</style>
```

### Side effects (DOM access)

```svelte
<script lang="ts">
  let isDark = $state(false);

  $effect(() => {
    isDark = document.documentElement.classList.contains('dark');
  });
</script>
```

### Shared reactive state

```typescript
// src/lib/state/counter.svelte.ts
let count = $state(0);
export function getCount() { return count; }
export function increment() { count++; }
```

Files using Runes outside of components must end in `.svelte.ts` (or `.svelte.js`).

## Astro integration

### Hydration directives

```astro
<ThemeToggle client:load />      <!-- immediate, interactive from first paint -->
<Newsletter client:idle />       <!-- defer until idle -->
<Comments client:visible />      <!-- hydrate when in viewport -->
<StaticChart />                  <!-- no hydration, static render only -->
```

### Config

```javascript
// astro.config.mjs
import svelte from '@astrojs/svelte';

export default defineConfig({
  integrations: [
    svelte({ compilerOptions: { runes: true } }),
  ],
});
```

`runes: true` enables Runes for all `.svelte` files globally.

## Styling

- `<style>` blocks for component-scoped CSS.
- Reference design tokens via `var(--color-text)` and friends.
- Tailwind utility classes work in the template section.
- `:global(...)` for styling slotted or external content.

```svelte
<style>
  .toggle {
    color: var(--color-text);
    border: 1px solid var(--color-border);
    border-radius: var(--button-radius);
    transition: background-color var(--transition-fast);
  }
  .toggle:hover { background: var(--color-bg-secondary); }
</style>
```

## Common mistakes

- Using `on:click` — it's `onclick` (lowercase, no colon).
- Using `export let` — use `$props()` destructuring.
- Using `$:` reactive declarations — use `$derived()` or `$effect()`.
- Using stores — use `$state()` in `.svelte.ts`.
- Using `createEventDispatcher` — pass callback props instead.
- Forgetting `lang="ts"` on `<script>`.
