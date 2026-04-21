---
name: seo
description: General SEO patterns for Astro sites — meta tags, Open Graph, canonical URLs, sitemap, robots.txt, JSON-LD WebPage/Article. Use for on-page SEO plumbing, not for LocalBusiness or regional optimization.
---

# SEO

## Page SEO component

Centralize meta tags in a single component slotted into the layout head. Typical props:

| Prop | Type | Notes |
|---|---|---|
| `title` | `string` | Page title, used for `<title>`, OG, Twitter |
| `description` | `string` | Meta description (≤ 160 chars) |
| `canonicalUrl` | `string?` | Defaults to `Astro.url.href` |
| `ogImage` | `string?` | Absolute URL, 1200×630 PNG |
| `ogType` | `'website' \| 'article'?` | Defaults to `website` |
| `twitterCard` | `string?` | Defaults to `summary_large_image` |
| `noIndex` | `boolean?` | Adds `noindex,nofollow` |

Generated output:

- `<title>` and `<meta name="description">`
- `<link rel="canonical">`
- `<meta property="og:title|description|type|url|image">`
- `<meta name="twitter:card|title|description|image">`
- `<script type="application/ld+json">` (WebPage schema)

## Open Graph images

- 1200 × 630 PNG, generated at build time (Satori + resvg is a solid stack).
- One image per page; blog posts derive from frontmatter at build time.
- Reference with absolute URLs: `new URL('/og/page.png', Astro.site).href`.
- Maintain parity across locales — every localized page needs its own OG image.

## Sitemap

Generate `/sitemap.xml` from static routes plus collection entries:

```typescript
import { getCollection } from 'astro:content';

export const GET = createSitemapRoute({
  siteUrl: import.meta.env.SITE,
  pageModules: import.meta.glob('./**/*.astro', { eager: true }),
  getBlogPosts: () => getCollection('blog'),
  blogPrefix: '/blog',
  locales: ['de'],
  exclude: ['/blog/'],
});
```

- Drafts are excluded because `getStaticPaths` filters them — no page is generated, so the sitemap is clean by construction.
- `<urlset>` is the standard root element — include `<lastmod>` where you have a reliable modification date.

## robots.txt

```
User-agent: *
Allow: /

Sitemap: https://example.com/sitemap.xml
```

Must point at the correct absolute sitemap URL and match the configured site.

## Canonical URLs

Auto-resolve from `Astro.url.href`. Override explicitly for:

- Paginated archives pointing at the canonical first page.
- Syndicated content pointing at the original.
- URL parameters that should not fragment ranking signals.

## JSON-LD structured data

Include WebPage schema on every page automatically. For blog posts, set `ogType="article"` for Open Graph; you can still use WebPage schema or upgrade to Article schema with author and dates.

```json
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "Page title",
  "description": "Page description",
  "url": "https://example.com/page"
}
```

For richer schemas (LocalBusiness, Service, FAQ, Breadcrumb) see the `local-business-seo` skill.

## Checklist for new pages

- `<title>` and meta description set via layout props.
- PageSEO with title, description, OG image.
- OG image generated (both locales, where applicable).
- Canonical URL resolves correctly.
- Page appears in sitemap.
- `hreflang` alternates for localized pages.
- Page passes post-build audit (no missing title / description / canonical, no duplicate H1s).
