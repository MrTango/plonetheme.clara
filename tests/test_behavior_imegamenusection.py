"""Tests for IMegamenuSection behavior."""
import pytest
from plone.behavior.interfaces import IBehavior
from zope.component import getUtility

from plonetheme.clara.testing import INTEGRATION_TESTING


class TestBehaviorMegamenuSection:
    """Test IMegamenuSection behavior."""

    layer = INTEGRATION_TESTING

    @pytest.fixture(autouse=True)
    def _setup(self, integration):
        self.portal = integration["portal"]

    def test_behavior_registered(self):
        """Test behavior is registered."""
        behavior = getUtility(
            IBehavior,
            name="plonetheme.clara.imegamenusection",
        )
        assert behavior is not None
        assert behavior.title

    def test_behavior_marker(self):
        """Without a factory the schema doubles as the marker."""
        behavior = getUtility(
            IBehavior,
            name="plonetheme.clara.imegamenusection",
        )
        from plonetheme.clara.behaviors.imegamenusection import IMegamenuSection
        assert behavior.marker == IMegamenuSection
