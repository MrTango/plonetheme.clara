"""Tests for upgrade step 1000 -> 1001."""
import pytest
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from plonetheme.clara.testing import INTEGRATION_TESTING


class TestUpgrade1001:
    """Test upgrade to version 1001."""

    layer = INTEGRATION_TESTING

    @pytest.fixture(autouse=True)
    def _setup(self, integration):
        self.portal = integration["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_upgrade_handler_importable(self):
        """Test the upgrade handler can be imported."""
        from plonetheme.clara.upgrades.v1001 import upgrade

        assert callable(upgrade)

    def test_upgrade_handler_runs(self):
        """Test the upgrade handler can be executed."""
        from plonetheme.clara.upgrades.v1001 import upgrade

        setup_tool = self.portal.portal_setup
        upgrade(setup_tool)

    def test_upgrade_reimports_registry(self):
        """Running the upgrade re-imports registry.xml on an existing site.

        Simulate a site installed before the registry records existed by
        clobbering navigation_depth, then assert the upgrade restores the
        profile value (3).
        """
        from plone.registry.interfaces import IRegistry
        from plonetheme.clara.upgrades.v1001 import upgrade
        from zope.component import getUtility

        registry = getUtility(IRegistry)
        registry["plone.navigation_depth"] = 1
        assert registry["plone.navigation_depth"] == 1

        upgrade(self.portal.portal_setup)

        assert registry["plone.navigation_depth"] == 3
