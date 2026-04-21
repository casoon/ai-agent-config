---
name: local-business-seo
description: Local SEO for company sites — LocalBusiness and Service JSON-LD, geo meta tags, areaServed hierarchy, regional keyword patterns, and the substance-over-keywords ranking approach. Use when adding local schema, regional landing pages, or optimizing for city-level search.
---

# Local business SEO

Patterns for optimizing business websites for local search visibility (e.g. "web development <city>", "SEO agency <city>").

## 1. LocalBusiness JSON-LD (homepage)

```astro
---
// src/components/seo/LocalBusinessSchema.astro
export interface Props {
  name: string;
  description: string;
  url: string;
  telephone: string;
  email?: string;
  foundingDate?: string;
  founder?: { name: string; jobTitle?: string };
  address: {
    street: string;
    city: string;
    postalCode: string;
    region: string;       // full region name, e.g. state/province
    regionCode: string;   // ISO 3166-2, e.g. "DE-XX"
    country: string;      // ISO, e.g. "DE"
  };
  geo: { latitude: number; longitude: number };
  logo?: string;
  image?: string;
  sameAs?: string[];
  openingHours?: string;  // e.g. "Mo-Fr 09:00-17:00"
  priceRange?: string;    // e.g. "€€"
}

const props = Astro.props;

const schema = {
  '@context': 'https://schema.org',
  '@type': 'LocalBusiness',
  '@id': `${props.url}#organization`,
  name: props.name,
  description: props.description,
  url: props.url,
  telephone: props.telephone,
  ...(props.email && { email: props.email }),
  ...(props.foundingDate && { foundingDate: props.foundingDate }),
  ...(props.founder && {
    founder: {
      '@type': 'Person',
      name: props.founder.name,
      ...(props.founder.jobTitle && { jobTitle: props.founder.jobTitle }),
    },
  }),
  address: {
    '@type': 'PostalAddress',
    streetAddress: props.address.street,
    addressLocality: props.address.city,
    postalCode: props.address.postalCode,
    addressRegion: props.address.region,
    addressCountry: props.address.country,
  },
  geo: {
    '@type': 'GeoCoordinates',
    latitude: props.geo.latitude,
    longitude: props.geo.longitude,
  },
  ...(props.logo && { logo: props.logo }),
  ...(props.image && { image: props.image }),
  ...(props.sameAs && { sameAs: props.sameAs }),
  ...(props.priceRange && { priceRange: props.priceRange }),
};
---

<script type="application/ld+json" set:html={JSON.stringify(schema)} />
```

## 2. Geo meta tags (global in BaseHead / BaseLayout)

Emit on every page:

```astro
---
export interface GeoMeta {
  region: string;     // ISO 3166-2, e.g. "DE-XX"
  placename: string;
  latitude: number;
  longitude: number;
}

const geo: GeoMeta = {
  region: 'DE-XX',
  placename: 'City',
  latitude: 0,
  longitude: 0,
};
---

<meta name="geo.region" content={geo.region} />
<meta name="geo.placename" content={geo.placename} />
<meta name="geo.position" content={`${geo.latitude};${geo.longitude}`} />
<meta name="ICBM" content={`${geo.latitude}, ${geo.longitude}`} />
```

Store geo config centrally, e.g. `src/config/business.ts`:

```typescript
export const businessConfig = {
  name: 'Company name',
  city: 'City',
  region: 'Region',
  regionCode: 'DE-XX',
  country: 'DE',
  geo: { latitude: 0, longitude: 0 },
  telephone: '+49-…',
  email: 'info@example.com',
  url: 'https://example.com',
} as const;
```

## 3. `areaServed` hierarchy (service pages)

For each service (web dev, SEO, e-commerce, etc.), emit a `Service` schema with a multi-level `areaServed`:

```astro
---
export interface Props {
  serviceName: string;
  serviceDescription: string;
  serviceUrl: string;
  providerName: string;
  providerUrl: string;
}

const { serviceName, serviceDescription, serviceUrl, providerName, providerUrl } = Astro.props;

const schema = {
  '@context': 'https://schema.org',
  '@type': 'Service',
  name: serviceName,
  description: serviceDescription,
  url: serviceUrl,
  provider: {
    '@type': 'LocalBusiness',
    name: providerName,
    url: providerUrl,
    '@id': `${providerUrl}#organization`,
  },
  areaServed: [
    {
      '@type': 'City',
      name: 'City',
      containedInPlace: { '@type': 'State', name: 'Region' },
    },
    {
      '@type': 'State',
      name: 'Region',
      containedInPlace: { '@type': 'Country', name: 'Country' },
    },
    { '@type': 'Country', name: 'Country' },
  ],
};
---

