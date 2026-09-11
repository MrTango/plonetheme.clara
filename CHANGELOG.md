# Changelog

## 1.0.0a1 (unreleased)

- Hide upgrade profile 1007 from the Add-ons control panel — `HiddenProfiles`
  enumerated 1001 to 1006 and stopped. The test now derives the expected set
  from the registered upgrade profiles instead of a hardcoded list of
  versions, so the next scaffolded step turns it red rather than slipping
  through.

- **Hide the stock multilingual language selector (profile version 1007).**
  The element added in 1006 was written against a layout that rendered no
  stock viewlet manager at all, so `plone.app.multilingual`'s own selector
  was simply absent. `plone.pageletlayout` bridges the stock managers now,
  `plone.portalheader` among them, which turns the same registration into the
  opposite problem: the stock switch renders on every page one row under the
  header, beside the element that exists to replace it. So Clara hides it, the
  trade the base package already makes for the logo, the breadcrumbs and the
  byline -- bridge the manager, hide what we reimplement. Configuration, not a
  code-level exemption: unhide it and hide
  `plonetheme.clara.languageselector` instead to get
  `plone.app.multilingual`'s markup back. The uninstall profile mirrors it:
  Clara's element goes with the browser layer, so a site that drops the theme
  has to get the stock switch back rather than be left with none.

- **The page-tail sub-navigation lists sections, not everything in the
  folder.** It is a way DOWN the site tree -- the sections below the one being
  read -- and it was listing a folder's loose Documents, News Items and Images
  beside them, which turned the tail of a section page into a dump of whatever
  happened to sit next to its default page. Those are leaves of the page being
  read, not branches off it. The catalog query gains ``is_folderish=True``
  rather than a ``portal_type`` list: the question is "does this have a
  subtree", so a project's own folderish type qualifies without being
  enumerated in Clara. A folder holding nothing but loose pages now renders
  nothing at all. Pinned by ``tests/test_subnav.py``.

- **Give a multilingual site its language switch back.** `plone.app.multilingual`
  registers its selector for `plone.app.layout.viewlets.interfaces.IPortalHeader`,
  a viewlet manager the pagelet layout never renders — so on a Clara site with
  two languages the switch was not styled wrong, it was absent, at every width
  and on every page. Nothing short of an element of its own puts it back, and
  it belongs to Clara for the reason the sub-navigation does: a multilingual
  site's switch is generic, and a brand layer only re-points its tokens.

  `plonetheme.clara.languageselector` is that element (profile version 1006),
  placed after `plone.pageletlayout.globalnav` — where the header's utility
  lane begins: language switch, then search. The lookups are
  `plone.app.i18n`'s `LanguageSelector` reused, not ported; which selector
  answers is decided per request, so with `plone.app.multilingual` installed a
  link goes through `@@multilingual-selector` to the *translation* of the
  current page, and without it a link is the plain `?set_language=` switch a
  site with two interface languages wants. Picking by layer inside `update()`
  rather than by a second registration is deliberate: the two browser layers
  are siblings, not a chain, so two registrations would be an ambiguous
  multi-adapter lookup rather than an override.

  It paints codes, not flags: a flag is a country and not a language, and the
  header row has no place for a 16px raster. The native name rides along as
  each link's accessible name and title, so nothing is lost to a screen
  reader, and the current language keeps its link and stays in the row —
  a switch that shows only the language you are NOT in reads as a label, not
  as a choice. A site with one language renders nothing at all. Pinned by
  `tests/test_languageselector.py` and `tests/test_upgrade_1006.py`.

  Two upgrade profiles that were never hidden from the Add-ons panel — 1005
  and 1006 — join the list `getNonInstallableProfiles` returns, and
  `test_setup.py` now walks every version rather than the first four.

- Make the toolbar's pin/unpin toggle findable. The viewlet renders it as a
  bare 16px icon link in the header strip — no hit area past the glyph, no
  hover, and nothing naming it — so people who know Volto's collapsible
  toolbar look for it, do not see it and conclude the rail cannot be collapsed
  at all. The control and its behaviour were never missing, so nothing new was
  added: whichever toggle the state switch is showing now gets a 32px target,
  a hover/focus background and, in the 220px expanded rail, its own name. The
  label is `content: attr(aria-label)` — the string the viewlet already
  renders and Plone already translates ("Unpin" → "Abkoppeln") — so it cannot
  drift from what a screen reader announces, and it appears only where there
  is room to read it: not in the 60px icon rail, and not below 768px, where
  both toggles stay hidden because the expanded state does not exist there.
  Pinned by `tests/test_toolbar.py`.

