# Quanta analysis summary for Clara

## Executive conclusion

Quanta's strongest contribution is **system structure**, not a palette to copy.
Clara adopts its primitive/semantic/component layering and state completeness
while preserving Plone identity, Clara's accessibility contract, and the
`--plone-*` public API.

## What the upstream research established

- Quanta was created as an experimental successor to Pastanaga for Volto.
- Its vocabulary uses physics metaphors: Planck units, particles, atoms,
  molecules and organisms.
- Its early SCSS used a 207° HSL base, a 14px mass unit, a 12px length unit,
  modular spacing, Metropolis/Anonymous Pro, and atomic component folders.
- Accessibility and framework independence were stated goals.
- The examined implementation was incomplete: foundations and several controls
  existed, while molecules, organisms, navigation and broad production
  adoption were unfinished.
- `quanta-icons` is separately useful as an SVG icon source subject to its
  license and attribution requirements.

## Corrections made during integration

1. **Primary identity**
   - Historical Clara used illustration blue `#0047c8`.
   - Quanta used a different HSL cobalt.
   - The packaged official Plone logo itself specifies `#0083BE`; Clara now
     uses that exact value for `--plone-color-primary`.

2. **Contrast**
   - Exact logo blue is 4.21:1 against white: sufficient for UI boundaries and
     large text, not normal text.
   - `#006293` is the same-hue normal-link step and clears at least 4.64:1 on
     every Clara light ground.
   - Exact-blue controls use `#001018`, reaching 4.59:1.
   - Tests calculate ratios from actual sRGB values; documentation arithmetic
     is not accepted as evidence.

3. **Namespace**
   - A copied `--quanta-*` tree would create two public APIs and ambiguous
     precedence.
   - Clara keeps `--plone-*` public and `--clara-*` private.
   - The obsolete standalone `_quanta-tokens.scss` was removed.

4. **Typography and spacing**
   - Quanta's 14px body was rejected. Clara keeps 16px content and a 15px floor.
   - Quanta's rhythm concept was adopted, but Clara keeps its fluid Utopia-style
     `--plone-space-*` scale and intrinsic layout primitives.

5. **Elevation and components**
   - Quanta's shadow scale and generic card examples conflict with Clara's flat,
     tonal system.
   - Clara uses hairlines, surfaces and existing Plone/Bootstrap hooks.
   - No parallel card component was introduced.

6. **Semantic states**
   - Success, warning, danger and info now have runtime fill, text, surface,
     border and on-fill roles.
   - `_clara-states.scss` maps buttons, alerts and validation to those roles.
   - Bootstrap compile literals are drift-guarded against the runtime tokens.

## Files changed by the integration

- `theme/scss/_clara-tokens-defaults.scss`
- `theme/scss/_clara-brand.scss`
- `theme/scss/_clara-tokens.scss`
- `theme/scss/_clara-bridge.scss`
- `theme/scss/_clara-states.scss`
- `theme/scss/_clara-components.scss`
- `theme/scss/_clara-classic.scss`
- `theme/scss/_clara-toolbar.scss`
- `tests/test_token_drift.py`
- `tests/test_color_contrast.py`
- `DESIGN.md` and architecture documentation

## Outcome

Clara aligns with Plone's design-system direction without pretending that an
experimental Volto palette is the Classic UI contract. A site integrator changes
semantic `--plone-*` roles at runtime; every supported component follows.
