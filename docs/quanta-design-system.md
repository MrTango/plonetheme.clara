# Quanta concepts and Clara adoption decisions

## Scope

This document records the design-system concepts found in the experimental
Quanta repositories and the production decisions made for `plonetheme.clara`.
It is not a verbatim upstream specification. The normative Clara contract is
[`clara-theming-architecture.md`](clara-theming-architecture.md).

## Upstream projects examined

| Repository | Role | Integration relevance |
|---|---|---|
| [plone/quanta-icons](https://github.com/plone/quanta-icons) | SVG icon set | Potential shared icon source |
| [plone/volto-quanta](https://github.com/plone/volto-quanta) | Experimental Volto add-on | Primary source for foundations |
| [plone/volto-quanta-project](https://github.com/plone/volto-quanta-project) | Demo project | Integration/Storybook reference |

Quanta was experimental in the material captured here. Its implementation
status and roadmap must be verified upstream before making current claims.

## Philosophy

Quanta's useful principles are:

1. Accessibility belongs in the foundation.
2. Design decisions should be tokens, not repeated literals.
3. Components should consume semantic roles rather than raw palette steps.
4. Small, composable responsibilities are easier to maintain than monoliths.
5. Runtime theming should not require rebuilding the application.

Clara shares those goals but expresses them through the existing Plone/pagelet
contract.

## Architecture comparison

| Concern | Historical Quanta | Clara decision |
|---|---|---|
| Public namespace | Quanta-specific variables | `--plone-*` only |
| Component structure | Atomic-design folders | Plone hooks + focused SCSS partials |
| Runtime values | CSS custom properties | CSS custom properties |
| Framework | Intended framework-agnostic; built in Volto | Bootstrap 5.3 bridge + Plone markup |
| Base type | 14px | 16px body, 15px floor |
| Spacing | Fixed 12px Planck length | Fluid `--plone-space-*` rhythm |
| Colour model | Historical HSL generation | Measured sRGB values documented in OKLCH |
| Elevation | Named shadow levels | Tonal surfaces and hairlines; no shadows |
| Dark mode | Palette inversion proposal | Semantic-role remapping |

## Token hierarchy

Clara uses three levels.

### Primitive

Raw ramps and scales:

```css
--plone-blue-500: #0083be;
--plone-blue-700: #006293;
--plone-gray-900: #0e222e;
--plone-space-s: clamp(1rem, 0.96rem + 0.22vw, 1.25rem);
--plone-duration-standard: 225ms;
```

### Semantic

Roles that communicate intent:

```css
--plone-color-primary: var(--plone-blue-500);
--plone-color-on-primary: var(--plone-gray-950);
--plone-color-link: var(--plone-blue-700);
--plone-color-success-surface: #e7f5ec;
--plone-color-success-text: #205d40;
```

### Component

Bootstrap and Clara components consume semantic roles:

```css
.btn-primary {
  --bs-btn-bg: var(--plone-color-primary);
  --bs-btn-color: var(--plone-color-on-primary);
}

.alert-success {
  --bs-alert-bg: var(--plone-color-success-surface);
  --bs-alert-color: var(--plone-color-success-text);
}
```

A component never chooses a raw colour because it happens to look close.

## Colour system

### Official anchor

The SVG packaged at
`docs/design/clara-base/site/assets/images/plone-logo.svg` specifies
`fill="#0083BE"`. That exact value is the primary identity token.

### Functional split

| Role | Value | Measured purpose |
|---|---|---|
| Primary | `#0083be` | Logo, UI geometry, large emphasis; ≥3:1 on light grounds |
| Link | `#006293` | Normal text; ≥4.64:1 on all Clara light grounds |
| Link hover | `#005c88` | Stronger interactive state |
| On-primary | `#001018` | 4.59:1 on exact primary |
| Dark surface | `#083148` | Toolbar and skip-link ground |

Exact logo blue is not used as normal-size text merely because it is called
“primary.” Naming does not override contrast.

### Semantic families

Success, warning, danger and info each define:

- base fill;
- readable text;
- tinted surface;
- visible boundary;
- foreground for the base fill.

This avoids alpha-derived backgrounds and prevents every component from making
its own contrast decision.

### Dark mode

Dark mode remaps semantic roles only. Primitive identity values stay stable.
Higher surfaces are lighter, body text remains readable, and no shadows are
introduced to simulate elevation.

## Typography

Clara keeps its established pairing:

- Literata for display and headings;
- Source Sans 3 for body and interface text.

The content body is always `1rem`; labels never fall below `0.9375rem`.
Headings are fluid and bounded. This preserves readable Plone content and avoids
Quanta's historical 14px application default.

## Spacing and layout

Quanta's rhythm principle is adopted, not its literal fixed scale. Clara uses a
fluid scale from `--plone-space-3xs` through `--plone-space-3xl`, mapped into
Bootstrap's `$spacers` compatibility surface and consumed by intrinsic
`.plone-stack`, `.plone-cluster`, `.plone-grid`, `.plone-switcher` and
`.plone-sidebar` primitives.

## Motion

Runtime motion roles are deliberately small:

- instant: 100ms;
- fast: 150ms;
- standard: 225ms;
- slow: 300ms;
- exponential ease-out curves.

Reduced-motion users receive static state feedback. Content never depends on an
entrance animation to become visible.

## Component model

Clara does not mint a second component library. It reuses:

- Plone hooks such as `.entries`, `.item`, `.summary` and `.documentByline`;
- Bootstrap hooks such as `.btn`, `.alert`, `.card`, `.table`, `.form-control`;
- `plone-` classes only for layout concepts Plone does not already name.

The result is compatible with existing add-ons and remains runtime-themable.

## Accessibility validation

- `tests/test_color_contrast.py` resolves actual light/dark token values and
  checks WCAG ratios.
- `tests/test_token_drift.py` keeps Bootstrap Sass literals synchronized with
  runtime defaults.
- component bridge tests verify that Bootstrap's component-scoped literals do
  not shadow Clara's runtime roles.
- focus, disabled, busy, valid and invalid states are styled explicitly.

## Adopt / adapt / reject summary

### Adopt

- token layers;
- semantic completeness;
- rhythmic scales;
- atomic responsibilities;
- accessibility-first testing.

### Adapt

- spacing to Clara's fluid system;
- components to Plone/Bootstrap hooks;
- dark mode to semantic role flips;
- motion to Clara's restrained brand voice.

### Reject

- public `--quanta-*` duplication;
- historical HSL cobalt as Plone identity;
- unverified contrast claims;
- 14px content;
- generic shadows and card proliferation;
- wholesale palette copying.