- Step the editor toolbar aside for data entry on a phone. Below 768px the
  toolbar is a 60px icon rail whose expand toggle is already hidden, so it
  takes an eighth of a 390px screen and cannot show a single label in return —
  and it takes it from the one page whose whole job is field width. On a form
  holding unsaved data the rail is now hidden and `body`'s `padding-left`
  released, which gave the edit form's fields 358px instead of 298px. What
  makes hiding a navigation landmark safe is that the trigger IS the escape
  hatch: the selector requires `form.pat-formunloadalert` *and*
  `#form-buttons-cancel`, so the rail only goes where the page already offers
  a documented way out, and Save and Cancel both land on a view that has the
  toolbar back. Content edit and add forms match; the article view, the search
  page, the control panel overview and `@@aurora-edit` (no z3c.form buttons,
  and its exit lives in the editor's own chrome) do not. Desktop is untouched.
  Pinned by `tests/test_toolbar.py`.

- Let the page-tail sub-navigation stack on a phone. The tiles wrapped
  correctly on their own, but the guard that keeps a wrapped orphan from
  stretching the whole row — `.subnav-list:has(> :nth-child(4)) > li
  { max-inline-size: calc((100% - 2 * gap) / 3) }` — asserted a column count
  the row had never agreed to, and on a 390px screen a third of the row is a
  90px tile: a four-child folder rendered three unreadable columns instead of
  one. Both the wrap and the guard now come from one elastic track list,
  `repeat(auto-fit, minmax(min(100%, 18rem), 1fr))` (§5, no query and no
  breakpoint): `min(100%, …)` collapses the track floor to the row on a phone,
  `auto-fit` drops the tracks no item reaches (a two-child folder gets halves,
  not thirds and a hole) and keeps the ones items do reach, which is what
  holds the orphan at a track's width. The 2-up band a `:nth-child(4)` test
  could never see — three children in a row that seats two — is covered too.
  Pinned by `tests/test_subnav.py::TestSubnavLayout`.

- Style the control panels (`@@overview-controlpanel` and its siblings), which
  Clara had never covered: new `theme/scss/_clara-controlpanel.scss`. Two Clara
  decisions had broken core's Site Setup markup. `$theme-colors` is slimmed to
  five roles, so Bootstrap emitted neither `.btn-light` — every configlet tile
  rendered as a transparent, edgeless rectangle — nor `.btn-secondary`, leaving
  the Cancel button on every control-panel form invisible; the neutral button
  family is now supplied by hand in `_clara-bridge.scss`, collapsed into one
  quiet neutral button bound to the surface/border/text roles instead of
  Bootstrap's grey literals, next to the existing `.btn-outline-light` compat
  block. And the base reset's `svg { display: block }` took the tile icon
  out of the tile's centred text flow and pinned it to the inline start, at its
  16px intrinsic size; the icon now gets the 3rem box Barceloneta pins (through
  a `--plone-configlet-icon-size` knob) and `margin-inline: auto` to re-centre
  it without reverting the reset or overriding core's template. Panel header
  rhythm comes from `--plone-space-l` rather than Barceloneta's flat 2rem.
  Covered by `tests/test_controlpanel.py`.

- Build the theme with pnpm instead of npm, and track `pnpm-lock.yaml` so the
  compiled CSS is reproducible. `package.json`'s `postinstall` and the
  validation steps in the Quanta guide now call `pnpm`. `pnpm-workspace.yaml`
  answers pnpm's build-script prompt for `@parcel/watcher` with `false`: it is
  an optional dependency of sass that only speeds up `sass --watch`, this
  package has no watch script, and sass falls back to chokidar anyway. The
  pinned sass (1.102.0) reproduces the committed `static/clara.min.css`
  byte for byte.

- Re-enable `plone.app.theming` on uninstall
  (`profiles/uninstall/registry.xml`). Clara's default profile switches the
  theming engine off because it styles every page itself; removing the add-on
  left the site with neither Clara's bundle nor the auto-injected `diazo`
  bundle (barceloneta.min.css), i.e. unstyled HTML. Uninstalling now restores
  `IThemeSettings.enabled = True` — plone.app.theming's own default — so a
  site falls back to stock Plone chrome. Covered by
  `TestUninstall.test_theming_reenabled`.

- Track the compiled `static/clara.min.css` in git instead of gitignoring it
  and force-including it into wheels: any build from a fresh clone (mxdev
  checkouts, `uv pip install` editable) failed with "Forced include not
  found" unless `npm run build` had run first. The force-include hook is
  gone; regenerate and commit the bundle alongside scss changes.

- Remove the `plone.bundles/plonetheme-clara` registry records on uninstall
  (`profiles/uninstall/registry.xml`), so clara.min.css and clara.js stop
  loading once the add-on is removed.

- **New named component hook: `--clara-button-border-color`.** `.clara-button`
  hard-coded a 1.5px ink hairline around the CTA pill. That is a Klarsicht
  judgement — amber is light enough to want the edge — and a theme whose accent
  is dark enough to stand alone had no way to drop it except by forking the
  rule. The hook defaults to `var(--clara-ink)`, so Clara's own appearance is
  unchanged. Deliberately a *colour*, not a `border: none` switch: the border
  box has to survive so the pill keeps its metrics and still has an edge in
  forced-colors mode. `tests/test_component_bridge.py` now guards every named
  hook (this one plus `--clara-footer-ground` / `--clara-footer-ink`): each is
  declared with Clara's own value as the default, and each component paints
  through its hook rather than the ladder token behind it.

- **Bridge Bootstrap's compile-time `$primary` literals** (`_clara-bridge.scss`
  §3). Seven components still painted the compiled Plone blue on a theme whose
  tokens were entirely another hue — `.pagination`, `.nav-pills`,
  `.progress-bar`, `.list-group`, `.dropdown-item.active`, the outline button
  variants, and the form-control checked / indeterminate / range-thumb / focus
  properties, four of which are plain properties with no `--bs-*` knob at all
  and so were unreachable by any `:root` override. Found while building the
  second theme on Clara (`plonetheme.derico`): 13 blue spots measured on a
  live page, 0 after. Clara's own appearance is unchanged — every role now
  read already resolved to the value Sass had baked in, and the two
  `color-mix()` calls reproduce Bootstrap's own `tint-color($primary, 50%)` and
  `rgba($primary, .25)` arithmetic. Architecture doc §6.2/§6.3 corrected: the
  old claim that "only an unbridged third-party derivative may retain a
  compiled shade" was wrong.

