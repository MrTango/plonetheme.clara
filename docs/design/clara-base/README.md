# clara-base — the base Clara theme, "Klarsicht"

Reference mockup for the base `plonetheme.clara` composition, created
2026-07-18. Its illustration-sampled `#0047c8` palette is retained as a
historical exploration; the shipping theme now follows `plonetheme.clara/DESIGN.md`
and the official Plone logo blue `#0083be`.

It is the sibling of the derico.de „Jahresringe" site: the same structural
system (bands, hairlines, field-guide lists, click-open disclosure nav,
load-time-only motion) re-skinned with Clara's own palette, imagery and
content. It deliberately ignores the current packaged theme and the earlier
"Sunroom" exploration.

## Brief (confirmed 2026-07-18)

- **Register:** brand · EN only · 7 pages + 404, hand-authorable static HTML.
- **Nav:** Home · Why Plone · Secure Content · Community (disclosure panel →
  Forum, Sprints, Conferences). Utility link: plone.org.
- **Home hero figure:** `plone_en.png` from the derico asset set — the
  illustration is the imagery and the palette anchor.
- **Signature motif:** a content-tree SVG with workflow-state nodes (private /
  pending review / published), Clara's counterpart to derico's growth rings.
- Memorable line: **"Content, clearly governed."**

## Re-shape brief: "Secure content" as the site thesis (confirmed 2026-07-18, implemented same day)

Widen "secure content" from data/workflow security into the site's central,
three-pillar claim — **Protected · Durable · Open** — and rework the site
around it:

- **Protected** — permissions, workflow states as security boundaries, the
  public security record (today's page, tightened).
- **Durable** — structured, typed content plus the migration record: every
  major release since 2001 has shipped an upgrade path; content stays
  meaningful, usable and accessible over time. Honest phrasing, no invented
  statistics.
- **Open** — `plone.restapi`: complete HTTP/JSON access to all content, any
  front end, export any time.
- Pivot sentence, landed in a closing band: *all of this together is secure
  content.*

Decisions:

- **Memorable line changes site-wide** to **"Content, secure in every
  sense."** (home h1 + footer). "Content, clearly governed." retires into the
  Protected chapter.
- `secure-content.html`: definitional hero → pillar band with `#protected` /
  `#durable` / `#open` anchors → three chapters (prose + figure + fact-aside,
  alternating grounds) → closing band with proof links → CTA band.
- `index.html`: hero headline switches to the thesis (illustration stays);
  manifesto band rebalances to one item per pillar + "content at scale";
  Secure Content teaser rewritten. `why-plone.html`: durability and REST API
  rise to equal weight, cross-linking the pillar chapters. Other pages:
  footer line only.
- **One figure per pillar**, same SVG grammar (flat fills in ink outlines,
  1–2px strokes, labels in HTML): existing layers figure (Protected); a
  **version-path** — one document glyph along a horizontal line of release
  stations, amber = current, dashed = next, deliberately linear so it doesn't
  clone derico's rings (Durable); a **flows-out** diagram — content tree
  behind one API port, arrows to several consumers (Open).
- Proof links real and stable only: `plone.org/security`, `6.docs.plone.org`
  upgrading docs, `github.com/plone/plone.restapi`.
- Production-ready; edits land in `site/build.mjs`, HTML regenerated. New
  copy states positive claims directly. Load-time-only motion; reduced-motion
  renders figures in final state.

## Palette — the Clara ladder

One blue hue (OKLCH hue 261.9, sampled from the illustration's `#0047c8`),
lightness moves; one amber accent. All ratios below were measured against the
rendered values, not derived.

| token | value | role |
|---|---|---|
| `--brand` | `oklch(0.4553 0.2091 261.9)` `#0047c8` | exact illustration blue: links, nav marks, SVG strokes (7.5:1 on ground) |
| `--brand-deep` | `oklch(0.32 0.10 261.9)` | dark accents, skip-link ground |
| `--ground` | `oklch(0.99 0.0025 261.9)` | page |
| `--surface` | `oklch(0.965 0.008 261.9)` | soft sections |
| `--band` / `--band-soft` | `oklch(0.915 0.04 261.9)` / `oklch(0.955 0.02 261.9)` | manifesto + CTA bands / mega panel |
| `--ink` / `--ink-soft` | `oklch(0.24 0.045 261.9)` / `oklch(0.40 0.045 261.9)` | text (≥12.8:1 / ≥7.1:1 on every ground) |
| `--amber` / `--amber-hover` | `oklch(0.80 0.155 78)` / `oklch(0.74 0.15 78)` | the one CTA fill, published-state fill |
| `--amber-text` | `oklch(0.50 0.105 72)` | amber as text/numerals (≥4.5:1 everywhere) |

**Named rules**

- **The ladder inverts derico's.** Clara's brand colour is dark enough to be
  text; it carries links and strokes at full strength. No separate link step.
- **The outline carries the contrast.** Flat amber (and pale blue) fills never
  meet the ground directly: they sit inside a ≥3:1 ink outline, exactly like
  the flat fills in `plone_en.png`. This is why `.button` has a 1.5px ink
  border — it is a compliance mechanism *and* the illustration's language.
- **Amber = published/now.** The accent marks the CTA, the published state and
  legend numerals; blue is structure, amber is the live edge.
- **Blend, don't box.** The hero PNG melts into the ground via
  `mix-blend-mode: multiply` on the `img`. Entrance animations must sit on the
  img itself — an animated *ancestor* isolates the stacking context, suspends
  the blend and flashes the PNG's white ground.

## Type & patterns

Literata (display, italic = voice) + Source Sans 3 (body), self-hosted, same
tiers as derico (`--text-label` 15px floor, 16px flat body, fluid headings).
Patterns reused from the Jahresringe system: `.section--band/--soft`,
`.section-index`, `.detail-grid` + sticky aside, `.proof-band`, `.event-list`,
`.mega-panel` (one Community panel), `.error-page`. New: `.hero-figure`,
`.structure-figure` + `.state-legend`, `.layers-figure` (Secure Content),
page-hero "sheet" decorations (offset rounded rects, wide viewports only).
Labels live in HTML, never in SVG text.

## Build & preview

```bash
node site/build.mjs        # regenerates the committed HTML from one template
# Serve from the workspace root on 8088 — the container firewall only accepts
# inbound 8080–8090, so 8088 is reachable from the host browser:
python3 -m http.server 8088 --bind 0.0.0.0 --directory /workspaces/pagelet-playground
# → http://localhost:8088/plonetheme.clara/docs/design/clara-base/site/
```

## Deviations & follow-ups

- Photography (added 2026-07-18, superseding the earlier no-photo deviation):
  the Community, Sprints and Conferences pages each carry one Unsplash photo
  (`photo-community` by Annie Spratt, `photo-sprint` by Marvin Meyer,
  `photo-conference` by Headway), self-hosted in `assets/images/` as jpg +
  webp (1600/800) with the `.photo-frame` brand-blue wash and an italic
  credit caption. Home and Secure Content stay illustration/diagram-led on
  purpose. `images.unsplash.com` is in the container's firewall allowlist,
  but the ipset snapshot may need re-resolving after a restart (see
  `firewall-init.sh`'s snapshot limitation) before re-downloading.
- External links (plone.org, community.plone.org, docs.plone.org) are real;
  event copy avoids fabricated dates.
- `plone_en.png/webp` is copied from `plonetheme.clara/src/plonetheme/clara/static/`
  (same file the derico site uses).
