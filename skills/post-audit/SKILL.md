---
name: post-audit
description: Post-build SEO / link / a11y audit via @casoon/astro-post-audit — integration setup, options, what it checks, and how to fix common findings. Use when wiring up build audits or resolving audit failures.
---

# Post-audit

[`@casoon/astro-post-audit`](https://github.com/casoon/astro-post-audit) is a fast post-build auditor for Astro sites. It runs a Rust binary against the build output and checks for SEO, link, and lightweight WCAG issues. It runs automatically after every `astro build` via the `astro:build:done` hook.

## Integration

```javascript
// astro.config.mjs
import postAudit from '@casoon/astro-post-audit';

export default defineConfig({
  integrations: [
    postAudit(),                                    // defaults
    // or with options:
    // postAudit({ exclude: ['blog/index.html'] }),
  ],
});
```

## Options

| Option | Type | Default | Description |
|---|---|---|---|
| `site` | `string?` | auto from `config.site` | Base URL for link validation |
| `strict` | `boolean?` | `false` | Treat warnings as errors |
| `format` | `'text' \| 'json'?` | `'text'` | Output format |
| `config` | `string?` | — | Path to a `rules.toml` config file |
| `exclude` | `string[]?` | — | Glob patterns to exclude from the audit |
| `noSitemapCheck` | `boolean?` | `false` | Skip sitemap checks |
| `checkAssets` | `boolean?` | `false` | Enable asset reference checking |
| `checkStructuredData` | `boolean?` | `false` | Enable structured-data validation |
| `checkSecurity` | `boolean?` | `false` | Enable security heuristics |
| `checkDuplicates` | `boolean?` | `false` | Enable duplicate-content detection |
| `disable` | `boolean?` | `false` | Disable the integration entirely |

## What it checks

- Missing or duplicate `<title>`.
- Missing `<meta name="description">`.
- Missing canonical URLs.
- Missing Open Graph tags.
- Multiple `<h1>` elements per page.
- Broken internal links.
- Sitemap validity.
- Empty HTML files (0 bytes).
- Basic WCAG heuristics: missing `alt`, empty links, missing skip link, missing form labels.

## Fixing common findings

### Missing canonical on 404 pages

Add a `<PageSEO>` with `noIndex`:

```astro
---
import PageSEO from '@/components/seo/PageSEO.astro';
---

<BaseLayout title="404 — Page not found" lang="en">
  <PageSEO slot="head"
           title="404 — Page not found"
           description="The page you are looking for does not exist."
           noIndex />
</BaseLayout>
```

### Multiple `<h1>` in MDX blog posts

If the layout renders `frontmatter.title` as `<h1>`, don't add another `# Heading` at the top of MDX. Start the post body at `## Subheading`.

### Empty HTML files (0 bytes)

These come from `Astro.redirect()` in SSG mode. Exclude them:

```javascript
postAudit({ exclude: ['blog/index.html'] });
```

## CLI usage

The binary can be used standalone:

```bash
npx @casoon/astro-post-audit dist/client --site https://example.com
npx @casoon/astro-post-audit dist/client --exclude "blog/index.html" --strict
```

## Binary installation

The Rust binary is downloaded automatically during `npm install` via a `postinstall` script. Supported platforms: macOS (x64, arm64), Linux (x64, arm64), Windows (x64). If the download fails (e.g. no internet), the integration warns and skips the audit gracefully.