- **Fix dark mode, which never actually went dark.** `[data-bs-theme="dark"]`
  scores 0,1,0 — the same as `:root` — so `_clara-brand.scss`'s later `:root`
  block silently undid the defaults' dark values for background, surface, text,
  muted, border and on-primary. Both dark blocks now repeat the attribute
  selector (0,2,0), which beats any `:root` in the layer regardless of import
  order while keeping `data-bs-theme` usable on any element, so scoped dark
  regions still work. `tests/test_color_contrast.py` could not have caught this:
  its `_dark_props()` overlays the partials in import order, modelling a cascade
  the browser never runs — the fix makes that model true. New
  `tests/test_dark_mode_cascade.py` guards the shipped bundle.

- Retire the classic-surface stopgaps: `plone.pageletlayout`'s
  `main_template` bridge now frames every unconverted classic page (login,
  `@@search`, edit forms, control panels) in pagelet chrome, so no page
  emits raw classic markup on Clara's layer any more. Deleted
  `_clara-classic.scss` (the 2026-07-19 raw-markup compat chrome) from the
  bundle, and dropped the interim classic-surface `plone.global_sections`
  viewlet override — the `IMainNavigation` manager never renders on the
  bridged surface; the mega panel reaches every page via the globalnav
  chrome pagelet.

- Mega menu intro: one anchor (`a.megamenu-intro-link`) now wraps the
  section title and its description — the description is a click target
  too, like the described child links; hover/focus feedback stays on the
  title, whose arrow moved from the inner link to the heading itself.

- Hide the upgrade profiles (`plonetheme.clara.upgrades:1001…1004`) and the
  uninstall profile from the Add-ons control panel: the `HiddenProfiles`
  utility existed but was never registered in ZCML, so every upgrade profile
  showed up as an installable add-on. Now registered, extended with
  `getNonInstallableProducts`, and covered by a test.

