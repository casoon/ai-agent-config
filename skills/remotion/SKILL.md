---
name: remotion
description: Remotion workflow for animated explainer videos embedded in Astro sites — composition setup, render pipeline (ProRes → MP4 → WebP poster), frontmatter integration, and Astro component embedding. Use when building or integrating Remotion videos into an Astro project.
---

# Remotion

Remotion renders React components to video. Typical use: short animated
explainers (30–120 s) embedded as hero elements in articles or landing pages.

## Composition setup

Register in `src/Root.tsx`:

```tsx
<Composition
  id="MyCompositionId"
  component={MyComponent}
  defaultProps={{}}
  durationInFrames={900}
  fps={30}
  width={1920}
  height={1080}
/>
```

Standard spec: **1920×1080, 30 fps**. Duration: 30 s = 900 frames, 60 s = 1800 frames.

Use `interpolate` with `extrapolateLeft/Right: 'clamp'` for all animations.
Crossfade scenes with a 10–12 frame overlap.

## Render pipeline

Always render a ProRes master first, then derive MP4 from it — never render
MP4 directly (lower quality, no intermediate for re-encoding):

```bash
npm run render:final -- <CompositionId>
```

Expected output in `out/<CompositionId>/`:

| File | Purpose |
|---|---|
| `master.mov` | ProRes master — internal only, do not deploy |
| `720p.mp4` | H.264 delivery file |
| `poster-720p.png` | Frame at ~2 s — convert to WebP before deploying |

Typical sizes for a 30 s animation: 720p MP4 ≈ 500 KB–2 MB. No CDN needed below ~4 MB.

## Poster conversion

PNG frames are large (600 KB–1 MB). Convert to WebP immediately:

```bash
cwebp -q 85 out/<CompositionId>/poster-720p.png -o out/<CompositionId>/poster-720p.webp
```

Typical WebP result: 15–40 KB.

## Astro frontmatter integration

Add video fields to the content schema (`content.config.ts`):

```typescript
heroVideo:       z.string().optional(),
heroVideoPoster: z.string().optional(),
```

Reference in MDX frontmatter:

```yaml
heroVideo: '/videos/<CompositionId>/720p.mp4'
heroVideoPoster: '/videos/<CompositionId>/poster-720p.webp'
```

Keep a separate `teaserImage` for OG/social — video poster is not a substitute.

## Embedding in Astro

Minimal inline embed:

```astro
{heroVideo && (
  <video
    src={heroVideo}
    poster={heroVideoPoster}
    autoplay muted loop playsinline
    aria-label="Animated explainer"
  />
)}
```

For a reusable component, accept `src`, `poster`, `title`, and an optional
`class` prop. Add `prefers-reduced-motion` support:

```astro
<video
  class:list={['hero-video', className]}
  src={src}
  poster={poster}
  autoplay={!prefersReducedMotion}
  muted loop playsinline
  aria-label={title}
/>
```

## What NOT to add

- **VideoObject structured data** — only useful when video is the primary page
  content, not a decorative header element.
- **Captions** — not needed for silent/music-only animation-only videos.
- **WebM variant** — H.264 MP4 with `faststart` covers all modern browsers.
- **Cloudflare Stream or similar CDN** — only necessary above ~4 MB per video.
- **Direct MP4 render** — always go through a ProRes master.

## Narrative structure for explainers

1. **Hook** — show the visible symptom or the unseen mechanism.
2. **Mechanics** — reveal the internal structure (loop, pipeline, decision tree).
3. **Contrast or failure case** — contrast sharpens the aha moment.
4. **Aha** — one consequence the viewer didn't know before.
5. **Close** — what changes now.

Scene pacing: fade in at frame 0, fade out at 12 frames before cut, crossfade 12 frames into next scene.
