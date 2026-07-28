---
name: Clara Theme — Klarsicht (Plone Base)
register: brand
platform: web
colors:
  # One ladder anchored at the official Plone logo's exact #0083be
  # (OKLCH hue 238.72). Identity, text, and control roles are separate so the
  # exact logo colour never has to pretend it clears 4.5:1 against white.
  brand: "#0083be"          # oklch(0.57997 0.13006 238.72), exact logo blue
  brand-text: "#006293"     # accessible links; ≥4.64:1 on every light ground
  brand-hover: "#005c88"
  brand-deep: "#083148"
  on-brand: "#001018"       # 4.59:1 on exact logo blue
  ground: "#fafcfe"
  surface: "#f0f4f7"
  band: "#b7ddf8"
  band-soft: "#ddeefa"
  ink: "#0e222e"
  ink-soft: "#314553"
  rule: "#bfcdd6"
  band-rule: "#5e89a6"
  amber: "#f4af2d"
  amber-hover: "#de9d16"
  amber-text: "#7a4e05"
  error: "#a2080c"
typography:
  display:
    fontFamily: "Literata, georgia, serif"
    fontSize: "clamp(2.75rem, 1.85rem + 4vw, 5rem)"
    fontWeight: 600
    lineHeight: 1.12
    letterSpacing: "-0.02em"
  heading:
    fontFamily: "Literata, georgia, serif"
    fontSize: "clamp(2rem, 1.45rem + 2.3vw, 3.5rem)"
    fontWeight: 600
    lineHeight: 1.12
  title:
    fontFamily: "Literata, georgia, serif"
    fontSize: "clamp(1.35rem, 1.2rem + 0.7vw, 1.75rem)"
    fontWeight: 650
  body:
    fontFamily: "Source Sans 3, system-ui, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.65
  navigation:
    fontFamily: "Source Sans 3, system-ui, sans-serif"
    fontSize: "1.18125rem"
    fontWeight: 650
  label:
    fontFamily: "Source Sans 3, system-ui, sans-serif"
    fontSize: "0.9375rem"
    fontWeight: 700
rounded:
  soft: "0.625rem"
  pill: "50rem"
---

# Clara Theme — Klarsicht (Plone Base)

The packaged implementation of the clara-base "Klarsicht" reference design
(`docs/design/clara-base/`, the composition and content reference, sibling of
the derico.de „Jahresringe" system). Its original illustration-sampled palette
is archived there; this file and `theme/scss/_clara-brand.scss` are authoritative
for the shipping Plone identity. Memorable line: **"Content, secure in every sense."**

## Direction

A clear-sighted civic surface: one perceptual blue ladder anchored at the
Plone logo's exact #0083be, bookish Literata headings over a plain Source Sans
3 body, and a single amber that marks the live edge — the marketing CTA and
published state. Flat, tonal, hairlined; no shadows, no gradients.

## Rules

- **Identity and reading are separate roles.** Exact logo blue (`#0083be`)
  carries logos, large display emphasis, primary-control fills and UI geometry.
  Normal-size links use the darker same-hue `#006293` step, which clears AA on
  every Clara light ground.
- **Foregrounds are explicit.** Exact logo blue clears 3:1 as a UI boundary but
  only 4.21:1 against white. Blue controls therefore use the same-hue near-black
  `#001018` foreground (4.59:1), never assumed white.
- **Amber = published/now.** Amber marks the single marketing CTA and the
  published workflow state; standard Plone primary controls remain Plone blue.
  Wayfinding markers are blue, never amber.
- **Blend, don't box.** The hero PNG melts into the ground via
  `mix-blend-mode: multiply` on the `img`; entrance animations sit on the img
  itself (an animated ancestor isolates the stacking context and suspends the
  blend).
- **The content is 16px.** `--plone-text-base` is a flat `1rem`, never
  viewport-fluid; the 15px `--clara-text-label` tier is the floor and nothing
  renders below it.
- Depth is tonal: ground → surface → band, separated by `rule` / `band-rule`
  hairlines. No box-shadows.
- Load-time-only motion, reduced-motion safe; content is visible without
  animation.

## Customization contract

Every colour the theme paints with is a runtime custom property in
`@layer tokens` (`theme/scss/_clara-brand.scss`):

- `--plone-*` is the sole public pagelet/layout API: primitive ramps, semantic
  roles, spacing, type, motion and component foundations.
- `--clara-*` is private Klarsicht vocabulary used to compose those public
  roles and named Clara-only hooks such as `--clara-footer-ground`.
- Quanta informs the systematic role model but does not create a competing
  `--quanta-*` runtime namespace.

A theme built on Clara overrides either level with a later `:root {}` block —
no Sass, no template forks. The Sass-side `$clara-*` literals
(theme/scss/_clara-tokens.scss) only seed Bootstrap's compile-time color math
and are drift-guarded against the runtime defaults by
tests/test_token_drift.py.
