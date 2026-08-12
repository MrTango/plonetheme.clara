# Clara — theming architecture

Clara is the first — and, for now, the only — theme built on
`plone.pageletlayout`. This document is the design contract for two things at
once: the **`--plone-*` layout contract** that ships in `plone.pageletlayout`
(the primitives, the markup hooks, the token *vocabulary*), and **Clara's CSS
layer** (the token *values* and the Bootstrap compile that turn that vocabulary
into a look). Its promise: a site integrator restyles a whole Plone Blicca site
by editing tokens, never templates.

## Package split (read this first)

Two packages, one design language. The split is a **re-role**: the layout
package is an integration package headed upstream, and Clara is the one real
theme that owns every stylesheet.

| Package | Owns | Ships |
|---|---|---|
| `plone.pageletlayout` | The **rendering machinery** and the **markup contract** | Pagelet/layout directives, the single whole-body viewlet manager, the content views, all base templates, and the **class + custom-property vocabulary** those templates author (`.plone-*` primitive classes, `.element-*` hooks, `--plone-*` token references with fallbacks). **No CSS bundle, no Bootstrap.** Staged to prove the layout machinery, then merged upstream into `plone.app.layout`. |
| `plonetheme.clara` | The **one real theme** | The `--plone-*` token **values**, the Bootstrap 5.3 **Sass compile** driven from those values, the `@layer` declaration, the layout-primitive CSS, the `--bs-*`→`--plone-*` bridge, the `$spacers` remap, dark-mode token flips, Clara's own non-contract extensions (`.clara-megamenu`, brand assets) — **all of it as one compiled bundle**, `clara.min.css`. |

`--plone-*` is the name of the **design language**, not of the theme — exactly
as `--bs-*` is Bootstrap's language, not the name of a file. It is namespaced
`--plone-`, not `--clara-`, on purpose: the primitives and templates that read
these tokens are destined for `plone.app.layout` upstream, and **a theme's name
cannot appear in core Plone markup**. `plone.pageletlayout` declares the
vocabulary and consumes it through fallbacks; **Clara supplies the values** —
it is a *values + assets* layer that sets `--plone-*`. A second theme
(`plonetheme.foo`) sets a different set of values against the identical
contract and reuses every primitive, every template, every bridge line
unchanged.

Because the layout package ships **no CSS**, a site running `plone.pageletlayout`
with *no* theme renders **unstyled** — that is expected and correct for an
integration package (like a Volto site with no add-on styling). Styling is a
theme's job; there is no "legible without a theme" fallback bundle, and there is
no standalone `bootstrap5` bundle — Bootstrap is `@import`ed *inside* Clara's
single compile.

**Design principles (non-negotiable, enforced in review):**

1. Customization happens in CSS, not template overrides. A common adjustment
   that forces a template override is a bug in the markup contract — fix the
   contract, do not ship the override.
2. CSS custom properties are the public API. Sass is a build-time
   implementation detail; an integrator never opens a `.scss` file.
3. No spacing utility classes in the contract markup or in Clara's own markup or
   docs — not `m-2`, not `p-3`, not `g-4`. Between-sibling spacing belongs to
   the parent primitive; inside-component spacing belongs to that component's
   `--bs-*` properties.
4. Semantic, minimal markup. Every wrapper element is a permanent contract.
   Justify each one or delete it.
5. **Reuse over invent.** Where Plone already names a thing, reuse its class
   verbatim (`.entries`, `.item`, `.summary`, `.card`, `.table`). A `plone-`
   prefix is only for primitives Plone has no name for.

---

## 1. Token layer — the `--plone-*` namespace

All contract tokens live under `--plone-`. Four families, one flat namespace, no
nesting games. Tokens are **primitive** (raw scale steps) or **semantic** (role
names that reference primitives). Components and the Bootstrap bridge read
*semantic* tokens only; the raw scale is an implementation detail of the token
file. The token file ships in **Clara** (the values layer); its *names* are the
`plone.pageletlayout` contract.

### 1.1 Fluid space scale (Utopia-style `clamp()`)

One geometric-ish scale, viewport-fluid between a 320 px min and a 1240 px max
viewport. Steps are named by t-shirt size, not by number, so markup reading
`--plone-space-m` never has to change when the scale is retuned.

```css
:root {
  /* Fluid space scale — min@320px … max@1240px, single source of truth.
     Generated shape is Utopia's: clamp(min, <slope>vw + <intercept>rem, max). */
  --plone-space-3xs: clamp(0.25rem, 0.24rem + 0.05vw, 0.31rem);
  --plone-space-2xs: clamp(0.50rem, 0.48rem + 0.11vw, 0.63rem);
  --plone-space-xs:  clamp(0.75rem, 0.72rem + 0.16vw, 0.94rem);
  --plone-space-s:   clamp(1.00rem, 0.96rem + 0.22vw, 1.25rem);
  --plone-space-m:   clamp(1.50rem, 1.43rem + 0.33vw, 1.88rem);
  --plone-space-l:   clamp(2.00rem, 1.91rem + 0.43vw, 2.50rem);
  --plone-space-xl:  clamp(3.00rem, 2.87rem + 0.65vw, 3.75rem);
  --plone-space-2xl: clamp(4.00rem, 3.83rem + 0.87vw, 5.00rem);
  --plone-space-3xl: clamp(6.00rem, 5.74rem + 1.30vw, 7.50rem);
}
```

### 1.2 Type scale

Fluid too, on a modular scale (~1.2 mobile → ~1.25 desktop). `--plone-text-*`
sets `font-size`; matching line-heights are unitless.

```css
:root {
  --plone-text-xs:   clamp(0.79rem, 0.77rem + 0.08vw, 0.83rem);
  --plone-text-s:    clamp(0.89rem, 0.86rem + 0.14vw, 0.96rem);
  --plone-text-base: clamp(1.00rem, 0.96rem + 0.22vw, 1.13rem);
  --plone-text-m:    clamp(1.13rem, 1.06rem + 0.33vw, 1.35rem);
  --plone-text-l:    clamp(1.27rem, 1.17rem + 0.49vw, 1.62rem);
  --plone-text-xl:   clamp(1.42rem, 1.28rem + 0.71vw, 1.94rem);
  --plone-text-2xl:  clamp(1.60rem, 1.39rem + 1.01vw, 2.33rem);
  --plone-text-3xl:  clamp(1.80rem, 1.51rem + 1.42vw, 2.80rem);

  --plone-leading-tight: 1.15;
  --plone-leading-body:  1.55;
}
```

