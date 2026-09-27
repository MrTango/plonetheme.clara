"""Upgrade step 1008 -> 1009: the search_on_demand record."""

import pytest
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

from plonetheme.clara.testing import INTEGRATION_TESTING


PROFILE = "plonetheme.clara:default"
RECORD = "plonetheme.clara.search_on_demand"


class TestUpgrade1009:
    layer = INTEGRATION_TESTING

    @pytest.fixture(autouse=True)
    def _setup(self, integration):
        self.portal = integration["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.setup_tool = self.portal.portal_setup
        del getUtility(IRegistry).records[RECORD]
        self.setup_tool.setLastVersionForProfile(PROFILE, "1008")

    def test_adds_the_record_switched_off(self):
        self.setup_tool.upgradeProfile(PROFILE)
        assert api.portal.get_registry_record(RECORD) is False

    def test_leaves_the_other_registry_records_alone(self):
        api.portal.set_registry_record("plone.navigation_depth", 5)
        self.setup_tool.upgradeProfile(PROFILE)
        assert api.portal.get_registry_record("plone.navigation_depth") == 5

    def test_reaches_the_profile_version(self):
        self.setup_tool.upgradeProfile(PROFILE)
        assert self.setup_tool.getLastVersionForProfile(PROFILE) == ("1009",)
