# Plonetheme Clara

A Plone heme based on plonetheme.pageletbase

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