### 1.3 Color

Semantic roles reference a small primitive ramp. Roles are what the bridge and
components consume; the ramp is retunable without touching either. Both are
`--plone-*` — the whole token file is the contract's default values.

```css
:root {
  /* primitive ramp (excerpt) — exact Plone identity plus functional steps */
  --plone-blue-100: #ddeefa;
  --plone-blue-500: #0083be; /* exact official Plone logo blue */
  --plone-blue-700: #006293; /* accessible normal-size text */
  --plone-gray-050: #f7f8fa;
  --plone-gray-200: #d7e0e5;
  --plone-gray-700: #314553;
  --plone-gray-900: #0e222e;
  --plone-gray-950: #001018;

  /* semantic roles — the actual public surface */
  --plone-color-primary: var(--plone-blue-500);
  --plone-color-on-primary: var(--plone-gray-950);
  --plone-color-text: var(--plone-gray-900);
  --plone-color-muted: var(--plone-gray-700);
  --plone-color-bg: #ffffff;
  --plone-color-surface: var(--plone-gray-050);
  --plone-color-border: var(--plone-gray-200);
  --plone-color-link: var(--plone-blue-700);
  --plone-color-focus-ring: var(--plone-gray-950);

  /* every state is runtime-tunable as fill/text/surface/border/on-fill */
  --plone-color-success: #2e7d52;
  --plone-color-success-text: #205d40;
  --plone-color-success-surface: #e7f5ec;
  --plone-color-success-border: #3b8f67;
  --plone-color-on-success: #ffffff;
}
```

The exact logo blue is an identity/UI colour: it clears 3:1 against Clara's
light grounds but only 4.21:1 against white. Normal-size links therefore use
the darker same-hue step; controls filled with exact logo blue use the explicit
near-black `--plone-color-on-primary` (4.59:1). Contrast tests enforce these
roles instead of relying on palette arithmetic.

### 1.4 Measure, radii, borders

```css
:root {
  --plone-measure:       65ch;   /* readable content column width */
  --plone-measure-wide:  85ch;

  --plone-radius-0: 0;
  --plone-radius-s: 0.25rem;
  --plone-radius-m: 0.5rem;
  --plone-radius-l: 1rem;
  --plone-radius-pill: 50rem;

  --plone-border-width: 1px;
  --plone-border: var(--plone-border-width) solid var(--plone-color-border);
}
```

### 1.5 How a site overrides tokens

**One file, one place.** Clara ships its whole theme as the single
`plonetheme-clara` bundle (`clara.min.css`), whose `tokens` layer sets the
`--plone-*` defaults and whose `site`-adjacent tail is the last word. A site
integrator overriding tokens does exactly one thing: register a **later** bundle
whose entire content is a single `:root` block.

```xml
<!-- site.package/profiles/default/registry.xml -->
<records interface="plone.base.interfaces.IBundleRegistry"
         prefix="plone.bundles/acme-tokens">
  <value key="csscompilation">++resource++acme.theme/acme-tokens.css</value>
  <value key="depends">plonetheme-clara</value>
  <value key="enabled">True</value>
</records>
```

```css
/* acme.theme/acme-tokens.css — the ENTIRE site customization */
:root {
  --plone-color-primary: #b6002c;
  --plone-space-m: clamp(1.25rem, 1.2rem + 0.3vw, 1.6rem);
  --plone-radius-m: 0;
}
```

Because everything downstream (primitives, the `--bs-*` bridge, components)
reads these roles, the whole theme responds. No Sass rebuild, no template touch.
Clara's own brand values are set the same way — `clara-brand.css` is a Clara
*asset* that sets `--plone-*` values; the namespace it writes is the contract's,
not the theme's.

### 1.6 Per-site / per-content-type tokens (control panel & Chameleon)

Custom properties inherit and cascade, so **scope = selector**. Two runtime
override paths, neither of which recompiles anything:

- **Control panel** writes a `<style>:root{…}</style>` blob (or a
  registry-record string) that the head emits — a Blicca control panel that
  exposes "primary color" / "base spacing" sliders is just a form that writes
  four `--plone-*` declarations. (Building that control panel is a separate
  feature; the *CSS mechanism* it would drive is what this section specifies.)
- **Chameleon-computed inline style** sets tokens per content item or per type
  by binding them on the element. The base layout's `<body>`/wrapper already
  carries the portal-type body class; a template (or a behavior-driven view)
  can additionally emit an inline `style` scoping tokens to a subtree:

```html
<!-- per-content-type accent, computed server-side, zero new CSS -->
<body tal:attributes="style python:view.plone_token_style()">
  <!-- e.g. style="--plone-color-primary:#0a7; --plone-space-m:2rem" on News items -->
```

Everything inside `<body>` inherits the narrowed tokens; the rest of the site
keeps the site defaults. This is the sanctioned mechanism for
"News items are green, Events are amber" — a token scope, never a stylesheet
fork.

---

## 2. Cascade layers

**Clara** declares the layer order **once**, as the first rule of its single
compiled bundle, before any other rule is written:

```css
@layer reset, tokens, bootstrap, primitives, components, compat, addons, site;
```

Later layers win over earlier ones **regardless of selector specificity**. That
single line is the whole conflict-resolution strategy — it is why Clara needs no
`!important` and no specificity escalation anywhere. There is no cross-bundle
`depends` chain to reason about: the entire order lives inside one file.

| Layer | Owner | Holds |
|---|---|---|
| `reset` | Clara | the minimal CSS reset shipped ahead of Bootstrap's reboot |
| `tokens` | Clara | the `:root` `--plone-*` value blocks (§1) + dark-mode flips (§6.4) |
| `bootstrap` | Clara | the compiled Bootstrap 5.3 output (§6) |
| `primitives` | Clara (class names = contract) | the layout-primitive CSS (§3), whose `.plone-*` class names are `plone.pageletlayout`'s markup contract |
| `components` | Clara | the `--bs-*`→`--plone-*` bridge + Clara's component restyle |
| `compat` | Clara | the `$spacers` remap + third-party shims (§7) |
| `addons` | add-ons | any add-on that opts in (below) |
| `site` | site integrator | the site's final overrides (§1.5) |

Every functional layer's CSS ships in Clara's one bundle. The `primitives`
layer is special only in that the **class names** it styles (`.plone-stack` …)
are authored by `plone.pageletlayout`'s templates and are the stable hooks §9
guarantees — Clara ships their look, the layout package ships their use.

### Why this order

