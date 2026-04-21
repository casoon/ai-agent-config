---
name: astro-architecture
description: Astro v6 architecture — rendering strategy, routing, Content Collections Loader API, Zod v4 schemas, API routes, islands, and Node 22+ setup. Use when working on Astro pages, layouts, or configuration.
---

# Astro architecture

## Goals

- Server-first, static-friendly by default.
- Minimize shipped client-side JavaScript.
- Use islands intentionally, not by default.
- Be explicit about SSG vs SSR vs hybrid per route.

## Structure

- `src/pages` for route entry points — keep files slim.
- `src/layouts` for page shells.
- `src/components` for reusable UI.
- `src/content` for structured editorial content.
- `public` for static assets that skip the module graph.

## Rules

- Prefer `.astro` components for presentational UI.
- Use framework components (Svelte, React, Vue) only where client-side interaction is actually needed.
- Move logic into utilities or domain modules — keep route files thin.
- Reuse layouts and content schemas instead of duplicating page logic.
- Cover SEO-critical metadata on every public page.

## Astro v6 API

### Content Collections — Loader API

```typescript
// src/content.config.ts  (NOT src/content/config.ts)
import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const blog = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    // Zod v4 top-level validators
    email: z.email(),   // not z.string().email()
    website: z.url(),   // not z.string().url()
  }),
});

export const collections = { blog };
```

### Rendering content

```astro
---
import { getCollection, render } from 'astro:content';

const posts = await getCollection('blog');
const { Content } = await render(post);  // not post.render()
---

<a href={`/blog/${post.id}`}>{post.data.title}</a>  <!-- id, not slug -->
```

### Zod v4 syntax

```typescript
import { z } from 'astro/zod';  // not from 'astro:content' or 'astro:schema'

z.email()   // instead of z.string().email()
z.url()     // instead of z.string().url()
z.uuid()    // instead of z.string().uuid()

z.string().min(5, { error: 'Too short.' });      // 'error', not 'message'
z.string().transform(Number).default(0);         // default matches output type
```

### Removed / renamed APIs (v5 → v6)

| Old | New |
|---|---|
| `Astro.glob()` | `import.meta.glob()` |
| `ViewTransitions` | `ClientRouter` |
| `getEntryBySlug()` | `getEntry()` |
| `post.render()` | `render(post)` |
| `entry.slug` | `entry.id` |
| `emitESMImage` | `emitImageMetadata` |
| `src/content/config.ts` | `src/content.config.ts` |
| `handleForms` prop on `ClientRouter` | default behavior |

## Component patterns

### Astro component

```astro
---
export interface Props {
  title: string;
  variant?: 'default' | 'primary';
}

const { title, variant = 'default' } = Astro.props;
---

<section>
  <h2>{title}</h2>
  <slot />
</section>
```

### Hydration directives

- `client:load` — immediate (navbar, theme toggle).
- `client:idle` — browser idle (secondary features).
- `client:visible` — in viewport (footer widgets, comments).
- omit directive — static render only.

### API route

```typescript
import type { APIRoute } from 'astro';
import { z } from 'astro/zod';

const schema = z.object({
  email: z.email(),
  name: z.string().min(1),
});

export const POST: APIRoute = async ({ request }) => {
  try {
    const data = await request.json();
    const parsed = schema.safeParse(data);
    if (!parsed.success) {
      return new Response(JSON.stringify({ error: parsed.error.flatten() }), { status: 400 });
    }
    return new Response(JSON.stringify({ ok: true }), { status: 200 });
  } catch {
    return new Response('Invalid request', { status: 400 });
  }
};
```

## Configuration

### astro.config.mjs

```javascript
import { defineConfig } from 'astro/config';
import svelte from '@astrojs/svelte';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  site: 'https://example.com',
  integrations: [
    svelte({ compilerOptions: { runes: true } }),
  ],
  vite: {
    plugins: [tailwindcss()],
    ssr: { noExternal: ['@fontsource/*'] },
  },
  build: { inlineStylesheets: 'auto' },
});
```

## Node requirement

Astro v6 requires Node >= 22.12.0. Older versions are not supported.

## New stable features (promoted from experimental)

- **Live Content Collections** — real-time data without rebuild.
- **Content Security Policy** — automatic CSP headers.
- **Vite Environment API** — dev server matches production runtime.

## Astro 6.1 additions

### Sharp image service config

Codec-specific encoder options (only for `astro/assets/services/sharp`, not `noop`):

```javascript
image: {
  service: {
    entrypoint: 'astro/assets/services/sharp',
    config: {
      webp: { effort: 6, alphaQuality: 90 },
      avif: { effort: 4, chromaSubsampling: '4:2:0' },
      jpeg: { mozjpeg: true },
      png:  { compressionLevel: 8 },
    },
  },
},
```

Per-image `quality` prop still takes precedence over `config` defaults. Cloudflare Workers does not support Sharp — use `noop` there.

### SmartyPants options object

```javascript
markdown: {
  smartypants: {
    dashes: 'oldschool', // -- → en-dash, --- → em-dash
    ellipses: true,      // ... → …
    backticks: false,
    quotes: true,        // "hello" → curly quotes
  },
},
```

### i18n `fallbackRoutes` in integrations

When `fallbackType: 'rewrite'` is set, integrations can read fallback routes via the `astro:routes:resolved` hook:

```typescript
{
  name: 'my-integration',
  hooks: {
    'astro:routes:resolved': ({ routes }) => {
      const fallbacks = routes.filter((r) => r.fallbackRoutes?.length);
    },
  },
}
```

### Notable 6.1 bugfixes

- CSRF `checkOrigin` reads `X-Forwarded-Proto` behind reverse proxies.
- Cloudflare `server:defer` dev crash fixed.
- Middleware HMR: changes detected in dev server.
- Warning when Vite 8 is hoisted (Astro requires Vite 7).
- `ClientRouter` skips animations when the browser supplies a native transition.

## Review checklist

- Is hydration avoidable for this component?
- Is content modeled as a collection with a schema, not ad-hoc?
- Is the component boundary clear (server-rendered vs island)?
- Are SEO basics covered — title, description, canonical, OG?
- Is the rendering mode of the page explicit (static vs on-demand)?
