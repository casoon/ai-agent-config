---
name: webspire
description: Webspire MCP integration for UI patterns, CSS snippets, and design tokens — hero/pricing/FAQ patterns, scroll/hover/glass snippets, three-layer token system. Use when enhancing pages with Webspire patterns or querying the registry via MCP.
---

# Webspire MCP integration

[Webspire](https://www.webspire.de) is a curated UI pattern and snippet registry. The MCP server (`@webspire/mcp`, [casoon/webspire](https://github.com/casoon/webspire)) exposes the registry as tools.

## MCP tools

| Tool | Purpose |
|---|---|
| `search_patterns` / `get_pattern` | UI patterns — hero, pricing, FAQ, tabs, cards, steps, etc. |
| `search_snippets` / `get_snippet` | CSS snippets — glass, scroll, hover, easing, surfaces |
| `search_templates` / `get_template` | Full page templates |
| `search_canvas_effects` / `get_canvas_effect` | Canvas/WebGL effects |
| `search_motion_recipes` / `get_motion_recipe` / `list_motion_recipes` | Motion recipes |
| `recommend_snippet` | Context-based recommendations |
| `recommend_token_mapping` | Map brand colors to Webspire tokens |
| `recommend_fonts` | Font pairing suggestions |
| `setup_tokens` | Generate token CSS for a brand |
| `list_pattern_families` / `list_categories` | Browse the registry |
| `list_design_skills` / `get_design_skill` / `recommend_design_skill` | Design skill resources |
| `list_templates` | Browse templates |
| `augment_page` / `compose_page` | Higher-level page composition helpers |

## Token system (three layers)

### Layer 1 — base tokens

Generic CSS custom properties from Webspire. Install via `setup_tokens` or copy from the registry.

```css
:root {
  --ws-color-surface: #ffffff;
  --ws-color-text: #0f172a;
  --ws-color-text-soft: #334155;
  --ws-color-primary: #4f46e5;
  --ws-color-accent: #06b6d4;
  /* plus semantic, radius, shadow tokens */
}
```

### Layer 2 — brand mapping

Override base tokens with brand values:

```css
:root {
  --ws-color-primary: #your-brand-color;
  --ws-color-accent:  #your-accent-color;
  --ws-color-surface: #your-background;
}
```

Use `recommend_token_mapping` to derive this layer from a brand palette.

### Layer 3 — component tokens

Patterns use component-scoped tokens that inherit from the base tokens:

```css
.ws-hero { --ws-hero-bg: var(--ws-color-surface); }
.ws-faq  { --ws-faq-bg:  var(--ws-color-surface); }
```

## Common CSS snippets

### Scroll reveal

```css
.scroll-reveal {
  animation: scroll-reveal linear both;
  animation-timeline: view();
  animation-range: entry 0% entry 30%;
}
```

Add `.scroll-reveal` to sections that should fade in on scroll.

### Hover lift

```css
.hover-lift {
  transition: transform 0.25s var(--ease-spring), box-shadow 0.25s var(--ease-spring);
}
.hover-lift:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px oklch(0 0 0 / 0.2);
}
```

Note: parent containers need `padding-bottom: 1.5rem` for the shadow to be visible.

### Shine sweep, border draw, spotlight, stagger children

- `.shine-sweep` — shimmer on hover (add the class).
- `.border-draw` — animated border from corners; trigger programmatically via `.is-drawing`.
- `.spotlight-card` — radial light follows cursor; set `--spotlight-x/y` via `onmousemove`.
- `.stagger-children` — sequential fade-in of child elements (add to parent).

## Easing tokens

```css
:root {
  --ease-spring: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);
  --ease-smooth: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-snappy: cubic-bezier(0.2, 0, 0, 1);
}
```

## Glass effects

Available via MCP: `glass/frosted`, `glass/subtle`, `glass/bold`, `glass/colored`, `glass/dark`.

```html
<div class="glass-colored rounded-xl p-6" style="--glass-hue: 220">
  Blue tinted glass
</div>
```

## Pattern integration (Astro)

1. Query the MCP for pattern HTML/CSS.
2. Adapt to Astro — convert to `.astro` with a `Props` interface.
3. Use Tailwind utilities where possible, Webspire tokens for custom properties.
4. Add dark mode via the `.dark` class or `@media (prefers-color-scheme: dark)`.
5. Add `prefers-reduced-motion: reduce` for every animation.

## Accessibility

All Webspire snippets include:

- `@media (prefers-reduced-motion: reduce)` handlers.
- `aria-hidden="true"` on decorative elements.
- `:focus-visible` support for interactive patterns.

Keep those guarantees intact when adapting snippets into components.