- `bootstrap` sits **below** `primitives`, `components`, and `site`: any Clara
  or site rule beats a Bootstrap rule of equal-or-higher specificity without a
  fight. A site's `.card { border: 0 }` in `site` beats Bootstrap's
  `.card { … }` even though both are single-class selectors.
- `tokens` sits **above** `reset`/`bootstrap` but the property *values* it sets
  are custom properties, which don't participate in the layer cascade for
  *inheritance* — so a `:root{--plone-*}` in `site` still overrides one in
  `tokens` by normal cascade order. Layers order the *rules*; custom-property
  resolution is orthogonal and always takes the last declared value in scope.
- `compat` is above `components` so a remapped third-party `.mb-3` (§7) lands
  predictably, but below `addons`/`site` so an add-on or the site can still
  correct it.

### What an add-on author must do to participate

An add-on that wants its CSS to lose to `site` but win over stock Bootstrap
wraps its rules in the `addons` layer:

```css
/* collective.someaddon/static/addon.css */
@layer addons {
  .someaddon-widget { border: var(--plone-border); }
}
```

Rules an add-on ships **outside** any layer still win over *all* layered rules
(unlayered beats layered in the cascade) — that is the escape hatch for an
add-on that genuinely must override, and the reason we do not rely on layers for
security-sensitive UI. The guidance: **layer your CSS in `addons`, read
`--plone-*` tokens, and you inherit the theme and stay overridable.**

### Where the lean bundle slots in

The future "lean bundle" (Bootstrap-free Clara) drops the `bootstrap` layer and
the compiled output entirely. The order becomes
`reset, tokens, primitives, components, compat, addons, site` — every other
layer keeps its meaning, every `--plone-*` token keeps its name, and the
hand-written tokens-only utilities file (§7) fills the `compat` layer in
Bootstrap's place. Nothing above `bootstrap` has to move. The lean bundle stays
a **future** stage; the architecture must keep honoring it, but building it is a
later effort.

---

## 3. Layout primitives

**Decision: prefixed, class-based, `plone-` namespace.** `.plone-stack`,
`.plone-cluster`, etc. Prefixed because these are a public, documented API that
must never collide with Bootstrap's or an add-on's unprefixed class — and
`plone-`, not `clara-`, because they are the layout contract bound for
`plone.app.layout`. Class-based (not attribute or utility) because a primitive
is a *named layout intent* with its own custom-property API, and a class is the
stable hook §9 guarantees. The **classes** are authored by `plone.pageletlayout`'s
templates; the **CSS** ships in Clara's `primitives` layer. They are what the
contract templates use **instead of** Bootstrap's spacing/flex utilities — while
Clara still uses Bootstrap's *components*.

Every primitive follows the same contract: **the class sets layout; a
`--plone-*` custom property tunes it; the exception mechanism is to set that
property on a child or a one-off scope — never to add a utility class.**

### Stack — vertical rhythm

```css
@layer primitives {
  .plone-stack {
    display: flex;
    flex-direction: column;
    --plone-stack-space: var(--plone-space-s);
  }
  .plone-stack > * { margin-block: 0; }
  .plone-stack > * + * { margin-block-start: var(--plone-stack-space); }
}
```

- **API:** `--plone-stack-space` (defaults to `--plone-space-s`).
- **Exception:** a single wider gap is set on the element *after* which it
  applies, inline or via a scoped rule — not with `mt-4`:
  `<hr style="--plone-stack-space: var(--plone-space-l)">`.

### Cluster — wrap-friendly horizontal group

```css
@layer primitives {
  .plone-cluster {
    display: flex;
    flex-wrap: wrap;
    align-items: var(--plone-cluster-align, center);
    justify-content: var(--plone-cluster-justify, flex-start);
    gap: var(--plone-cluster-space, var(--plone-space-2xs));
  }
}
```

- **API:** `--plone-cluster-space`, `--plone-cluster-align`,
  `--plone-cluster-justify`.
- **Exception:** push-apart (e.g. brand left, tools right) via
  `--plone-cluster-justify: space-between` on the instance — replaces
  `d-flex justify-content-between`.

### Sidebar — content + fixed-ish rail, collapses gracefully

```css
@layer primitives {
  .plone-sidebar {
    display: flex;
    flex-wrap: wrap;
    gap: var(--plone-sidebar-space, var(--plone-space-m));
  }
  .plone-sidebar > .plone-sidebar__aside {
    flex-basis: var(--plone-sidebar-width, 20rem);
    flex-grow: 1;
  }
  .plone-sidebar > .plone-sidebar__main {
    flex-basis: 0;
    flex-grow: 999;               /* takes all remaining until it can't */
    min-inline-size: var(--plone-sidebar-min, 50%);
  }
}
```

- **API:** `--plone-sidebar-width`, `--plone-sidebar-space`,
  `--plone-sidebar-min` (the wrap threshold).
- **Exception:** side swaps by DOM order + `--plone-sidebar-min`; no `order-*`
  utility.

### Switcher — N-up that flips to stacked below a threshold

```css
@layer primitives {
  .plone-switcher {
    display: flex;
    flex-wrap: wrap;
    gap: var(--plone-switcher-space, var(--plone-space-m));
  }
  .plone-switcher > * {
    flex-grow: 1;
    flex-basis: calc((var(--plone-switcher-threshold, 30rem) - 100%) * 999);
  }
}
```

- **API:** `--plone-switcher-space`, `--plone-switcher-threshold` (the width at
  which it flips from a row to a stack — quantum layout, no media query).
- **Exception:** cap the columns with a scoped `:nth-child` rule if you need
  "max 3 across"; do not reach for `col-md-4`.

### Grid — intrinsic responsive grid

```css
@layer primitives {
  .plone-grid {
    display: grid;
    gap: var(--plone-grid-space, var(--plone-space-m));
    grid-template-columns:
      repeat(auto-fit, minmax(min(var(--plone-grid-min, 16rem), 100%), 1fr));
  }
}
```

- **API:** `--plone-grid-min` (min track width → controls column count),
  `--plone-grid-space`.
- **Exception:** a fixed column count is a scoped
  `grid-template-columns: repeat(3, 1fr)` override of that one instance — this
  is the answer to `.row > .col-4` (§8).

### Center / content-width

```css
@layer primitives {
  .plone-center {
    box-sizing: content-box;
    margin-inline: auto;
    max-inline-size: var(--plone-measure, 65ch);
    padding-inline: var(--plone-center-gutter, var(--plone-space-s));
  }
  .plone-center--wide { --plone-measure: var(--plone-measure-wide); }
}
```

