---
name: i18n
description: Internationalization in Astro — URL-prefix routing, per-locale translation dictionaries, language switcher, localized OG images, and hreflang. Use when adding translations, locales, or language-aware pages.
---

# i18n

## Architecture

Two layers:

1. **Astro i18n routing** — URL prefixing (`/de/contact`).
2. **App-level translations** — `t('key')` per locale.

### Typical locales

- `en` as default without prefix — `/`, `/contact`.
- `de` prefixed — `/de/`, `/de/contact`.

## Astro config

```javascript
// astro.config.mjs
export default defineConfig({
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'de'],
    routing: {
      prefixDefaultLocale: false,  // EN at root, DE at /de/
    },
  },
});
```

## Utilities

```typescript
// Build a locale-prefixed path
localePath('/contact', 'en');  // → '/contact'
localePath('/contact', 'de');  // → '/de/contact'

// Detect locale from URL
getLocaleFromPath('/de/contact');  // → 'de'
getLocaleFromPath('/contact');     // → 'en'

// Swap locale in the current path
switchLocalePath('/de/contact', 'en');  // → '/contact'
switchLocalePath('/contact', 'de');     // → '/de/contact'

// Translation helper
const t = useTranslations(dictionary);
t('nav.home');  // → 'Home'
```

## Translation files

```
src/i18n/
  en.ts       # English
  de.ts       # German
  index.ts    # t() helper wiring
```

```typescript
// src/i18n/en.ts
export default {
  'nav.home': 'Home',
  'nav.contact': 'Contact',
  'home.title': 'My site',
  'contact.title': 'Contact',
  'contact.send': 'Send',
  '404.title': '404 — Page not found',
} as const;
```

```typescript
// src/i18n/index.ts
import type { Locale, Translations } from '@/lib/i18n';
import { useTranslations } from '@/lib/i18n';
import de from './de.js';
import en from './en.js';

const translations: Record<Locale, Translations> = { en, de };

export function t(locale: Locale) {
  return useTranslations(translations[locale]);
}
```

## Page pattern

Each locale gets its own page file:

```
src/pages/
  index.astro           # EN homepage
  contact.astro         # EN contact
  de/
    index.astro         # DE homepage
    contact.astro       # DE contact
```

```astro
---
import { localePath } from '@/lib/i18n';
import { t } from '@/i18n';

const locale = 'de';
const tr = t(locale);

const links = [
  { href: localePath('/', locale), label: tr('nav.home') },
  { href: localePath('/contact', locale), label: tr('nav.contact') },
];
---

<BaseLayout title={tr('home.title')} lang={locale}>
  <Navbar slot="header" links={links}>
    <a href="/contact">EN</a>
  </Navbar>
  <h1>{tr('home.title')}</h1>
</BaseLayout>
```

## Adding a new page (both locales)

1. Create `src/pages/<name>.astro` with `const locale = 'en'`.
2. Create `src/pages/de/<name>.astro` with `const locale = 'de'`.
3. Add translation keys to both `en.ts` and `de.ts`.
4. Add nav links via `localePath('/<name>', locale)`.
5. Add OG image entries for both locales in the OG generator.

## Adding a new locale

1. Add the locale to `astro.config.mjs` (`locales: ['en', 'de', 'fr']`).
2. Extend your `Locale` type (`['en', 'de', 'fr'] as const`).
3. Create `src/i18n/fr.ts` and register it in `src/i18n/index.ts`.
4. Create `src/pages/fr/` and duplicate the localized pages with `const locale = 'fr'`.
5. Update the sitemap config: `locales: { en: 'en', de: 'de', fr: 'fr' }`.
6. Add OG image entries for the new locale.

## Sitemap and hreflang

```javascript
sitemap({
  i18n: {
    defaultLocale: 'en',
    locales: { en: 'en', de: 'de' },
  },
}),
```

The integration emits `<xhtml:link rel="alternate" hreflang="…">` for each localized URL automatically.

## Language switcher pattern

```astro
<!-- On EN pages: link to DE version -->
<a href="/de/contact" class="text-xs font-medium no-underline">DE</a>

<!-- On DE pages: link to EN version -->
<a href="/contact" class="text-xs font-medium no-underline">EN</a>
```

Build the href with `switchLocalePath(Astro.url.pathname, otherLocale)` if you want a switcher that works on any page.