- Mega menu parity with the derico.de design mockups (profile 1004): each
  section panel now carries the mockups' three zones — the section's own
  linked title, description, and overview link on the left; described child
  links with third-level dot rows in the middle; a proof sentence on the
  right. The new `IMegamenuSection` behavior (on Folder, Settings fieldset)
  contributes the optional proof sentence and overview-link label; both reach
  the navigation as catalog metadata columns so rendering never wakes
  objects, and each renders only when filled — an empty overview label means
  no overview link.
  The markup comes from a Clara-layer override of the base globalnav chrome
  pagelet (`pagelets.py` subclasses `GlobalSectionsViewlet`; the top-level
  skeleton stays byte-compatible, so the pure-CSS opener idiom and clara.js
  are untouched). The panel gains the mockups' dimming click-to-close
  backdrop (a second pure-CSS label on the same checkbox) and a clip-path
  reveal (240ms ease-out, reduced-motion safe); zones without data are
  absent, and a new mid-width layout (48–64rem) folds intro and proof into a
  left rail. DE/EN translations included; empty/fallback states covered by
  tests.

- Integrate Quanta's systematic token lessons without importing its namespace:
  `--plone-*` remains the sole public runtime API. The palette is now anchored
  at the official Plone logo's exact `#0083be`; accessible darker same-hue
  steps handle normal links, and exact-blue controls use an explicit near-black
  foreground. Runtime success/warning/danger/info families now include fill,
  text, surface, border and on-fill roles and drive buttons, alerts and form
  validation through `_clara-states.scss`. Contrast and Sass/runtime drift tests
  cover the complete system. The obsolete parallel `_quanta-tokens.scss` file
  is removed.

- Clara does the styling — no Diazo at all (profile 1003, decision
  2026-07-19): installing Clara disables plone.app.theming, which drops the
  injected Barceloneta bundle from the classic-template surface, and the
  bundle's X-Theme-Disabled expression gate is retired (explicitly blanked on
  upgrade — a GS records import never clears omitted keys). Pages the pagelet
  layout does not cover yet (login, @@search, edit forms, control panels,
  sitemap) render their raw classic markup styled by the same clara.min.css:
  the new `_clara-classic.scss` gives that skeleton the Klarsicht chrome
  (header lockup, nav bar over the bare `ul.navbar-nav`, focused login card,
  flattened footer portlet cards into the closing band, hairline search
  results via the list-group `--bs-*` API). The partial retires when pagelet
  coverage reaches every template.

- Craft pass against the clara-base reference (2026-07-19): the footer's three
  native pagelets now read as one closing band flush with the document end
  (CSS `order` sequences links → legal line → colophon; the layout grid no
  longer paints ground below the band, and list primitives re-zero the `ul`
  padding/margin Bootstrap's Reboot re-adds from its later layer).
- Mobile navigation collapses behind a 44px Menu disclosure below 48rem,
  driven by the contract markup's new nav-level `.opener` (no JS); the
  searchbox joins the opened panel. The header keeps logo + Log in on one row.
- The mega panel spans the now full-bleed nav element with 100%-based
  insets — a scrollbar no longer skews column alignment — sizes to its
  content, and speaks the field-guide voice (serif brand column heads).
- Listing rows (`.entries`) carry serif titles at weight 650, matching the
  homepage resource list.
- The byline pagelet's reused viewlet markup (`#section-byline`) is styled at
  the label tier; the author's Bootstrap badge pill is neutralized through its
  own `--bs-badge-*` API (`bg-light`/`text-dark` utilities do not exist in
  Clara's build — `$theme-colors` deliberately drops them).
- The stock events aggregator is moved off the classic-only `event_listing`
  view onto the covered `summary_view` at install time, so the Events section
  renders inside the theme.

- Implement the original clara-base "Klarsicht" exploration
  (`docs/design/clara-base`; its illustration-sampled blue was superseded by
  the official Plone identity integration above), with one amber accent and
  Literata + Source Sans 3 (self-hosted, replacing Inclusive Sans). Every colour is a runtime custom property — the `--clara-*` ladder
  plus the `--plone-*` semantic roles mapped onto it — so themes based on
  Clara override the palette with a plain `:root {}` block.
- Bridge `--bs-body-font-family` onto `--plone-font-body`: Bootstrap's Reboot
  (in the later `bootstrap` layer) beat the reset's font stack, so the brand
  face never reached the page.
- Initial release.
