# Coding standards

Judgement calls a reviewer checks by reading a change. Formatting, lint and
types belong to the tools.

## Rendered layout is measured in a browser

A change that promises rendered layout or size ships an e2e test that
measures the rendered element in Chromium: `offsetHeight`, a computed style,
a line count. A test that reads stylesheet text or renders in jsdom proves a
rule exists, not that it wins the cascade.

## A GenericSetup profile change comes with an upgrade step

Any change under `profiles/` (registry.xml, types, workflows, catalog,
rolemap, ...) gets an upgrade step, in unreleased alphas too. Scaffold it
with `plonecli add upgrade_step`, which also bumps the profile version, and
narrow its handler to the import step that changed.

## Docstrings are short or absent

A function that needs a paragraph of explanation gets a better name or a
split instead.

## Checks are tests

A behaviour worth checking gets a test in the suite, where it keeps running.
One-off verification scripts stay out of the change.

## README

The README is written for an external developer who decides whether to use
this add-on and how.

- It describes this add-on on its own. Name another add-on only where this
  one depends on it or works with it directly (e.g. it works with
  `plone.app.multilingual`); chapters about other add-ons, such as layout or
  theme packages, belong in their own READMEs.
- Say once that Blicca is the former Classic UI, then call it Blicca for the
  rest of the document.
- The author line reads: Maik Derstappen, [derico.de](https://derico.de), <md@derico.de>
