"""Tests for upgrade step 1005 -> 1006."""
import pytest
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
from zope.component import getUtility

from plonetheme.clara.testing import INTEGRATION_TESTING


MANAGER = "plone.pageletlayout.layout"
NAME = "plonetheme.clara.languageselector"


class TestUpgrade1006:
    """Test upgrade to version 1006."""

    layer = INTEGRATION_TESTING

    @pytest.fixture(autouse=True)
    def _setup(self, integration):
        self.portal = integration["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def _order(self):
        storage = getUtility(IViewletSettingsStorage)
        return list(storage.getOrder(MANAGER, "Plone Default"))

    def test_upgrade_handler_importable(self):
        """Test the upgrade handler can be imported."""
        from plonetheme.clara.upgrades.v1006 import upgrade

        assert callable(upgrade)

    def test_upgrade_handler_runs(self):
        """Test the upgrade handler can be executed."""
        from plonetheme.clara.upgrades.v1006 import upgrade

        setup_tool = self.portal.portal_setup
        upgrade(setup_tool)

    def test_upgrade_puts_the_element_back(self):
        """The case the step exists for: a site installed before 1006 whose
        stored order has no language switch at all."""
        from plonetheme.clara.upgrades.v1006 import upgrade

        storage = getUtility(IViewletSettingsStorage)
        storage.setOrder(
            MANAGER,
            "Plone Default",
            tuple(name for name in self._order() if name != NAME),
        )
        assert NAME not in self._order()

        upgrade(self.portal.portal_setup)
        assert NAME in self._order()

    def test_upgrade_is_idempotent(self):
        """`insert-after` removes a name before re-inserting it, so running
        the step twice cannot leave the element in the order twice."""
        from plonetheme.clara.upgrades.v1006 import upgrade

        upgrade(self.portal.portal_setup)
        upgrade(self.portal.portal_setup)
        assert self._order().count(NAME) == 1
