# derico.de — design exploration: „Jahresringe"

Design exploration for a relaunch of [derico.de](https://derico.de), created
2026-07-16. The original single-page direction remains in
`variant-2-jahresringe-hell.html`. The `site/` directory develops it into a
responsive, bilingual multi-page reference implementation with shared assets,
reusable page patterns, a click-open mega menu, form states, and a 404 page.
It is the visual/content contract for the later Clara/pagelet integration.

Three variants were explored (1 „Werkbank", 2 „Jahresringe", 3 „Quelloffen").
**Variant 2 was chosen on 2026-07-16 and the other two were deleted** — they were
never committed, so they exist nowhere else. Two things worth remembering from
them: variant 2's palette is the petrol/copper set adopted from „Werkbank" (a
deepened evolution of Clara's brand teal `#1e6f8e`), and the „Quelloffen"
direction was the developer/community-facing one, should that audience ever need
its own surface.

## Brief

- **Register:** brand — the site's job is to communicate, the design IS the product.
- **Positioning:** *Nachhaltige Lösungen* — applications built for the decade
  after launch. Sustainability meaning maintainability, open standards, and a
  20+ year track record — never greenwashing.
- **The four values:** flexible · modern · secure · sustainable.
- **Content pillars:** Python (Plone, Odoo, FastAPI, Django, Pyramid),
  JavaScript (Svelte, SvelteKit, React), agile delivery, training & talks,
  open-source community work (plonecli, bobtemplates.plone, sprints).
- **Audiences:** business decision-makers (primary), developers/community (secondary).
- **CTA:** a first conversation, `md@derico.de`. Secondary: workshop request / talks.
- Bilingual DE/EN is part of the identity; the mockup shows an EN/DE switch in the nav.

## The variant

| | 2 „Jahresringe" |
|---|---|
| Audience lean | sustainability-minded founders |
| Scene | founder reading at night, allergic to hype |
| Color strategy | exact cyan in logo and rings; pale cyan manifesto/contact bands; direct orange accent |
| Type | Literata + Source Sans 3, Roboto Slab display (forestry manual / bookbinding) |
| Signature move | growth-rings SVG: tree rings = 20+ years of release history |
| Voice | quiet, durable, grown |

Notes:

- The growth rings are deliberately **generic** (Jahr 1 / Jahr 10 / heute): they
  tell the story of one solution growing with the client's needs, not derico's
  own tech timeline (decided in live steer a392e049).
- Contact details, phone fragments, and all `#` links are placeholders from the
  current site; verify before shipping.

## Type floor (2026-07-16)

**No text renders below 15px.** Hierarchy comes from weight, color, casing, and
spacing; the label tier (`--label`, nav, language switch, footer, caption,
small-caps tags) sits exactly on the floor at 15px, prose stays at 16px+.

The rings legend is **HTML beneath the disc, not `<text>` inside the SVG**. SVG
text scales with the graphic — the figure's scale factor runs 0.42–0.80 across
viewports, so any fixed value swings ~1.9× (16px on mobile forces 31px on
tablet). Only geometry belongs in that SVG. See DESIGN.md, "The 15px Floor".

## Multi-page reference implementation

Build the German and English pages after changing content or shared markup:

```bash
node site/build.mjs
```

Serve `site/` from any static server and open `de/index.html`. The implementation
contains five reusable patterns: home, section overview, capability detail,
training/talk listing, and contact. Its desktop navigation borrows DLR's
click-open grouped-panel behavior; the visual language remains Jahresringe.
Mobile uses a menu button and nested accordions, with the same information
architecture and no hover-only actions.

Fonts are self-hosted variable WOFF2 files in `site/assets/fonts/`: Literata and
Source Sans 3 under the OFL, plus Roboto Slab under Apache 2.0 for the homepage
service atlas. There are no third-party requests at render time.

The homepage hero photograph shows an established, managed conifer stand by
[Kat Closon on Unsplash](https://unsplash.com/photos/brown-and-green-trees-on-brown-grass-field-during-daytime-hZX4tYgljUI).
Locally generated wide and portrait crops ship as AVIF, WebP, and JPEG in
`site/assets/images/`; source and license details live beside them.

## Implementation notes (Clara / plone.pageletlayout)

The mockup's `:root` opens with a `--plone-*` block — the same public token API
Clara implements (`docs/clara-theming-architecture.md` §1.5). Adoption is
therefore mostly a `:root` override in the `tokens` layer:

- **Tokens only:** colors (`--plone-color-*`), body font, measure, radii.
- **Beyond tokens** (needs templates/components in the theme): the hero layout,
  the growth-rings SVG, the rings legend, the field-guide definition list.
- Fonts load from Google Fonts **in the mockup only**. Production must
  self-host (GDPR — German audience) with `font-display: swap` fallbacks.
- All motion is load-time only, ends visible, and is wrapped in
  `@media (prefers-reduced-motion: no-preference)`. Keep that contract.

## Verification done

Rendered headless (Chrome-for-Testing over CDP) at 1440 / 900 / 375 / 320px:
no text below the 15px floor, no SVG text overflow, no horizontal overflow;
body-text contrast checked against WCAG AA (≥ 4.5:1) across the hero, cyan
bands, orange accents, and controls.
