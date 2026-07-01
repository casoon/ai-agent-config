---
name: biome
description: Biome configuration for linting and formatting — single tool replacing ESLint and Prettier, with Astro/Svelte/Tailwind quirks and pre-commit wiring. Use for lint errors, formatting rules, and code-style questions.
---

# Biome

Biome is the single tool for linting and formatting. No ESLint, no Prettier.

## Configuration (`biome.json`)

```json
{
  "$schema": "https://biomejs.dev/schemas/2.4.8/schema.json",
  "files": {
    "includes": ["**/*.js", "**/*.ts", "**/*.mjs", "**/*.cjs",
                 "**/*.json", "**/*.astro", "**/*.svelte", "**/*.css"]
  },
  "formatter": {
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100
  },
  "linter": {
    "rules": {
      "recommended": true,
      "correctness": { "noUnusedVariables": "warn", "noUnusedImports": "warn" },
      "suspicious": { "noExplicitAny": "warn", "noVar": "error" },
      "style": { "useConst": "error" }
    }
  },
  "javascript": {
    "formatter": { "quoteStyle": "single", "trailingCommas": "es5", "semicolons": "always" }
  },
  "json": {
    "formatter": { "trailingCommas": "none" }
  },
  "css": {
    "parser": { "cssModules": false, "tailwindDirectives": true },
    "formatter": { "enabled": true },
    "linter": { "enabled": true }
  }
}
```

## Commands

```bash
pnpm check          # lint + format check (no changes)
pnpm check:fix      # auto-fix lint + format issues
pnpm format         # format only (writes)
```

## Pre-commit hook

Husky + lint-staged runs Biome on staged files only:

```json
"lint-staged": {
  "*.{js,mjs,cjs,ts,tsx,json,astro,svelte,css}": [
    "biome check --write --no-errors-on-unmatched"
  ]
}
```

## Known quirks

### Tailwind CSS directives

`tailwindDirectives: true` in the CSS parser config is required. Without it, Biome reports errors on `@source`, `@theme`, `@apply`, `@custom-variant`, and other Tailwind-specific at-rules.

### `@source` ordering

Biome's `noInvalidPositionAtImportRule` requires `@source` to appear **after** all `@import` statements:

```css
/* Correct */
@import "tailwindcss";
@import "./styles/global.css";
@import "@fontsource/inter/latin-400.css";

@source "./src/components";

/* Wrong — Biome error */
@source "./src/components";
@import "@fontsource/inter/latin-400.css";
```

### False-positive unused imports in `.astro`

Biome cannot see template usage of imports in `.astro` files. Imports used only in the template (not in the frontmatter script) may trigger `noUnusedImports`. Keep the rule at `"warn"`, not `"error"`, to avoid blocking valid code.

### `.svelte` file support

Biome supports `.svelte` for formatting and linting. Runes and `{#if}` blocks are handled correctly.

## Code style

| Rule | Setting | Meaning |
|---|---|---|
| Quotes | Single (`'`) | `import x from 'y'` |
| Semicolons | Always | `const x = 1;` |
| Trailing commas | ES5 | Arrays, objects, parameters |
| Indent | 2 spaces | No tabs |
| Line width | 100 | Max chars per line |
| `const` | Required | `useConst: "error"` |
| `var` | Forbidden | `noVar: "error"` |
| `any` | Warned | `noExplicitAny: "warn"` |

## Fixing common issues

```bash
pnpm check:fix                              # fix everything auto-fixable
npx biome check src/pages/index.astro       # check a single file
npx biome format --write src/app.css        # format a single file
```
