# Changelog

## 1.0.0a1 (unreleased)

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
