# Quanta-informed Clara implementation guide

This guide describes the implementation that actually ships. Quanta contributes
system ideas; `--plone-*` remains Clara's only public runtime API.

## Build shape

`theme/scss/clara.scss` compiles one layered bundle:

```text
reset → tokens → bootstrap → primitives → components → compat → addons → site
```

Relevant partials:

| File | Responsibility |
|---|---|
| `_clara-tokens-defaults.scss` | Public primitive and semantic defaults |
| `_clara-brand.scss` | Klarsicht identity composed onto the contract |
| `_clara-tokens.scss` | Sass literals required by Bootstrap colour math |
| `clara-bootstrap.scss` | Bootstrap compile and spacer remap |
| `_clara-bridge.scss` | Runtime `--bs-*` → `--plone-*` bridge |
| `_clara-states.scss` | Buttons, alerts, forms and status states |
| `_clara-primitives.scss` | Intrinsic layout primitives |
| `_clara-components.scss` | Clara/pagelet component styling |
| `_clara-content.scss` | Listings, cards, albums and tables |
| `_clara-toolbar.scss` | Editor chrome |

There is no `_quanta-tokens.scss`. Do not recreate one.

## Primary colour

The official packaged Plone logo uses `#0083BE`.

```css
:root {
  --plone-blue-500: #0083be;
  --plone-blue-700: #006293;
  --plone-gray-950: #001018;

  --plone-color-primary: var(--plone-blue-500);
  --plone-color-link: var(--plone-blue-700);
  --plone-color-on-primary: var(--plone-gray-950);
}
```

Why three roles:

- exact logo blue against white is 4.21:1;
- that clears the 3:1 UI/large-text threshold, not normal-text AA;
- the darker link step clears at least 4.64:1 on every Clara light ground;
- the near-black foreground clears 4.59:1 on exact logo blue.

Never “fix” this by putting white normal text on exact logo blue.

## Semantic states

Every state must remain complete:

```css
--plone-color-success;
--plone-color-success-text;
--plone-color-success-surface;
--plone-color-success-border;
--plone-color-on-success;
```

The same five-role pattern exists for `warning`, `danger` and `info`.
`_clara-states.scss` binds these to:

- `.btn-primary|success|warning|danger|info`;
- `.alert-primary|success|warning|danger|info`;
- valid/invalid form controls and feedback;
- explicit busy feedback through `[aria-busy="true"]`.

State markup still needs words or icons. Colour alone is not status content.

## Typography

Keep:

```css
--plone-font-body: "Source Sans 3", system-ui, sans-serif;
--clara-font-display: "Literata", georgia, serif;
--plone-text-base: 1rem;
--clara-text-label: 0.9375rem;
```

Only headings and intentional lede/display roles are fluid. Do not copy Quanta's
historical 14px body scale into content or editor interfaces.

## Spacing and motion

Components consume the public scales:

```css
.component {
  gap: var(--plone-space-s);
  padding: var(--plone-space-m);
  transition: color var(--plone-duration-standard)
    var(--plone-ease-out-quint);
}
```

Do not introduce a second fixed rhythm or raw durations. The fluid Plone space
scale is also mapped into Bootstrap's `$spacers` output for third-party
compatibility.

## Bootstrap bridge

Bootstrap declares some variables globally and others directly on component
roots. Rebind at the scope Bootstrap uses:

```css
:root {
  --bs-body-color: var(--plone-color-text);
  --bs-link-color: var(--plone-color-link);
}

.card {
  --bs-card-spacer-x: var(--plone-space-m);
}
```

A component-scoped Bootstrap literal shadows a `:root` custom property even
when the name matches. `tests/test_component_bridge.py` guards this failure.

## Runtime customization

A downstream theme registers a later bundle whose content is a `:root` block:

```css
:root {
  --plone-color-primary: #8a2054;
  --plone-color-primary-hover: #b84a7c;
  --plone-color-on-primary: #ffffff;
  --plone-color-link: #7a1748;
  --plone-color-link-hover: #5d0f35;
}
```

When changing a semantic family, override the complete family. A control panel
should validate contrast before saving values.

Do not override `--clara-*` unless the site intentionally depends on Clara's
private visual vocabulary. Public integrations use `--plone-*`.

## Adding a component

1. Reuse an existing Plone or Bootstrap hook.
2. Identify semantic roles before writing selectors.
3. Use component-level `--bs-*` rebinding when Bootstrap pins a literal there.
4. Use the fluid spacing scale and 44px minimum interactive target.
5. Cover default, hover, focus-visible, active, disabled, busy, error and
   success where applicable.
6. Add reduced-motion behavior.
7. Add a structural test and, when computed style matters, a fixture.
8. Measure actual foreground/background pairs.

Do not:

- create `.plone-card` when `.card` already exists;
- expose `--quanta-*`;
- use shadows for decorative depth;
- derive status surfaces with arbitrary alpha;
- put normal-size logo blue text on white;
- add utility classes to Clara's own markup.

## Validation

Run:

```bash
pnpm run build
uv run pytest -q
node /.agents/skills/impeccable/scripts/detect.mjs --json theme/scss tests/fixtures
```

Important guards:

- `test_color_contrast.py` — light/dark role ratios;
- `test_token_drift.py` — Sass/runtime equality and namespace hygiene;
- `test_component_bridge.py` — component-scope rebinding;
- `test_content_components.py` — intrinsic content layouts;
- `test_toolbar.py` — theme-owned editor chrome.

Then inspect the runtime fixtures at narrow, medium and wide viewports, with
keyboard focus and dark mode.

## Migration from the retired Quanta token file

If local code used `--quanta-*`, migrate by role rather than by colour name:

| Retired concept | Current Clara role |
|---|---|
| cobalt used as brand | `--plone-color-primary` |
| sapphire used as link | `--plone-color-link` |
| denim used as text | `--plone-color-text` |
| air used as background | `--plone-color-bg` |
| snow used as surface | `--plone-color-surface` |
| rhythm-medium | choose the semantic `--plone-space-*` step |
| Quanta size-m | `--plone-text-base` for content |
| Quanta elevation | surface + `--plone-color-border` |

Do not preserve aliases indefinitely: they would recreate the competing public
API this integration removes.
