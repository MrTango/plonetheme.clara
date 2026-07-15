# Plonetheme Clara

The first theme built on `plone.pageletlayout`. Clara is where the *look*
lives: it supplies the `--plone-*` token values, the Bootstrap 5.3 build driven
from those tokens, dark mode, and a Volto-style dropdown mega menu — all without
overriding a single template.

## What it ships

- **Brand tokens** (`static/clara-brand.css`) — one `:root {}` block that
  overrides the base defaults. This is the entire runtime difference between the
  bare base and Clara; a site rebrands by layering one more such file (no Sass).
- **The Bootstrap build sources** (`theme/scss/`) — `clara-bootstrap.scss` +
  `_clara-tokens.scss`, driving Bootstrap's Sass from the tokens and remapping
  `$spacers` onto the Clara fluid space scale (§6, §7 of the architecture doc).
- **A Volto-style mega menu** (`static/clara-megamenu.css`) — pure CSS over the
  **native** `plone.app.layout` global-sections markup (the `.has_subtree`
  dropdown tree with its CSS-only `.opener` toggle). No template override, no
  custom JS. Clara sets the native `navigation_depth` so sections carry children
  into the panel.
- **Single content column** — inherited from the base's whole-body layout.

## Design contract

See [docs/clara-theming-architecture.md](docs/clara-theming-architecture.md) —
the decisions-first specification of tokens, cascade layers, primitives, the
single viewlet manager, container queries, the Bootstrap token bridge, the
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
# Clone the repository
git clone https://github.com/collective/plonetheme.clara.git
cd plonetheme.clara

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install in development mode
pip install -e ".[test]"
```

### Running Tests

```bash
pytest
```

### Running Tests with Coverage

```bash
pytest --cov=plonetheme.clara --cov-report=html
```

## License

GPL-2.0-or-later

## Author

Maik Derstappen <md@derico.de>