<script type="application/ld+json" set:html={JSON.stringify(schema)} />
```

## 4. Regional keywords in titles and descriptions

Rules:

- Put the location in the title, preferably near the front. Pattern: `Service City | Brand`.
- Work the location into the description naturally — no keyword stuffing.
- Title ≤ 60 chars, description ≤ 160 chars.
- Brand name at the end after `|`.
- H1 should contain the location. Pattern: `Service in City` or `Service from City`.

Centralize per-page SEO strings:

```typescript
// src/config/seo.ts
export const localSeoPages = {
  home: {
    title: 'Service A & Service B City | Brand',
    description: 'Service A, Service B, and digital systems from City. Modern websites with Astro and Tailwind.',
  },
  serviceA: {
    title: 'Service A City | Modern Solutions | Brand',
    description: 'Service A from City — concrete outcomes with a modern stack.',
  },
  // ...
} as const;
```

## 5. Implementation checklist

### New local site

1. `src/config/business.ts` with company data, geo, contact.
2. `src/config/seo.ts` with per-page localized titles/descriptions.
3. Geo meta tags rendered globally in the layout head.
4. `LocalBusinessSchema` on the homepage.
5. `ServiceSchema` on every service page with `areaServed` hierarchy.
6. Titles/descriptions from `seo.ts` wired into `<PageSEO>`.
7. OG images with regional context.

### Validation

- [Google Rich Results Test](https://search.google.com/test/rich-results) for JSON-LD.
- [Schema.org Validator](https://validator.schema.org/).
- Search Console coverage after deploy.
- Verify `<meta name="geo.*">` in the HTML source.

### E2E pattern

```typescript
test('homepage has LocalBusiness JSON-LD', async ({ page }) => {
  await page.goto('/');
  const jsonLd = await page.locator('script[type="application/ld+json"]').allTextContents();
  const schemas = jsonLd.map((s) => JSON.parse(s));
  const local = schemas.find((s) => s['@type'] === 'LocalBusiness');
  expect(local).toBeDefined();
  expect(local.address.addressLocality).toBeTruthy();
});

test('every page has geo meta tags', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('meta[name="geo.region"]')).toHaveAttribute('content', /.+/);
  await expect(page.locator('meta[name="geo.placename"]')).toHaveAttribute('content', /.+/);
});

test('service pages have areaServed', async ({ page }) => {
  await page.goto('/service-a');
  const jsonLd = await page.locator('script[type="application/ld+json"]').allTextContents();
  const service = jsonLd.map(JSON.parse).find((s) => s['@type'] === 'Service');
  expect(service?.areaServed?.length).toBeGreaterThanOrEqual(3);
});
```

## 6. What actually ranks — three principles

Pages that rank for many local keywords don't do it with black-hat tricks. They do three things consistently.

### 6.1 Substance, not keyword density

The location shows up 20–30 times on a strong service page — but never as repetition. Each occurrence is anchored in a real statement:

> "Service from City for businesses in the region."

Test: remove the location word. Does the sentence still make sense? If yes, it's substance, not stuffing.

### 6.2 Process depth as a trust signal

The strongest pages explain not just *what* you do but *how* — concrete steps, phases, decision points. This demonstrates competence and keeps users on the page (lower bounce, longer dwell).

- 5-step processes with sub-headings.
- Phase 1 / Phase 2 / Phase 3 structure with real decision points.
- Specific over generic: "We check the CMS for X, Y, Z" beats "We analyze your site".

Depth target: ~4,000 words per service page; the strongest pages reach 6,000–8,000.

### 6.3 One landing page per service

Each offering gets its own URL, title tag, and meta description. More entry points, stronger internal linking.

```
/service-a   — own H1, title, description
/service-b   — own H1, title, description
/service-c   — own H1, title, description
```

Not: a single `/services` page with sections for every offering.

## 6.4 Further ranking levers

- LocalBusiness markup (address + contact present).
- BreadcrumbList schema on all subpages.
- FAQ schema on service pages with real recurring questions.
- Flat heading hierarchy: one H1 → 2–4 H2 → H3 detail levels.
- Internal linking — each service page links to related services and the homepage.

### BreadcrumbList schema

```astro
---
export interface Props { items: { name: string; url: string }[]; }
const { items } = Astro.props;

const schema = {
  '@context': 'https://schema.org',
  '@type': 'BreadcrumbList',
  itemListElement: items.map((item, index) => ({
    '@type': 'ListItem',
    position: index + 1,
    name: item.name,
    item: item.url,
  })),
};
---

<script type="application/ld+json" set:html={JSON.stringify(schema)} />
```

### FAQ schema

```astro
---
export interface Props { questions: { question: string; answer: string }[]; }
const { questions } = Astro.props;

const schema = {
  '@context': 'https://schema.org',
  '@type': 'FAQPage',
  mainEntity: questions.map((q) => ({
    '@type': 'Question',
    name: q.question,
    acceptedAnswer: { '@type': 'Answer', text: q.answer },
  })),
};
---

<script type="application/ld+json" set:html={JSON.stringify(schema)} />
```

## 7. i18n notes

- Use the locale-matching form of city/region names on each language variant. City names often stay identical across languages; administrative region names typically get translated.
- JSON-LD `areaServed`: use the language of the document.
- Geo meta tags: language-independent (ISO codes), identical across all language versions.
- `hreflang` covered by sitemap config.
