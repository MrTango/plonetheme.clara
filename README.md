# Plonetheme Clara

The first theme built on `plone.pageletlayout`. Clara is where the *look*
lives: it supplies the `--plone-*` token values, the Bootstrap 5.3 build driven
from those tokens, dark mode, and a Volto-style dropdown mega menu — all without
overriding a single template.

## What it ships

- **A useful first install** — a minimal Clara homepage using the Plone logo and
  community resources, plus `Demo content` (Pages, News, Photos) and an editable
  Contact page. Existing editor-owned pages are preserved when the profile is
  reapplied.
- **One public token contract** (`--plone-*`) — Clara supplies a systematic
  Plone-blue ramp anchored at the official logo's exact `#0083be`, accessible
  text/control role splits, semantic state families, fluid rhythm and motion.
  A site rebrands by layering one later `:root {}` block; no Sass and no
  competing `--quanta-*` namespace.
- **The Bootstrap build sources** (`theme/scss/`) — `clara-bootstrap.scss` +
  `_clara-tokens.scss` drive Bootstrap's compile-time fallbacks, while
  `_clara-bridge.scss` and `_clara-states.scss` rebind components to runtime
  roles. `$spacers` maps onto Clara's fluid space scale (§6–7).
- **A Volto-style mega menu** (`theme/scss/_clara-megamenu.scss`, compiled into
  `static/clara.min.css`) — the stock global-sections markup with richer panels
  (section intro, described child links, a proof sentence from the
  `IMegamenuSection` behavior). A CSS-only `.opener` toggle; `clara.js` only
  adds the close gestures.
- **Single content column** — inherited from the base's slot layout.

## Dark mode

Clara follows the visitor's OS preference (`prefers-color-scheme`). To pin a
mode, set `data-bs-theme` on the `<html>` element:

- `data-bs-theme="light"` keeps a site light on a dark OS.
- `data-bs-theme="dark"` makes a site dark on a light OS. It also works on any
  inner element to darken just that region.

## Search on demand

Set the registry record `plonetheme.clara.search_on_demand` to `True` to show
a search toggle in the header instead of an always-open field:

```xml
<record name="plonetheme.clara.search_on_demand">
  <value>True</value>
</record>
```

## Design contract

See [docs/clara-theming-architecture.md](docs/clara-theming-architecture.md) —
the decisions-first specification of tokens, cascade layers, primitives, the
slot layout, container queries, the Bootstrap token bridge, the
spacer remap, the markup contract, and migration risk.

## Features

- Compatible with Plone 6.2+

## Installation

Add `plonetheme.clara` to your project's dependencies:

```python
# In your pyproject.toml
dependencies = [
    "plonetheme.clara",
    # ...
]
```

Then activate the addon in your Plone site's control panel or via GenericSetup.

## Development

### Setup

```bash
git clone https://github.com/MrTango/plonetheme.clara.git
cd plonetheme.clara
uv sync --extra test
pnpm install   # fetches Bootstrap and builds static/clara.min.css
```

`plone.pageletlayout` and `plone.app.viewletmanager` are editable checkouts
expected next to this repository (see `[tool.uv.sources]`).

### Building the stylesheet

```bash
pnpm run build
```

### Running tests

```bash
uv run pytest
uv run pytest --cov=plonetheme.clara --cov-report=html
```

## License

GPL-2.0-or-later

## Author

Maik Derstappen <md@derico.de>
