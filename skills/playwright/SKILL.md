---
name: playwright
description: Playwright E2E patterns for Astro — project setup, static-build servers, navigation/SEO/a11y/i18n/form/theme tests. Use when writing, running, or debugging E2E tests.
---

# Playwright

## Project layout

Keep tests under `e2e/`, grouped per app or feature:

```
e2e/
  <app>/
    a11y.spec.ts
    navigation.spec.ts
    seo.spec.ts
    i18n.spec.ts
    theme.spec.ts
    forms.spec.ts
```

## Configuration

Run each app as its own Playwright project against the static build:

```typescript
// playwright.config.ts
export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  projects: [
    {
      name: 'site',
      use: { ...devices['Desktop Chrome'], baseURL: 'http://localhost:5173' },
      testMatch: 'site/**/*.spec.ts',
    },
  ],
  webServer: [
    { command: 'npx serve dist/client -l 5173', port: 5173, reuseExistingServer: false },
  ],
});
```

Tests require a build first. Web servers serve the static `dist/client/` output — server-side features (form actions, sessions) are not exercisable from E2E against the static build.

## Commands

```bash
pnpm test:e2e                         # everything
pnpm test:e2e --project=site          # single project
playwright test -g "SEO"              # filter by name
playwright test --ui                  # interactive runner
```

## Test patterns

### Navigation

```typescript
import { expect, test } from '@playwright/test';

test.describe('Navigation', () => {
  test('homepage renders', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/.+/);
    await expect(page.locator('h1')).toBeVisible();
  });

  test('contact link works', async ({ page }) => {
    await page.goto('/');
    await page.click('a[href="/contact"]');
    await expect(page).toHaveURL('/contact');
  });
});
```

### SEO

```typescript
test('homepage has OG meta tags', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('meta[property="og:title"]')).toHaveAttribute('content', /./);
  await expect(page.locator('meta[property="og:image"]')).toHaveAttribute('content', /\.png$/);
});

test('robots.txt contains Sitemap', async ({ page }) => {
  const res = await page.goto('/robots.txt');
  expect(res?.status()).toBe(200);
  expect(await res?.text()).toContain('Sitemap:');
});

test('sitemap is valid XML', async ({ page }) => {
  const res = await page.goto('/sitemap.xml');
  expect(res?.status()).toBe(200);
  expect(await res?.text()).toContain('<urlset');
});

test('JSON-LD present', async ({ page }) => {
  await page.goto('/');
  const jsonLd = page.locator('script[type="application/ld+json"]').first();
  await expect(jsonLd).toBeAttached();
  const parsed = JSON.parse((await jsonLd.textContent())!);
  expect(parsed['@context']).toBe('https://schema.org');
});
```

### Accessibility (axe-core)

```typescript
import AxeBuilder from '@axe-core/playwright';

test('homepage has no a11y violations', async ({ page }) => {
  await page.goto('/');
  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag22aa'])
    .analyze();
  expect(results.violations).toEqual([]);
});
```

### i18n

```typescript
test('german homepage has lang="de"', async ({ page }) => {
  await page.goto('/de');
  await expect(page.locator('html')).toHaveAttribute('lang', 'de');
});

test('language switcher navigates', async ({ page }) => {
  await page.goto('/');
  await page.click('a:has-text("DE")');
  await expect(page).toHaveURL('/de');
});
```

### Forms

```typescript
test('contact form renders all fields', async ({ page }) => {
  await page.goto('/contact');
  await expect(page.locator('input[name="name"]')).toBeVisible();
  await expect(page.locator('input[name="email"]')).toBeVisible();
  await expect(page.locator('textarea[name="message"]')).toBeVisible();
  await expect(page.locator('button[type="submit"]')).toBeVisible();
});
```

### Theme toggle

```typescript
test('theme toggle flips dark class', async ({ page }) => {
  await page.goto('/');
  const html = page.locator('html');
  const toggle = page.locator('button[aria-label*="dark" i], button[aria-label*="light" i]');
  await toggle.click();
  await expect(html).toHaveClass(/dark/);
});
```

## Writing new tests

1. Use descriptive `test.describe` groups.
2. Test both locales when the feature is i18n-aware.
3. For SEO tests, verify OG tags, canonical URLs, meta descriptions.
4. For a11y tests, use `AxeBuilder` and expect zero violations.
5. Build before running — E2E serves `dist/client/`, not the dev server.

## Common mistakes

- Forgetting to build first — tests run against the static output.
- `page.waitForNavigation()` — prefer `await expect(page).toHaveURL(...)`.
- Hardcoding ports — use relative URLs; `baseURL` is set per project.
- Testing server-only logic — E2E cannot exercise SSR-only endpoints when running against a static build.
