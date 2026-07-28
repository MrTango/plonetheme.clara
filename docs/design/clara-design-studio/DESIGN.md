---
name: Clara Design Studio — The Sunroom
description: Sunny full-palette reference identity for the default Clara Plone theme
colors:
  sun: "oklch(0.89 0.17 96)"
  sun-soft: "oklch(0.96 0.075 98)"
  sun-deep: "oklch(0.76 0.16 88)"
  sky: "oklch(0.82 0.10 220)"
  sky-soft: "oklch(0.94 0.038 220)"
  leaf: "oklch(0.55 0.13 151)"
  leaf-soft: "oklch(0.91 0.07 151)"
  coral: "oklch(0.52 0.18 28)"
  coral-hover: "oklch(0.46 0.17 28)"
  coral-soft: "oklch(0.91 0.055 28)"
  ink: "oklch(0.22 0.045 157)"
  ink-raised: "oklch(0.30 0.045 157)"
  ink-soft: "oklch(0.40 0.035 157)"
  ground: "oklch(0.992 0 0)"
  surface: "oklch(0.965 0.012 157)"
  rule: "oklch(0.79 0.026 157)"
  on-dark: "oklch(0.98 0.008 96)"
  error: "oklch(0.46 0.19 27)"
  success: "oklch(0.40 0.11 151)"
  footer-copy: "oklch(0.88 0.018 96)"
  footer-rule: "oklch(0.46 0.04 157)"
  footer-faint: "oklch(0.82 0.02 96)"
  greenhouse-header-rule: "oklch(0.46 0.08 157)"
  greenhouse-logo-green: "oklch(0.66 0.15 157)"
  greenhouse-copy-light: "oklch(0.84 0.03 112)"
  greenhouse-panel-rule: "oklch(0.48 0.07 157)"
  greenhouse-hero-copy: "oklch(0.88 0.035 112)"
  greenhouse-band-green: "oklch(0.70 0.14 157)"
  greenhouse-band-coral: "oklch(0.72 0.15 35)"
  open-sky-sequence: "oklch(0.43 0.18 255)"
typography:
  display:
    fontFamily: "Krona One, Arial Black, sans-serif"
    fontSize: "clamp(2.55rem, 1.55rem + 4.35vw, 5.65rem)"
    fontWeight: 400
    lineHeight: 1.12
    letterSpacing: "-0.028em"
  heading:
    fontFamily: "Krona One, Arial Black, sans-serif"
    fontSize: "clamp(2rem, 1.35rem + 2.8vw, 4.25rem)"
    fontWeight: 400
    lineHeight: 1.12
    letterSpacing: "-0.025em"
  title:
    fontFamily: "Krona One, Arial Black, sans-serif"
    fontSize: "clamp(1.45rem, 1.25rem + 0.9vw, 2.15rem)"
    fontWeight: 400
    lineHeight: 1.12
  medium:
    fontFamily: "Inclusive Sans, Segoe UI, system-ui, sans-serif"
    fontSize: "1.25rem"
    fontWeight: 700
    lineHeight: 1.35
  lede:
    fontFamily: "Inclusive Sans, Segoe UI, system-ui, sans-serif"
    fontSize: "clamp(1.2rem, 1.11rem + 0.45vw, 1.5rem)"
    fontWeight: 400
    lineHeight: 1.5
  body:
    fontFamily: "Inclusive Sans, Segoe UI, system-ui, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: 1.62
  label:
    fontFamily: "Inclusive Sans, Segoe UI, system-ui, sans-serif"
    fontSize: "0.9375rem"
    fontWeight: 700
    lineHeight: 1.35
spacing:
  3xs: "0.25rem"
  2xs: "0.5rem"
  xs: "0.75rem"
  s: "clamp(1rem, 0.96rem + 0.22vw, 1.25rem)"
  m: "clamp(1.5rem, 1.4rem + 0.45vw, 1.9rem)"
  l: "clamp(2rem, 1.8rem + 0.85vw, 2.75rem)"
  xl: "clamp(3rem, 2.55rem + 1.8vw, 4.75rem)"
  2xl: "clamp(4.75rem, 3.8rem + 3.8vw, 8.5rem)"
  3xl: "clamp(6.25rem, 4.9rem + 5.2vw, 11rem)"
rounded:
  cell: "0.125rem"
  small: "0.375rem"
  logo: "0.5rem"
  alternate-control: "0.75rem"
  alternate-surface: "1rem"
  pill: "999px"
---

# Design System: Clara Design Studio — The Sunroom

## Creative north star

A bright working studio in which content, people, and technology have room to
grow. Sustainability is expressed through accessibility, efficient delivery,
open standards, structured content, editorial independence, and planned care.
It is never represented by leaf icons or unsupported environmental claims.

## Variants

### 1. The Sunroom

Solar yellow, crisp rectangular photographic windows, and Krona One. This is
the original light-default proposal.

### 2. Greenhouse

Deep evergreen owns the whole hero and service field. Citron, wet mint, grown
green, and brick coral act as planted accents. Inclusive Sans carries both
display and body roles, the hero reverses image and copy, and uneven rounded
service blocks rise from a shared baseline.

### 3. Open Sky

Cobalt owns the hero, sunlight yellow drives actions, and coral carries strong
public moments. The hero becomes a broad horizontal composition and rounded
service destinations use an asymmetric 7/5 then 4/8 rhythm rather than a
repeated card grid.

The alternatives use a strict radius ceiling: 12px controls, 16px content
surfaces, and full pills only for actions. The small 2px/8px radii belong solely
to the four-pane logo.

## Palette rules

- Solar yellow owns the homepage hero and conversion moments.
- Deep evergreen is the default ink and footer ground.
- Sky blue supports public-information and explanatory sections.
- Green describes continuity and successful states; it is not decorative eco
  shorthand.
- Coral marks primary actions, focus, and active wayfinding.
- Reading surfaces use a true neutral near-white, not cream or parchment.
- Flat fields, full-perimeter rules, and photography provide depth. There are no
  gradients, glass surfaces, or decorative shadows.

## Typography rules

Krona One gives headings the voice of optimistic public posters. Inclusive Sans
keeps navigation, forms, and long content open and readable. The pairing
contrasts a wide geometric display with a humanist body rather than combining
two similar grotesques.

- Body copy is 17px at the default browser size.
- The 15px label token is the absolute floor.
- Heading clamps stop at 68px; homepage display stops at 90.4px.
- Display tracking never exceeds the `-0.04em` floor.
- Body measure is capped at 68 characters.

## Layout and component rules

- Shared structure mirrors the derico reference: bilingual chrome, three-level
  mega navigation, breadcrumbs, page heroes, overview/detail/listing patterns,
  contact band, form states, search, footer, and 404 recovery.
- Components use intrinsic Flexbox/Grid layouts and fluid spacing tokens.
- Cards are not the default grouping. Services are connected color bands;
  projects use image-led editorial compositions; articles use ruled lists.
- Rectangular photographic windows with a full dark frame are Clara's signature
  move.
- The four lifecycle numbers are a genuine ordered sequence. Numbers are not
  used as generic labels for unrelated sections.

## Motion

One load-time homepage movement adds a subtle focus pull and settling motion
while leaving content visible at every point. Menus do not gate visibility on
animation. All transitions have a `prefers-reduced-motion` alternative.

## Imagery

Use daylight, architecture, working environments, and one direct nature detail.
Avoid staged whiteboard teams, isolated leaves as sustainability shorthand,
seedlings in hands, and generic device mockups. Images are local derivatives,
receive specific alt text, and are credited only in Impressum / Legal Notice.