- **API:** `--plone-measure`, `--plone-center-gutter`.
- **Exception:** a wider block uses the modifier or sets `--plone-measure`
  locally — this is how a full-width figure escapes the reading column without a
  `.container-fluid`.

---

## 4. The single viewlet manager and the content views

The base ships **one** `OrderedViewletManager` — `plone.pageletlayout.layout`
— holding a flat sibling list of ~13 element wrappers (`logo`, `anontools`,
`globalnav`, `searchbox`, `breadcrumbs`, `statusmessages`, `socialtags`,
`contentheader`, `byline`, `body`, `copyright`, `colophon`, `siteactions`). The
whole page is that list; there are no nested managers and no shared wrapper
markup between elements (each element's markup travels with the element).

### The content views — the payload (Half B)

The chrome above is the frame; the **content views** are the payload, and they
are the reason this stack exists: `plone.pageletlayout` + this content viewlet
manager is a **full Barceloneta alternative on pagelets**, not a demo. The
target is the complete default-view set for **all 8 stock content types**:

- **Per-item views** — one per type: `document`, `newsitem`, `event`, `file`,
  `image`, `link` (Document already exists; the other five are the build-out).
- **Folderish listing views** — the shared set every container offers:
  `listing`, `summary`, `tabular`, `full`, and `album` (album laid out
  flexbin-style).

There is deliberately **no "flat" listing variant** — the primitives and the
restyled Bootstrap grid cover that ground. Every view lays out with the §3
primitives and reused Plone hooks, never spacing/flex utilities (§7 lint), and
addresses CSS through named hooks + `--plone-*` APIs — never a utility-only
element.

### Decision: single content column

Clara is a **single-column** theme (like Volto): the whole-body manager is a
flat sibling list rendered into one readable content column — there are **no
portlet side-columns**, no `.row`/`.col` content split. The `.plone-sidebar`
primitive (§3) exists for components that locally want a rail, but the page
itself never splits. This falls straight out of the whole-body flat-list
architecture; there is nothing to switch off. Full-width elements escape the
column with `.plone-bleed` (below), which is how a Volto-style full-bleed header
band or hero is achieved without a second column.

### Decision: Stack **composed with** a full-bleed named-column grid

Not one or the other — the layout root is a **grid** that defines the columns,
and the stack rhythm is expressed *through* the grid's `row-gap`. This gives
both the readable measure and the full-bleed escape in one construct, and it is
where the whole page's vertical rhythm lives.

```css
@layer components {
  .plone-layout {
    display: grid;
    row-gap: var(--plone-layout-space, var(--plone-space-m));
    grid-template-columns:
      [full-start] minmax(var(--plone-layout-gutter, var(--plone-space-s)), 1fr)
      [content-start] min(var(--plone-measure, 65ch), 100%
                          - var(--plone-layout-gutter, var(--plone-space-s)) * 2)
      [content-end]   minmax(var(--plone-layout-gutter, var(--plone-space-s)), 1fr)
      [full-end];
  }
  /* every element defaults to the readable content column */
  .plone-layout > * { grid-column: content-start / content-end; }
  /* opt into edge-to-edge */
  .plone-layout > .plone-bleed { grid-column: full-start / full-end; }
  /* bleed but keep inner content aligned to the measure */
  .plone-layout > .plone-bleed--contained {
    grid-column: full-start / full-end;
    display: grid;
    grid-template-columns: subgrid;   /* inherits the named lines */
  }
}
```

Why compose rather than choose: a plain stack cannot give a full-bleed hero its
edge-to-edge background while keeping the hero's *text* on the 65ch measure; the
named-column grid can, and its `row-gap` subsumes everything the
`> * + * { margin-block-start }` stack did — one mechanism, both jobs.

### How a viewlet opts into full-bleed

It adds `plone-bleed` (or `plone-bleed--contained`) to its **own outermost
element** — the markup travels with the element (§ the flat-list rule). No
parent wrapper, no layout template edit:

```html
<!-- a hero pagelet's template -->
<section class="plone-bleed clara-hero">…</section>
```

### How a viewlet overrides its own spacing

It sets `--plone-layout-space` **on itself**, which only affects its own
`row-gap` contribution above it, or it uses `margin-block-start` on its own root
scoped by its own class. It never reaches into a sibling and never uses a
spacing utility:

```css
@layer components { .clara-hero { margin-block-start: var(--plone-space-xl); } }
```

### Visual reordering in CSS, without touching ZCML registration order

Two independent mechanisms, both leaving `viewlets.xml` registration order (and
the flat twin's code order) untouched:

- **`order`** for a purely visual swap within the flat flow:
  `@layer components { .plone-layout > .element-siteactions { order: -1 } }`.
- **Named grid areas** for a structural regional move. Because the children sit
  on named column lines, a Clara variant can assign `grid-row`/area names to
  hoist, say, `breadcrumbs` above `globalnav` visually while the DOM and the
  registration order stay canonical (accessibility + reading order preserved
  where it must be; `order`/grid used only for presentation).

The **content reorder that changes source order** (an editor dragging
`byline` below `body`) is the manager's job via `IViewletSettingsStorage`
(GS `viewlets.xml`, `@@manage-layout-viewlets`, a future drag&drop UI) — that is
a *configuration* reorder, distinct from the *CSS* reorder above. Clara does not
use CSS `order` to fake configuration changes; it uses it only for
presentation-layer polish.

---

## 5. Responsiveness — elastic CSS first, container queries as a fallback

Any element that can render in **both** the wide content column and a narrow
slot (a rail, a card-deck cell) must size itself against **its context**, not a
fixed breakpoint. The reason a listing tile looks right in the main column and
in a 20rem sidebar with zero variant templates.

### The shipped mechanism: restyled Bootstrap + elastic CSS

**By default this is solved without container queries.** The §3 primitives are
already intrinsic — `grid` + `minmax()`/`auto-fit`, the Switcher's quantum flip,
`clamp()` tokens, flexbox wrap — so a tile reflows to its available inline size
with no query at all. Restyled Bootstrap components (their `--bs-*` bound to
`--plone-*`, §6.3) inherit the same fluid rhythm. This elastic approach is the
named, shipped responsiveness model.

### Container queries: a documented fallback, deferred

Container queries (`container-type: inline-size`) remain available as a
**fallback** for the case elastic CSS genuinely cannot hold — a component whose
*internal layout* (not just its wrapping) must change between a wide column and
a narrow rail. They are **deferred**, not part of the shipped contract: revisit
them only if the wide-column-vs-narrow-rail cases in the listing/card views
prove impossible with `grid`+`minmax()`, `clamp()`, and flexbox alone. When
used, a query context declares `container-type: inline-size` on one of the
**reused hooks** (`.entries`, `.card`, a listing wrapper) — never an invented
`.clara-tile`/`-listing`/`-card` context — and queries are written against a
named container so nesting resolves to the intended context.

```css
/* fallback only — used solely where elastic CSS cannot express the change */
@layer components {
  .entries { container: plone-listing / inline-size; }
  @container plone-listing (inline-size > 28rem) {
    .item__layout { grid-template-columns: 12rem 1fr; }  /* image beside text */
  }
}
```

The whole-page layout grid (§4) never uses a container query — it is the
outermost container and legitimately keys off the readable measure.

---

## 6. Bootstrap token bridge — the core

This is how one `--plone-*` edit moves the whole theme. Three mechanisms, in
increasing order of "how much Sass is involved". All three live inside Clara's
single compile (`clara-bootstrap.scss`); there is no base-side half.

### 6.1 Sass entry variables set from tokens (where Bootstrap allows a `var()`)

Bootstrap emits many of its `_root.scss` custom properties as
`--bs-x: #{$x}`. Where `$x` flows straight into a custom property with **no Sass
math on it**, we set `$x` to a `var(--plone-*)` string and Bootstrap prints the
`var()` through. `clara-bootstrap.scss` overrides Bootstrap defaults **before**
`@import "bootstrap"`:

```scss
// clara-bootstrap.scss — Clara's Bootstrap 5.3 build
// values that pass straight through to --bs-* custom properties:
$border-color:    var(--plone-color-border);
$border-radius:   var(--plone-radius-m);
$border-width:    var(--plone-border-width);
```

**Compile reality (found wiring the build, ticket 04):** several tokens one
would *want* here — `$body-color`, `$body-bg`, `$link-color`, `$font-size-base`
— **cannot** be `var()` after all, because Bootstrap 5.3.8 runs them through
compile-time math (`to-rgb`, `rfs()`) that a `var()` string breaks. Those move
into §6.2 as literals, and the runtime `--bs-*`→`--plone-*` bridge (§6.3)
delivers their token value at runtime. The pass-through set is therefore
smaller than it first looks — only the genuinely math-free vars stay here.

### 6.2 Compile-time fallbacks (where Bootstrap needs a literal)

Sass color functions (`shade-color`, `tint-color`, `color-contrast`), the
`$theme-colors` map, **and the math-bearing entry vars just named** cannot take
a `var()` — they must resolve to a literal at compile time. For those, Clara
feeds the **Clara default hex/size** (the same value the token file sets at
runtime) so hover/active shades and contrast picks are computed correctly, then
**rebinds the runtime custom property to the token** so a site's runtime
override still reaches the component (§6.3):

```scss
// literals for Sass math — must match the token file's default value:
$body-color:      #0e222e;      // === --plone-color-text default
$body-bg:         #fafcfe;      // === --plone-color-bg default
$link-color:      #0083be;      // Bootstrap compile seed; runtime link is #006293
$font-size-base:  1rem;         // rfs() math

$primary:   #0083be;            // exact official Plone logo blue
$success:   #2e7d52;
$danger:    #a2080c;
$theme-colors: (
  "primary": $primary, "success": $success, "danger": $danger,
);

@import "bootstrap/scss/bootstrap";
```

The tradeoff, stated plainly: Bootstrap still compiles fallback shades from
these literals, and **every one of them that reaches a shipped component has to
be rebound** — `_clara-states.scss` covers the solid button variants, and
§6.3's third scope covers the rest. A site overriding the semantic roles then
gets runtime-perfect buttons, alerts and validation states.

> **Corrected 2026-07-28.** This paragraph used to claim that "only an
> unbridged third-party Bootstrap derivative may retain a compiled shade".
> That was wrong, and it was only caught when the second theme
> (`plonetheme.derico`) was built on Clara: seven *first-party* components —
> `.pagination`, `.nav-pills`, `.progress-bar`, `.list-group`,
> `.dropdown-item.active`, the outline buttons, and the form-control
> checked/indeterminate/range-thumb properties — still painted the compiled
> `$primary`, for **13 measured Plone-blue spots** on a page whose tokens were
> entirely cyan. Four of them are plain properties with no `--bs-*` knob at
> all, so no amount of token overriding could have reached them. The rebinds
> are now in `_clara-bridge.scss` §3.

**Drift guard.** Because these literals mirror runtime defaults, pytest compares
primary, text, background, border, radius and all four state seeds against the
resolved base⊕brand `:root` values. No theme-colour seed is exempt.

### 6.3 Rebinding Bootstrap's component `--bs-*` to `--plone-*` (the workhorse)

Bootstrap 5.3 exposes component-level custom properties. Clara rebinds them to
`--plone-*` tokens in **one** block in the `components` layer — this is how Clara
gets declarative component spacing with **no `p-3`**, and how the §6.2 literals
regain their runtime tunability:

```css
@layer components {
  :root {
    /* body / surface — reclaims the §6.2 literals at runtime */
    --bs-body-bg:            var(--plone-color-bg);
    --bs-body-color:         var(--plone-color-text);
    --bs-border-color:       var(--plone-color-border);
    --bs-border-radius:      var(--plone-radius-m);
    --bs-link-color-rgb:     /* set via token-derived rgb triplet */ ;

    /* grid gutter — every .row/.col reads this */
    --bs-gutter-x:           var(--plone-space-m);

    /* buttons */
    --bs-btn-padding-x:      var(--plone-space-s);
    --bs-btn-padding-y:      var(--plone-space-2xs);
    --bs-btn-border-radius:  var(--plone-radius-m);

    /* cards */
    --bs-card-spacer-x:      var(--plone-space-m);
    --bs-card-spacer-y:      var(--plone-space-s);
    --bs-card-border-radius: var(--plone-radius-m);
    --bs-card-border-color:  var(--plone-color-border);

    /* nav / navbar / alerts / tables inherit the same tokens … */
    --bs-nav-link-padding-x: var(--plone-space-s);
    --bs-nav-link-padding-y: var(--plone-space-2xs);
    --bs-alert-padding-x:    var(--plone-space-m);
    --bs-alert-padding-y:    var(--plone-space-s);
    --bs-table-cell-padding-x: var(--plone-space-s);
    --bs-table-cell-padding-y: var(--plone-space-2xs);
  }
}
```

A `.card` now spaces itself from `--plone-space-*` with **no utility class on
the markup** — the card template is just `<div class="card">`, and its interior
rhythm is Plone tokens. Change `--plone-space-m` and every card, alert, and grid
gutter moves together.

**The third scope: compile-time literals (added 2026-07-28).** Beyond the two
scopes above — `:root` globals and component-scoped `--bs-*` — there is a third
class the bridge must answer, and it is invisible until a *second* theme exists.
Bootstrap's component mixins resolve `$primary` to a hex the moment Sass runs.
`.pagination { --bs-pagination-active-bg: #0083be }` is not a token reference; it
is a finished value. Worse, `.form-check-input:checked { background-color:
#0083be }` is a plain property with no custom property in sight.

A rule of thumb for anyone extending the bridge:

| what Bootstrap emitted | reachable by a `:root` override? | bridge action |
|---|---|---|
| `--bs-x: var(--bs-global)` | yes, through the global | none — repeating it is dead weight |
| `--bs-x: <literal>` on `:root` | yes | rebind in the `:root` block |
| `--bs-x: <literal>` on the component | **no** | rebind at component scope |
| `property: <literal>` | **no** | restate the property |
| `rgba(var(--bs-x-rgb), …)` | **no** — needs an r,g,b triplet | out of reach; keep it out of contract markup |

The first two are cosmetic; the middle two are the ones that break a downstream
theme, and they are what `_clara-bridge.scss` §3 now covers. The last row is the
documented residual: `--bs-*-rgb` and the `.text-primary` / `.link-primary` /
`.table-primary` utilities that read them cannot be expressed as a var, which is
one more reason contract markup uses none of them (principle 3).

### 6.4 Color modes — dark mode through Clara tokens

Bootstrap 5.3's `[data-bs-theme]` is honored, but dark mode is expressed by
**flipping the semantic tokens**, not by shipping a second Bootstrap theme. One
selector, the same `--plone-*` roles:

```css
@layer tokens {
  /* the attribute is REPEATED on purpose — see the specificity note below */
  [data-bs-theme="dark"][data-bs-theme="dark"] {
    --plone-color-bg:      var(--plone-gray-900);
    --plone-color-surface: var(--plone-gray-700);
    --plone-color-text:    var(--plone-gray-050);
    --plone-color-border:  var(--plone-gray-700);
    /* primary can stay or shift; roles are the only thing that moves */
  }
}
```

**Why the selector is doubled (fixed 2026-07-28).** A plain
`[data-bs-theme="dark"]` scores 0,1,0 — *exactly* what `:root` scores. Both
token partials write `:root` in the same `tokens` layer, and `_clara-brand.scss`
is imported after `_clara-tokens-defaults.scss`, so the brand's light `:root`
was beating the defaults' dark block on source order alone: background, surface,
text, muted, border and on-primary all snapped back to their light values the
moment the switch was flipped. Repeating the attribute lifts the dark blocks to
0,2,0 so dark always wins over light, whatever the import order.

`:root[data-bs-theme="dark"]` would also score 0,2,0 and is **not** used:
Bootstrap allows `data-bs-theme` on any element, and scoped dark regions have to
keep receiving the flips. `tests/test_dark_mode_cascade.py` guards both halves
of that. Note this defect was invisible to `tests/test_color_contrast.py`, whose
`_dark_props()` overlays the partials in import order — a cascade the browser
never runs; the fix makes that model true.

Because §6.3 binds every `--bs-*` to a `--plone-*` role, flipping the roles
flips Bootstrap's components, the primitives, and Clara's own components in one
move. The tokens for `[data-bs-theme]` ship, but **activation is not wired yet**
— nothing sets `data-bs-theme` from `prefers-color-scheme` or a toggle. Wiring
it (from the media query or a control panel) is a planned follow-up; the token
block above is ready for it.

**The result:** a site integrator sets `--plone-color-primary` and
`--plone-space-m` in one CSS file (§1.5) and the entire theme — Bootstrap
components included — responds.

---

## 7. Spacing utility remapping

Bootstrap's `$spacers` map is remapped onto the Plone space scale so that any
`.mb-3` emitted by a **third-party** add-on resolves to `var(--plone-space-s)`
rather than a hardcoded `1rem`. The remap lives **solely in Clara's compile** —
there is no separate base-owned copy.

### The remap (Clara's build) and generated values

```scss
// clara-bootstrap.scss — before @import "bootstrap"
$spacers: (
  0: 0,
  1: var(--plone-space-3xs),   // was .25rem
  2: var(--plone-space-2xs),   // was .5rem
  3: var(--plone-space-s),     // was 1rem
  4: var(--plone-space-m),     // was 1.5rem
  5: var(--plone-space-xl),    // was 3rem
);
```

Generated (excerpt): `.mb-3 { margin-bottom: var(--plone-space-s) !important }`,
`.p-4 { padding: var(--plone-space-m) !important }`,
`.g-2 { --bs-gutter-x/y: var(--plone-space-2xs) }`. A third-party `.mb-3` now
breathes on the Plone scale and reflows fluidly with the viewport, for free.
This is proven end-to-end (a structural test asserts every `$spacers` step lands
on its `--plone-space-*` token; a runtime fixture confirms a foreign `.mb-3`
computes to the fluid token value, not Bootstrap's flat 16px).

### Keep the utility API enabled — the tradeoff, defended

We do **not** `map-remove` the margin/padding utilities. The utility CSS stays
generated and shipped. Cost: a few kB of utility classes the contract markup
never uses, and the theoretical risk that an integrator copies a `.p-3` into a
template. Benefit: **every existing Plone add-on that emits `.mb-3`/`.p-2` keeps
working and lands on the Plone scale automatically** instead of on hardcoded
rems that fight the fluid rhythm. In a CMS whose value is its add-on ecosystem,
silently breaking third-party spacing to enforce purity is the wrong trade. We
buy compatibility and pay a few kB; the lean bundle (below) reclaims the kB.

### The rule, and how it is enforced

**The contract templates and Clara's own templates and docs never use these
classes.** They are a compatibility escape hatch for third-party markup only.
Enforcement is layered:

1. **Lint on the template tree.** A CI check greps
   `plone.pageletlayout/**/templates/**/*.pt` (and Clara's) for
   `class="…(^|\s)(m|p)[trblxy]?-\d|g-\d|d-flex|justify-content-|align-items-…"`
   and fails the build on a hit. (A ruff-style custom check or a plain `grep -E`
   in the test job — the template tree is small and static.)
2. **Review checklist.** Every template PR answers "does this add a spacing/flex
   utility? → use a primitive or a component `--bs-*` instead."
3. **Docs.** This section, plus §3, are the canonical "use the primitive"
   reference; the utilities are documented *only* here, *only* as the
   third-party shim.

### Under the lean bundle

The same remap is reproduced as a **small hand-written tokens-only utilities
file** in the `compat` layer — a couple dozen `.mb-3 { margin-bottom:
var(--plone-space-s) }` rules covering the spacers actually seen in the wild,
generated from the identical `$spacers`→token table. Third-party `.mb-3` keeps
resolving to `--plone-space-s`; the full Bootstrap utility generator is gone.
The `compat` layer's meaning and position (§2) are unchanged, so the swap is a
bundle substitution, not an architecture change.

---

## 8. Which Bootstrap features Clara uses, and which it forbids

### Used — restyled through `--bs-*` (§6.3), never through utilities

- **Components:** `.card`, `.btn` (+ `.btn-*` variants), `.alert`, `.nav` /
  `.navbar`, `.breadcrumb`, `.table`, `.badge`, `.dropdown`, `.pagination`, and
  **forms** (`.form-control`, `.form-select`, `.form-check`, `.input-group`).
  These are real accessibility- and behavior-bearing widgets; reimplementing
  them would be gratuitous. Clara restyles them entirely via their `--bs-*`
  custom properties. Their class names are Plone/Bootstrap's already and are
  reused verbatim (principle #5).
- **Reboot** (Bootstrap's normalize) — kept, sits in the `bootstrap` layer.
- **Color-mode plumbing** `[data-bs-theme]` — kept, driven by tokens (§6.4).

### Forbidden in the contract markup and Clara's own markup

- **Spacing utilities** (`m-*`, `p-*`, `g-*`) — replaced by primitives (§3) and
  component `--bs-*` (§6.3). Shipped-but-shimmed for third parties only (§7).
- **Display / flex / align utilities** (`d-flex`, `justify-content-*`,
  `align-items-*`, `order-*`) — replaced by Cluster / Switcher / Sidebar (§3)
  and, for reordering, §4's `order`/grid-area mechanism.

### Grid: the contract markup uses the **primitives**, not `.row`/`.col-*`

**Decision:** the contract templates lay out with `.plone-grid` /
`.plone-switcher` / `.plone-sidebar` (§3), **not** Bootstrap's `.row`/`.col-*`.
Justification: the Bootstrap grid needs gutter *utility* companions and
breakpoint column classes (`col-md-4`) that hardcode responsiveness and drag in
the exact utility idiom principle #3 forbids; the intrinsic primitives are
viewport-agnostic (they key off container/content, §5) and expose a single
`--plone-*-min`/`-space` knob instead of a dozen column classes. Bootstrap's
grid **stays compiled and enabled** so third-party `.row/.col` markup renders
(its gutters read `--bs-gutter-x` → `--plone-space-m`, §6.3) — it is a compat
surface, exactly like the spacing utilities.

### Navigation — the Volto-style mega menu (native skeleton, enriched panels)

Clara's dropdown mega menu keeps the **native `plone.app.layout` skeleton**
but enriches the panels: `plonetheme/clara/pagelets.py` subclasses
`GlobalSectionsViewlet` (behind a Clara-layer override of the base's
globalnav chrome pagelet — same provider name, `IPlonethemeClaraLayer`) and
takes over item rendering. The top level stays byte-compatible with the
stock viewlet — `.nav-item`/`.nav-link` and the **pure-CSS `.opener`
checkbox** toggle — while a section's first subtree becomes the three-zone
panel from the derico.de design mockups:

```
<li class="section-a has_subtree nav-item">
  <a class="state-published nav-link" aria-haspopup="true">Section A</a>
  <input class="opener" type="checkbox"><label for="…"></label>  ← native toggle
  <div class="has_subtree dropdown megamenu-panel">
    <div class="megamenu-intro"> title · description · overview link </div>
    <ul class="megamenu-links"> described children + .megamenu-sublinks </ul>
    <p class="megamenu-proof"> proof sentence </p>
  </div>
  <label class="megamenu-backdrop" for="…"></label>              ← CSS-only scrim
</li>
```

Zones render only when their data exists. Descriptions ride catalog brains
(`Description` plus one extra memoized depth-1 query for the top level); the
proof sentence and the overview-link label are the **`IMegamenuSection`
behavior**'s two optional fields (on Folder, `Settings` fieldset), reaching
the nav via the `megamenu_proof` / `megamenu_overview_label` metadata columns
— rendering never wakes objects. An empty overview label means no overview
link.

The mega menu styling stays **`clara-`/`megamenu-`** namespaced — Clara's own
non-contract extension. The panel opens on CLICK via the native
`.opener:checked` (never hover); the second label is the click-to-close
backdrop, and `clara.js` adds only the close gestures (outside click, Escape
with focus return, one-panel-at-a-time). The one native *configuration*
Clara sets is `plone.navigation_depth = 3` (so sections carry children and
grandchildren into the panel). No Bootstrap `dropdown` JS is involved, so
the mega menu survives the lean bundle unchanged.

### Bootstrap JavaScript

- **Used:** `dropdown`, `collapse` (navbar toggler + collapsibles), `modal`,
  `offcanvas` (mobile nav / toolbar drawers), `tab`, `alert` (dismiss).
- **Not used:** `carousel`, `scrollspy`, `tooltip`/`popover` (the last two pull
  Popper; Clara prefers native `title`/`[popover]` where possible).
- **Under the lean bundle:** the used plugins survive as the same public data
  API (`data-bs-toggle="…"`). The lean bundle either keeps Bootstrap's JS
  (JS is small and orthogonal to the CSS diet) or swaps in a byte-compatible
  micro-implementation honoring the same `data-bs-*` attributes — the markup
  contract (§9) does not change either way.

---

## 9. Markup contract

These are the **stable class hooks** the base templates guarantee. An integrator
may target them in the `site` layer forever; the lean bundle must honor them
identically. **The rule:** reuse Plone's own semantic class names verbatim; add
a **named `plone-` hook** wherever CSS must address something Plone has no name
for; **never a utility-only element.**

### Stable (semver-minor stable) — rely on these

| Hook | On | Meaning |
|---|---|---|
| `.plone-layout` | the whole-page grid root | the single layout container (§4) |
| `.plone-stack` `.plone-cluster` `.plone-sidebar` `.plone-switcher` `.plone-grid` `.plone-center` | primitives | layout intents (§3), with their `--plone-*` APIs |
| `.plone-bleed`, `.plone-bleed--contained` | any layout child | full-bleed opt-in (§4) |
| `.element-<name>` | each viewlet's outer element | per-element hook, e.g. `.element-globalnav`, `.element-body`, `.element-copyright` — the sanctioned target for element-specific CSS |
| `.entries` `.item` `.summary` `.card` `.table` | listings / content views | **reused Plone/Bootstrap names, verbatim** — the listing/view hooks (§4 payload); they are Plone's, not the theme's, so they are stable by inheritance |
| `#content-core` | the body element wrapper | the content hole (Plone-wide convention, preserved) |
| `#portal-globalnav`, `.nav-item`, `.nav-link`, `.has_subtree`, `.dropdown`, `.opener` | global nav | the **native plone.app.layout** global-sections hooks the mega menu styles (§8) — stable because they are Plone's |
| `.documentFirstHeading`, `.documentDescription` | contentheader | title/description hooks (Plone-wide convention, preserved) |
| `[data-bs-theme]` | root/subtree | color mode (§6.4) |
| every `--plone-*` token | anywhere | the token API (§1) |
| Bootstrap component classes (`.card` `.btn` `.nav` `.table` `.alert` …) | components | restyled via `--bs-*`; the class names are stable |

### May change between minor versions — do NOT rely on these

- The **internal element** structure *inside* a component template beyond the
  hooks above (e.g. the exact `<div>` nesting within `.element-globalnav`).
- The presence or absence of Bootstrap **utility** classes on any element —
  the templates may add/remove `.row`/`.col`/`.navbar-*` internals as the
  primitives absorb them (§10). Target `.element-*`, the reused Plone hooks, and
  tokens, never a utility class.
- The compiled `--bs-*` default *values* (they track token retuning).
- Any container-query `container-name` (§5) — container queries are a deferred
  fallback, not part of the shipped contract.

The contract is: **target `.plone-*`, `.element-*`, the reused Plone hooks
(`.entries`/`.item`/`.summary`/`.card`/`.table`/`#content-core`/…), and
`--plone-*`/`--bs-*` custom properties. Everything else is implementation.**
`clara-*` names (e.g. `.clara-megamenu`) are Clara's own extensions and are
**not** part of the cross-theme contract.

---

## 10. Migration and risk

Blunt about what hurts.

### What breaks for existing add-ons

- **Nothing that reads Bootstrap components or emits spacing utilities** — those
  are shimmed (§7, §8). An add-on shipping `.card`/`.mb-3`/`.row` renders, and
  lands on the Plone scale. This is the deliberate, expensive-in-kB
  compatibility bet.
- **Add-ons that override with raw specificity or `!important`** win *harder*
  than intended now, because Clara never escalates — their unlayered rules beat
  every Clara layer (§2). That is usually fine (their intent was to win) but
  means Clara cannot defensively reclaim those elements without the add-on
  moving into the `addons` layer. Coordinate with high-footprint add-ons.
- **Add-ons that assumed Barceloneta's exact DOM** (deep descendant selectors
  into the old viewlet markup) break — the pagelet layout's DOM is flatter (§4).
  This is real and unavoidable; it is the cost of retiring `main_template` +
  nested viewlet managers.

### Where legacy wrapper markup fights the primitives

The base templates were ported from `derico.pageletui`, which reproduced
**Barceloneta's** classic viewlet markup verbatim to prove parity. That markup
carries the very utility/grid classes principle #3 forbids, and it must be swept
before Clara ships — this cleanup also carries the `clara-*`→`plone-*` namespace
migration for every contract hook and custom property:

- `globalnav.pt`: `<ul class="navbar-nav me-auto">` — `me-auto` is a flex
  utility; the Cluster primitive (`--plone-cluster-justify`) should own that
  push, and `me-auto` must be stripped.
- `searchbox.pt`: `class="d-flex flex-column position-relative"` and
  `form-control me-2` — `d-flex`/`me-2` are utilities fighting a Cluster.
- `breadcrumbs.pt`: an inner `<div class="container">` — a second, redundant
  centering context nested inside `.plone-layout`; delete it and let the layout
  grid place the breadcrumbs.
- `anontools.pt`, `copyright.pt`, `colophon.pt`, `siteactions.pt`,
  `statusmessages.pt`: `.row > .col-12` shells and `.list-inline` — Bootstrap
  grid/utility idiom for what is semantically a Stack or a bare block.

**Prerequisite template cleanup (must land before Clara ships, not after):**

1. Strip every spacing/display/flex utility and every `.row`/`.col-*` shell from
   the contract templates; replace with the semantic element + a `.plone-*`
   primitive class (or nothing, letting `.plone-layout` place it).
2. Give every element its `.element-<name>` outer hook (§9) — several currently
   rely on Barceloneta ids like `#portal-globalnav`; keep the ids for JS/compat
   but add the class as the styling contract.
3. Collapse redundant inner `.container`/`.row` wrappers (breadcrumbs,
   siteactions) — each is an unjustified permanent wrapper under principle #4.
4. Migrate every contract `clara-*`/`--clara-*` hook and property to
   `plone-*`/`--plone-*` (reused Plone names stay verbatim; `.clara-megamenu`
   and brand-only tokens stay `clara-`).
5. Turn on the §7 lint **after** the sweep, so the tree stays clean.

This cleanup is the painful part: it is ~a dozen templates, each a small careful
edit that must preserve the Plone convention hooks (`#content-core`,
`.documentFirstHeading`, ARIA roles, `i18n:` attributes) while shedding the
Bootstrap scaffolding. It cannot be automated safely — the utility classes are
load-bearing for *layout* today, and each removal must be paired with the
primitive that replaces it. Budget it as real work, do it once, and the markup
contract (§9) is what keeps it done.

### Risk register

| Risk | Likelihood | Mitigation |
|---|---|---|
| Compiled `$primary` state shades drift from a runtime token override | medium | §6.2 caveat; set state `--bs-*` explicitly for runtime-critical themes |
| §6.2 literals drift from the runtime token defaults | low | the §6.2 drift guard (pytest + pre-commit) fails the build on mismatch |
| Third-party `!important` defeats Clara | medium | move the add-on into `addons` layer; document the pattern |
| Integrator copies a `.p-3` into a template | low | §7 lint fails the build |
| Cascade-layer support on very old browsers | low | `@layer` is Baseline 2022; Plone 6.2 targets modern browsers |
| Elastic CSS can't hold a wide-vs-rail case | low | the deferred container-query fallback (§5); the layout degrades to single-column, never breaks |
</content>
</invoke>
