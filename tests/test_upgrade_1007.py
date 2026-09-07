"""Tests for upgrade step 1006 -> 1007."""
import pytest
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
from zope.component import getUtility

from plonetheme.clara.testing import INTEGRATION_TESTING


SKINNAME = "Plone Default"
STOCK_MANAGER = "plone.portalheader"
STOCK = "plone.app.multilingual.languageselector"

LAYOUT_MANAGER = "plone.pageletlayout.layout"
OURS = "plonetheme.clara.languageselector"


class TestUpgrade1007:
    """Test upgrade to version 1007."""

    layer = INTEGRATION_TESTING

    @pytest.fixture(autouse=True)
    def _setup(self, integration):
        self.portal = integration["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def _hidden(self, manager=STOCK_MANAGER):
        storage = getUtility(IViewletSettingsStorage)
        return list(storage.getHidden(manager, SKINNAME))

    def _order(self):
        storage = getUtility(IViewletSettingsStorage)
        return list(storage.getOrder(LAYOUT_MANAGER, SKINNAME))

    def test_upgrade_handler_importable(self):
        """Test the upgrade handler can be imported."""
        from plonetheme.clara.upgrades.v1007 import upgrade

        assert callable(upgrade)

    def test_upgrade_handler_runs(self):
        """Test the upgrade handler can be executed."""
        from plonetheme.clara.upgrades.v1007 import upgrade

        setup_tool = self.portal.portal_setup
        upgrade(setup_tool)

    def test_upgrade_hides_the_stock_selector(self):
        """The case the step exists for: a site installed before 1007, whose
        header shows both switches once the layout bridges plone.portalheader."""
        from plonetheme.clara.upgrades.v1007 import upgrade

        storage = getUtility(IViewletSettingsStorage)
        storage.setHidden(
            STOCK_MANAGER,
            SKINNAME,
            tuple(name for name in self._hidden() if name != STOCK),
        )
        assert STOCK not in self._hidden()

        upgrade(self.portal.portal_setup)
        assert STOCK in self._hidden()

    def test_upgrade_keeps_the_base_packages_hidden_viewlets(self):
        """`<hidden>` appends to the manager's set rather than restating it —
        plone.pageletlayout hides the logo, the personal bar's anonymous half
        and the searchbox in this same manager, and they have to stay hidden
        or the header renders each of them twice."""
        from plonetheme.clara.upgrades.v1007 import upgrade

        upgrade(self.portal.portal_setup)
        assert {"plone.logo", "plone.anontools", "plone.searchbox"} <= set(
            self._hidden()
        )

    def test_upgrade_leaves_our_own_element_in_the_order(self):
        """Hiding the stock one must not disturb the element that replaces it."""
        from plonetheme.clara.upgrades.v1007 import upgrade

        upgrade(self.portal.portal_setup)
        assert self._order().count(OURS) == 1

    def test_upgrade_is_idempotent(self):
        from plonetheme.clara.upgrades.v1007 import upgrade

        upgrade(self.portal.portal_setup)
        once = (self._hidden(), self._order())
        upgrade(self.portal.portal_setup)
        assert (self._hidden(), self._order()) == once
