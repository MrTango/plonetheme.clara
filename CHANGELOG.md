# Changelog

## 1.0.0a1 (unreleased)

- Initial release.
- Add an opt-in search that opens on demand: the `plonetheme.clara.search_on_demand` registry record (off by default, upgrade step 1009).
- Follow the OS colour-scheme preference for dark mode; `data-bs-theme="light"` or `"dark"` on `<html>` still pins a mode.
- Use tokens for the toolbar colours; its dark block only restates what differs.
- Squash upgrade steps 1001–1008 into the 1008 baseline.
- Render Clara in plone.pageletlayout's slot layout: the language switch and search sit in `plone.mainnavigation`, the sub-navigation in `plone.belowcontentbody`.
- Collapse an empty content header.
- Give the content header a switcher layout driven by six `--plone-contentheader-*` tokens.
- Hide plone.app.multilingual's stock language selector, replaced by Clara's; uninstall unhides it.
- List only folderish children in the page-tail sub-navigation.
- Add a header language switch (`plonetheme.clara.languageselector`): language codes, native names as accessible names.
- Make the toolbar's pin/unpin toggle findable: larger target, hover feedback, visible label in the expanded rail.
- Hide the editor toolbar on phones while a form with a Cancel button holds unsaved data.
- Let the sub-navigation tiles stack on a phone with one elastic track list.
- Style the control panels, including neutral `.btn-light` / `.btn-secondary` and centred configlet icons.
- Build the theme with pnpm and track `pnpm-lock.yaml`; silence dependency and `@import` deprecation warnings in the sass build.
- Re-enable plone.app.theming and remove the bundle records on uninstall.
- Track the compiled `static/clara.min.css` in git.
- Add the `--clara-button-border-color` component hook.
- Bridge Bootstrap's compile-time `$primary` literals so components follow a retuned primary.
- Fix dark mode losing to the brand's later `:root` block.
- Drop the classic-surface stopgaps now that pageletlayout frames every classic page.
- Make the mega-menu intro one link over title and description.
- Hide the upgrade and uninstall profiles from the Add-ons control panel.
- Add the three-zone mega-menu panel and the `IMegamenuSection` behavior (proof sentence, overview label).
- Anchor the palette at the Plone logo blue `#0083be` with complete semantic state roles; keep `--plone-*` as the only public API.
- Disable Diazo: Clara styles every page itself.
- Footer as one closing band, a mobile Menu disclosure below 48rem, full-bleed mega panel, serif listing titles, byline styling.
- Move the events aggregator to `summary_view` on install.
- Implement the "Klarsicht" design with Literata and Source Sans 3 (self-hosted).
- Bridge `--bs-body-font-family` onto `--plone-font-body`.
