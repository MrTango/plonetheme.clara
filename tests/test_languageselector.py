"""Tests for the header language switch (pagelets.LanguageSelectorChromePagelet).

The element exists because plone.app.multilingual registers its selector for
``plone.app.layout.viewlets.interfaces.IPortalHeader`` — a manager the pagelet
layout did not render at all when this element was written, so on a Clara site
the switch was not styled wrong, it was absent. plone.pageletlayout bridges the
stock managers now, which turns the same registration into the opposite
problem: two switches on every page unless the profile hides the stock one.

That is what these pin: the element is in the layout order, the stock selector
it replaces is hidden, it stays silent on a site with one language, and once a
site has two it renders both codes with the current one marked.
"""

import pytest
from plone import api
from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
from zope.component import getUtility
from zope.interface import alsoProvides

from plonetheme.clara.interfaces import IPlonethemeClaraLayer
from plonetheme.clara.pagelets import LanguageSelectorChromePagelet
from plonetheme.clara.testing import INTEGRATION_TESTING


MANAGER = "plone.pageletlayout.layout"
NAME = "plonetheme.clara.languageselector"

#: The stock selector this element replaces, and the manager the layout
#: bridges it in through.
STOCK_MANAGER = "plone.portalheader"
STOCK = "plone.app.multilingual.languageselector"


class TestLanguageSelectorOrder:
    """The element is IN the whole-body layout, and in the right place."""

    layer = INTEGRATION_TESTING

    @pytest.fixture(autouse=True)
    def _setup(self, integration):
        self.portal = integration["portal"]

    def _order(self):
        storage = getUtility(IViewletSettingsStorage)
        return list(storage.getOrder(MANAGER, "Plone Default"))

    def test_registered_in_the_layout_manager(self):
        assert NAME in self._order()

    def test_opens_the_header_utility_lane(self):
        """After the navigation, before the search: the order the header's
        end lane is read in, and the order the design draws."""
        order = self._order()
        assert order.index("plone.pageletlayout.globalnav") < order.index(NAME)
        assert order.index(NAME) < order.index("plone.pageletlayout.searchbox")

    def test_the_stock_selector_it_replaces_is_hidden(self):
        """Otherwise plone.app.multilingual's own switch rides the
        plone.portalheader bridge onto every page, a row under the header and
        beside this one."""
        storage = getUtility(IViewletSettingsStorage)
        assert STOCK in storage.getHidden(STOCK_MANAGER, "Plone Default")


class TestLanguageSelector:
    """What the switch renders, and when it stays silent."""

    layer = INTEGRATION_TESTING

    @pytest.fixture(autouse=True)
    def _setup(self, integration):
        self.portal = integration["portal"]
        self.request = integration["request"]
        # The chrome pagelet's template is registered on Clara's layer; the
        # IContentTemplate lookup in render() needs it on the request.
        alsoProvides(self.request, IPlonethemeClaraLayer)

    def _pagelet(self):
        pagelet = LanguageSelectorChromePagelet(self.portal, self.request)
        pagelet.update()
        return pagelet

    def _make_multilingual(self):
        api.portal.set_registry_record("plone.available_languages", ["de", "en"])
        api.portal.set_registry_record("plone.use_cookie_negotiation", True)

    def test_silent_on_a_site_with_one_language(self):
        """A switch with nothing to switch to is chrome that only takes
        room; render() returns the empty string, not an empty list."""
        assert self._pagelet().render() == ""

    def test_renders_both_languages(self):
        self._make_multilingual()
        codes = [language["code"] for language in self._pagelet().languages]
        assert codes == ["de", "en"]

    def test_the_label_is_the_code(self):
        """One row in a header bar has no space for "Deutsch · English", and
        the code is how a two-language switch is written."""
        self._make_multilingual()
        labels = [language["label"] for language in self._pagelet().languages]
        assert labels == ["DE", "EN"]

    def test_the_native_name_is_kept_for_assistive_tech(self):
        """Nothing is lost to a screen reader by painting the code: the name
        rides along as the link's accessible name and title."""
        self._make_multilingual()
        names = {
            language["code"]: language["name"] for language in self._pagelet().languages
        }
        assert names["de"] == "Deutsch"
        assert names["en"] == "English"

    def test_the_current_language_is_marked(self):
        self._make_multilingual()
        selected = [
            language["code"]
            for language in self._pagelet().languages
            if language["selected"]
        ]
        assert len(selected) == 1

    def test_markup_carries_the_hooks_a_theme_needs(self):
        """`.element-language` is the layout hook; `currentLanguage` and
        `language-<code>` are Plone's own long-standing class contract, kept
        so an existing sheet still finds the row it expects."""
        self._make_multilingual()
        markup = self._pagelet().render()
        assert 'class="element-language"' in markup
        assert 'id="portal-languageselector"' in markup
        assert "currentLanguage" in markup
        assert "language-de" in markup
        assert "language-en" in markup

    def test_links_switch_the_language(self):
        """Without plone.app.multilingual the base selector answers, and its
        link is the plain `?set_language=` switch — which is what a site with
        two interface languages and no translated content actually wants."""
        self._make_multilingual()
        urls = {
            language["code"]: language["url"] for language in self._pagelet().languages
        }
        assert "set_language=de" in urls["de"]
        assert "set_language=en" in urls["en"]

    def test_silent_when_the_site_hides_the_selector(self):
        """The setting an integrator reaches for when language comes from the
        URL alone: two languages, but no switch asked for."""
        self._make_multilingual()
        api.portal.set_registry_record("plone.use_cookie_negotiation", False)
        api.portal.set_registry_record("plone.always_show_selector", False)
        assert self._pagelet().render() == ""
