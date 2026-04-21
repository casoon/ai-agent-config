---
name: mdx-content
description: MDX + Content Collections patterns for Astro v6 — Loader API, frontmatter schemas, rendering, remark-directive pitfalls, and blog post workflow. Use when adding MDX content, schemas, or collection queries.
---

# MDX content

## Content Collections (Astro v6 Loader API)

### Collection definition

```typescript
// src/content.config.ts  (NOT src/content/config.ts)
import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const blog = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/blog' }),
  schema: z.object({
    title: z.string().min(1).max(100),
    description: z.string().min(10).max(160),
    date: z.coerce.date(),
    author: z.string().default('Editorial team'),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
  }),
});

export const collections = { blog };
```

### v5 → v6 changes

| v5 | v6 |
|---|---|
| `src/content/config.ts` | `src/content.config.ts` |
| `type: 'content'` | `loader: glob({ … })` |
| `entry.slug` | `entry.id` |
| `entry.render()` | `render(entry)` (standalone import) |
| `getEntryBySlug()` | `getEntry()` |
| `import { z } from 'astro:content'` | `import { z } from 'astro/zod'` |

## Frontmatter

```yaml
---
title: 'Welcome to the blog'
description: 'The first post, using MDX and Content Collections.'
date: 2026-02-24
author: 'Editorial team'
tags: ['astro', 'template']
draft: false
---
```

- `title`: 1–100 chars, required.
- `description`: 10–160 chars, required (feeds meta description + OG).
- `date`: coerced to Date, required.
- `tags`: string array, defaults to `[]`.
- `draft`: boolean; drafts are filtered out of the listing and the sitemap.

## Querying collections

### List posts (excluding drafts)

```astro
---
import { getCollection } from 'astro:content';

const posts = (await getCollection('blog'))
  .filter((post) => !post.data.draft)
  .sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());
---
```

### Static paths

```astro
---
import { getCollection, render } from 'astro:content';

export async function getStaticPaths() {
  const posts = (await getCollection('blog')).filter((post) => !post.data.draft);
  return posts.map((post) => ({
    params: { slug: post.id },
    props: { post },
  }));
}

const { post } = Astro.props;
const { Content } = await render(post);
---

<article>
  <h1>{post.data.title}</h1>
  <Content />
</article>
```

### Single entry

```typescript
import { getEntry, render } from 'astro:content';

const post = await getEntry('blog', 'welcome');
const { Content } = await render(post);
```

## Writing MDX

```mdx
---
title: 'My post'
description: 'A post with components.'
date: 2026-02-25
tags: ['example']
---

# Heading

Regular markdown text with **bold** and *italic*.

## Code

```typescript
const greeting = 'Hello';
```
```

## remark-directive pitfalls

If the pipeline includes `remark-directive`, text in the form `:name` is parsed as a directive. This trips up common patterns in prose (not in code blocks).

### Problem

`:word` or `:digit` in prose can be interpreted as a text directive and rendered unexpectedly.

### Affected patterns

| Problematic | Safer replacement |
|---|---|
| `1:1 meeting` | `1-to-1 meeting` |
| `4.5:1 contrast` | `4.5 to 1 contrast` |
| `16:9 format` | `16-to-9 format`, or `16∶9` (ratio U+2236) |
| `2:3 ratio` | `2-to-3 ratio` |
| Time `10:00` | Inline code `` `10:00` `` or `10.00 UTC` |

### Safe contexts

- Fenced code blocks (` ```lang … ``` `) — directives are not parsed inside.
- Inline code (`` `text` `` ).
- Raw HTML tags (`<p>4.5:1</p>`) — not parsed as Markdown.
- Table cells are usually safe, but wrap in inline code when unsure.

### Writing rules

1. Never write `X:Y` ratios in prose — reword or inline-code them.
2. Time in prose: `10.00 UTC` or `` `10:00` ``.
3. Port numbers (`:3000`, `:8080`) only inside code blocks / inline code.
4. Tag-like `tag:server` strings always in inline code: `` `tag:server` ``.
5. Shortcodes `:smile:` are parsed as directives — do not use them.

## Styling MDX content

Render inside a `.post-content` wrapper with `:global()` selectors:

```css
.post-content :global(h2) { font-size: 1.5rem; font-weight: 700; }
.post-content :global(h3) { font-size: 1.25rem; font-weight: 600; }
.post-content :global(p)  { margin-bottom: var(--space-md); }
.post-content :global(code) { font-family: var(--font-mono); }
.post-content :global(pre)  { border-radius: var(--radius-lg); }
```

## Adding a new post

1. Create `src/content/blog/my-post.mdx`.
2. Fill in the required frontmatter (`title`, `description`, `date`).
3. Write content in Markdown / MDX.
4. Run the build — OG image is generated from frontmatter.
5. Post appears at `/blog/my-post`.

## RSS feed

Generate `/rss.xml` from the blog collection, filtering drafts and sorting by date descending. Keep the feed URL referenced from the homepage `<head>` via `<link rel="alternate" type="application/rss+xml" …>`.
