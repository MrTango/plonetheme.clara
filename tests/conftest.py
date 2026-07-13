"""Pytest configuration for plonetheme.clara tests."""
from pytest_plone import fixtures_factory

from plonetheme.clara.testing import FUNCTIONAL_TESTING
from plonetheme.clara.testing import INTEGRATION_TESTING


globals().update(
    fixtures_factory(
        (
            (INTEGRATION_TESTING, "integration"),
            (FUNCTIONAL_TESTING, "functional"),
        )
    )
)
