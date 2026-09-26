"""Tests for upgrade step 1007 -> 1008."""
import pytest
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
from zope.component import getUtility

from plonetheme.clara.testing import INTEGRATION_TESTING


PROFILE = "plonetheme.clara:default"
RECORD = "plone.pageletlayout.slot_assignments"
SKINNAME = "Plone Default"
ASSIGNED = {
    "plonetheme.clara.languageselector": "plone.mainnavigation",
    "plone.pageletlayout.searchbox": "plone.mainnavigation",
    "plonetheme.clara.subnav": "plone.belowcontentbody",
}


class TestUpgrade1008:
    layer = INTEGRATION_TESTING

    @pytest.fixture(autouse=True)
    def _setup(self, integration):
        self.portal = integration["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.setup_tool = self.portal.portal_setup
        self.storage = getUtility(IViewletSettingsStorage)
        self.simulate_1007_site()

    def simulate_1007_site(self):
        assignments = dict(api.portal.get_registry_record(RECORD))
        for name in ASSIGNED:
            assignments.pop(name, None)
        assignments["plone.pageletlayout.searchbox"] = "plone.portalheader"
        api.portal.set_registry_record(RECORD, assignments)
        for slot in set(ASSIGNED.values()):
            order = self.storage.getOrder(slot, SKINNAME)
            self.storage.setOrder(slot, SKINNAME, tuple(n for n in order if n not in ASSIGNED))
        self.setup_tool.setLastVersionForProfile(PROFILE, "1007")

    def test_elements_are_assigned(self):
        self.setup_tool.upgradeProfile(PROFILE)
        assignments = api.portal.get_registry_record(RECORD)
        for name, slot in ASSIGNED.items():
            assert assignments[name] == slot

    def test_base_assignments_are_kept(self):
        self.setup_tool.upgradeProfile(PROFILE)
        assert api.portal.get_registry_record(RECORD)["plone.pageletlayout.logo"] == (
            "plone.portalheader"
        )

    def test_the_utility_lane_order(self):
        self.setup_tool.upgradeProfile(PROFILE)
        order = list(self.storage.getOrder("plone.mainnavigation", SKINNAME))
        assert order.index("plone.pageletlayout.globalnav") < order.index(
            "plonetheme.clara.languageselector"
        ) < order.index("plone.pageletlayout.searchbox")

    def test_profile_version(self):
        self.setup_tool.upgradeProfile(PROFILE)
        assert self.setup_tool.getLastVersionForProfile(PROFILE) == ("1008",)
