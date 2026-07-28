"""Tests for upgrade step 1001 -> 1002."""
import pytest
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from plonetheme.clara.testing import INTEGRATION_TESTING


class TestUpgrade1002:
    """Test upgrade to version 1002."""

    layer = INTEGRATION_TESTING

    @pytest.fixture(autouse=True)
    def _setup(self, integration):
        self.portal = integration["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_upgrade_handler_importable(self):
        """Test the upgrade handler can be imported."""
        from plonetheme.clara.upgrades.v1002 import upgrade

        assert callable(upgrade)

    def test_upgrade_handler_runs(self):
        """Test the upgrade handler can be executed."""
        from plonetheme.clara.upgrades.v1002 import upgrade

        setup_tool = self.portal.portal_setup
        upgrade(setup_tool)

    def test_upgrade_adds_jscompilation(self):
        """Running the upgrade re-imports registry.xml on an existing site.

        Simulate a site installed before the bundle carried JS by clearing
        jscompilation, then assert the upgrade restores clara.js.
        """
        from plone.registry.interfaces import IRegistry
        from plonetheme.clara.upgrades.v1002 import upgrade
        from zope.component import getUtility

        key = "plone.bundles/plonetheme-clara.jscompilation"
        registry = getUtility(IRegistry)
        registry[key] = ""
        assert registry[key] == ""

        upgrade(self.portal.portal_setup)

        assert registry[key] == "++resource++plonetheme.clara/clara.js"
