"""Test plonetheme.clara installation."""

import pytest
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
from zope.component import getUtility

from plonetheme.clara.setuphandlers import post_install


class TestSetup:
    """Test installation and setup."""

    @pytest.fixture(autouse=True)
    def _setup(self, integration):
        self.portal = integration["portal"]

    def test_addon_installed(self):
        """Test addon is installed."""
        installer = api.addon.get_installer(self.portal)
        assert installer.is_product_installed("plonetheme.clara")

    def test_browserlayer(self):
        """Test browserlayer is registered."""
        from plone.browserlayer import utils

        from plonetheme.clara.interfaces import IPlonethemeClaraLayer

        assert IPlonethemeClaraLayer in utils.registered_layers()

    def test_upgrade_profiles_hidden_from_addons_panel(self):
        """The upgrade profiles are applied by upgrade steps, never offered
        as installable add-ons.

        Enumerated from the registered profiles rather than from a hardcoded
        list of versions: scaffolding a step registers a new EXTENSION
        profile and does not add it to `HiddenProfiles`, and a hardcoded list
        goes on passing over exactly that gap.
        """
        from plone.base.interfaces import INonInstallable
        from Products.GenericSetup import EXTENSION
        from zope.component import getAllUtilitiesRegisteredFor

        utilities = getAllUtilitiesRegisteredFor(INonInstallable)
        hidden_products = [
            name
            for utility in utilities
            for name in getattr(utility, "getNonInstallableProducts", list)()
        ]
        hidden_profiles = [
            name
            for utility in utilities
            for name in getattr(utility, "getNonInstallableProfiles", list)()
        ]
        setup_tool = api.portal.get_tool("portal_setup")
        registered = [
            info["id"]
            for info in setup_tool.listProfileInfo()
            if info["type"] == EXTENSION and info["product"] == "plonetheme.clara.upgrades"
        ]
        assert registered, "no upgrade profile is registered at all"
        assert "plonetheme.clara.upgrades" in hidden_products
        for profile_id in registered:
            assert profile_id in hidden_profiles

    def test_starter_navigation_and_homepage_are_installed(self):
        """A fresh Clara install has the minimal requested information architecture."""
        assert self.portal.getDefaultPage() == "front-page"
        assert {"front-page", "demo-content", "contact"} <= set(self.portal.objectIds())

        demo = self.portal["demo-content"]
        assert list(demo.objectIds())[:3] == ["pages", "news", "photos"]
        assert demo["pages"]["about-this-site"].portal_type == "Document"
        assert demo["news"]["welcome-to-clara"].portal_type == "News Item"
        assert demo["photos"].getLayout() == "album_view"
        assert demo["photos"]["plone-for-content-teams"].image.filename == "plone_en.png"

        front_page = self.portal["front-page"]
        assert front_page.exclude_from_nav is True
        assert "++resource++plonetheme.clara/plone_en.png" in front_page.text.raw
        assert "https://plone.org/" in front_page.text.raw
        assert "https://community.plone.org/" in front_page.text.raw
        assert "https://github.com/collective/awesome-plone" in front_page.text.raw

    def test_post_install_preserves_editor_owned_homepage(self):
        """Reapplying setup does not overwrite a renamed starter page."""
        front_page = self.portal["front-page"]
        front_page.title = "Our organisation"
        original_text = front_page.text.raw

        post_install(None)

        assert front_page.title == "Our organisation"
        assert front_page.text.raw == original_text
        assert list(self.portal.objectIds()).count("demo-content") == 1
        assert list(self.portal.objectIds()).count("contact") == 1


class TestUninstall:
    """Test uninstallation."""

    @pytest.fixture(autouse=True)
    def _setup(self, integration):
        self.portal = integration["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer = api.addon.get_installer(self.portal)
        self.installer.uninstall_product("plonetheme.clara")

    def test_addon_uninstalled(self):
        """Test addon is uninstalled."""
        assert not self.installer.is_product_installed("plonetheme.clara")

    def test_bundle_records_removed(self):
        """No orphaned bundle: clara.min.css/clara.js must stop loading
        after uninstall."""
        bundle = "plone.bundles/plonetheme-clara"
        assert api.portal.get_registry_record(f"{bundle}.enabled", default=None) is None
        assert (
            api.portal.get_registry_record(f"{bundle}.csscompilation", default=None)
            is None
        )
        assert (
            api.portal.get_registry_record(f"{bundle}.jscompilation", default=None)
            is None
        )

    def test_stock_language_selector_unhidden(self):
        """Clara hides plone.app.multilingual's selector because its own
        element replaces it. That element goes with the browser layer, so
        leaving the stock one hidden would leave a multilingual site with no
        language switch at all."""
        storage = getUtility(IViewletSettingsStorage)
        assert "plone.app.multilingual.languageselector" not in storage.getHidden(
            "plone.portalheader", "Plone Default"
        )

    def test_theming_reenabled(self):
        """Clara disables plone.app.theming while installed; uninstalling has
        to switch it back on, or the site is left with no styling at all."""
        assert (
            api.portal.get_registry_record(
                "plone.app.theming.interfaces.IThemeSettings.enabled",
                default=None,
            )
            is True
        )
