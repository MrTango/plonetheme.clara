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
