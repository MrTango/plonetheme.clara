# Clara e2e tests

## Theme parity

`theme-parity.e2e.js` checks that Clara never reaches into the blocks of the
Aurora editor (`plone.blicca.auroraeditor`). It builds the same published
Article (`theme-fixture.js`: image, video, teaser, listing, text, list, table
and column blocks, plus the Image and News Items they point at) on two Plone
sites, one on Barceloneta and one on Clara. It then measures the
`aurora-blocks-view` anonymously at 1400, 1200, 992 and 768px.

Clara may legitimately give the blocks view a different content column than
Barceloneta does. So each block's expected width is `min(content column,
blockWidth token)` (`theme-measure.js`):

- Where that is equal on both sites, the block box and its inner boxes
  (figure, picture, img, iframe, teaser card, listing items, table, columns)
  must match to half a pixel. Any difference fails the test.
- Where it differs, the block is reported with the column that explains it and
  not failed on.

The side-by-side table prints on every run. The script refuses to run when both
sites load the same stylesheets.

## Running

`tests/test_theme_parity.py` runs the script against a throwaway Zope with both
sites: Clara's test site and a plain Barceloneta one, each with
`plone.restapi` and the editor's `default` and `article` profiles. The plain
site has no portlets: Barceloneta's navigation portlet would narrow its column
below the `default` token, and those blocks would go uncompared. The test needs
a checkout of the editor next to Clara's, node, and a Chromium:

```sh
cd e2e && pnpm install && cd ..
uv add --no-sync --optional theme-parity --editable ../plone.blicca.auroraeditor
AURORA_E2E_SMOKE=1 AURORA_E2E_CHROMIUM=/usr/bin/chromium \
  uv run --extra test --extra theme-parity pytest -rsP tests/test_theme_parity.py
git checkout pyproject.toml uv.lock
```

The editor is a private repository, so the `uv add` is never committed; CI
does the same in its `theme-parity` job. Leave `AURORA_E2E_CHROMIUM` unset to
use playwright-core's own Chromium
(`pnpm exec playwright-core install --no-shell chromium`). With
`AURORA_E2E_ARTIFACTS=<dir>`, a failing viewport leaves full-page screenshots
of both sites there. Without `AURORA_E2E_SMOKE=1`, or without the editor, the
test is skipped.

Against two sites of a running instance:

```sh
AURORA_E2E_BASE=<plain site URL> AURORA_E2E_BASE_THEMED=<Clara site URL> \
AURORA_E2E_USER=admin AURORA_E2E_PASSWORD=<password> \
  node e2e/theme-parity.e2e.js
```
