# Clara Design Studio — “The Sunroom”

Production-ready bilingual reference design for the default `plonetheme.clara`
theme. Clara Design Studio is a fictional sustainable web-design studio. The
site demonstrates the same pagelet-oriented structure and component families as
the derico.de reference while supplying a distinct identity, information
architecture, imagery, and content.

## Direction

- **Creative north star:** The Sunroom — a bright working studio in which
  content, people, and technology have room to grow.
- **Palette:** solar yellow, deep evergreen ink, sky blue, leaf green, coral,
  and true neutral white. All authored in OKLCH.
- **Type:** Krona One display with Inclusive Sans for body and interface copy;
  both fonts are self-hosted under the OFL.
- **Content position:** sustainable content management through accessibility,
  efficient delivery, open standards, structured content, planned upgrades,
  and editorial independence. No decorative eco claims.
- **Navigation:** five top-level destinations, four click-open mega panels, and
  three complete levels of linked destinations. Mobile uses the same hierarchy
  as native disclosure panels.

## Build and preview

```bash
node site/build.mjs
python -m http.server 8089 --directory site
```

The active workspace demo uses port 8089:

- Sunroom: <http://localhost:8089/de/index.html?variant=sunroom>
- Greenhouse: <http://localhost:8089/de/index.html?variant=greenhouse>
- Open Sky: <http://localhost:8089/de/index.html?variant=open-sky>

Replace `/de/` with `/en/` for English. The variant query is carried through
internal navigation, so every page pattern can be reviewed in each design.

### Design variants

1. **The Sunroom** — solar yellow, deep evergreen, crisp rectangular windows,
   and poster-like Krona One typography.
2. **Greenhouse** — drenched deep green, citron and planted color, a direct
   single-family typographic voice, reversed hero composition, and rounded
   offset windows.
3. **Open Sky** — cobalt, direct sunlight yellow, coral, broad horizontal hero
   bands, and an asymmetric rounded service layout.

Both alternatives use a 16px corner ceiling for content blocks, 12px controls,
and full-pill actions. Rounded shapes remain structural; no 32px bubble cards
or nested rounded containers are introduced.

`build.mjs` is the source for shared chrome, page patterns, content, routing,
and translations. The generated German and English HTML is committed so the
reference can be reviewed without a Node server.

## Page patterns

The generated site includes:

- Homepage
- Service overview and three-level service details
- Project index, sector pages, and case-study details
- Insights index, journal, guides, workshops, and articles
- Studio overview and detail pages
- Contact form with validation and mail-client handoff
- Search demonstration including an empty state
- Legal notice, privacy, and 404 recovery

## Production contracts demonstrated

- Semantic HTML landmarks and heading order
- Native `<details>` navigation with a JavaScript enhancement that closes peer
  panels and restores focus on Escape
- Complete keyboard paths and visible focus treatment
- 44px minimum interaction targets
- Responsive structure from 320px upward and 200% zoom-safe reflow
- Local fonts and local responsive-ready image assets; no render-time third-party
  requests
- Reduced-motion alternatives
- Form default, focus, error, and success states
- Explicit image alt text and all Unsplash attribution consolidated in the
  German Impressum and English Legal Notice—not displayed beneath images
- `--plone-*` integration remains the later theme step; this mockup is the
  visual and behavioral contract for that implementation

## Image sources

Placeholder photographs were downloaded from verified `images.unsplash.com`
URLs and stored locally as AVIF and JPEG. Photographer links and usage notes are
rendered on the legal pages. They should be replaced or relicensed when this
fictional reference becomes a real site.
