"""Pytest configuration for plonetheme.clara tests."""
import re
from pathlib import Path

import pytest
from pytest_plone import fixtures_factory

from plonetheme.clara.testing import FUNCTIONAL_TESTING
from plonetheme.clara.testing import INTEGRATION_TESTING


BUNDLE = Path(__file__).resolve().parent.parent / "src/plonetheme/clara/static/clara.min.css"


def strip_block_comments(text):
    """Drop `/* … */` only: the bundle carries `http://` in SVG data URIs."""
    return re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)


@pytest.fixture(scope="session")
def bundle():
    """The compiled bundle, block comments stripped."""
    assert BUNDLE.exists(), f"compiled bundle missing at {BUNDLE}; run `pnpm run build`"
    return strip_block_comments(BUNDLE.read_text())


globals().update(
    fixtures_factory(
        (
            (INTEGRATION_TESTING, "integration"),
            (FUNCTIONAL_TESTING, "functional"),
        )
    )
)
