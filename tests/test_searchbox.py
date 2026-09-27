"""The searchbox, and its opt-in "opens on demand" mode."""

import re
from pathlib import Path

import plone.pageletlayout
import pytest
from plone import api
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter
from zope.contentprovider.interfaces import IContentProvider
from zope.interface import alsoProvides

from plonetheme.clara.interfaces import IPlonethemeClaraLayer
from plonetheme.clara.testing import INTEGRATION_TESTING


RECORD = "plonetheme.clara.search_on_demand"
BASE_TEMPLATE = (
    Path(plone.pageletlayout.__file__).parent / "pagelets/templates/searchbox.pt"
)
OPENER = 'id="portal-searchbox-opener"'


class TestSearchbox:
    layer = INTEGRATION_TESTING

    @pytest.fixture(autouse=True)
    def _setup(self, integration):
        self.portal = integration["portal"]
        self.request = integration["request"]
        alsoProvides(self.request, IPlonethemeClaraLayer)

    def _render(self):
        view = self.portal.restrictedTraverse("@@view")
        provider = getMultiAdapter(
            (self.portal, self.request, view),
            IContentProvider,
            name="plone.pageletlayout.searchbox",
        )
        provider.update()
        return provider.render()

    def test_on_demand_is_off_by_default(self):
        assert api.portal.get_registry_record(RECORD) is False

    def test_default_searchbox_is_always_open(self):
        html = self._render()
        assert 'id="searchGadget_form"' in html
        assert OPENER not in html
        assert "--plone-cluster-space" in html

    def test_default_searchbox_matches_the_base_markup(self):
        view = self.portal.restrictedTraverse("@@view")
        provider = getMultiAdapter(
            (self.portal, self.request, view),
            IContentProvider,
            name="plone.pageletlayout.searchbox",
        )
        provider.update()
        base = ViewPageTemplateFile(str(BASE_TEMPLATE))(provider)
        assert re.sub(r"\s+", " ", provider.render()) == re.sub(r"\s+", " ", base)

    def test_on_demand_renders_a_toggle_before_the_form(self):
        api.portal.set_registry_record(RECORD, True)
        html = self._render()
        assert html.index(OPENER) < html.index('for="portal-searchbox-opener"')
        assert html.index('for="portal-searchbox-opener"') < html.index('id="searchGadget_form"')

    def test_on_demand_marks_the_box_for_its_styles(self):
        api.portal.set_registry_record(RECORD, True)
        assert 'class="element-searchbox searchbox-on-demand"' in self._render()

    def test_on_demand_keeps_the_form_livesearch_reads(self):
        api.portal.set_registry_record(RECORD, True)
        html = self._render()
        for marker in ('id="searchGadget"', 'name="SearchableText"', "--plone-cluster-space"):
            assert marker in html
        assert 'autocomplete="off"' in html


def _flat(css):
    return re.sub(r"\s+", "", css)


def test_on_demand_hides_all_but_the_toggle_until_opened(bundle):
    """The form, and the live search results inserted beside it."""
    rule = ".searchbox-on-demand>.opener:not(:checked)~:not(.searchbox-toggle){display:none}"
    assert rule in _flat(bundle)


def test_on_demand_opener_stays_focusable(bundle):
    """Hidden visually, never with display:none, so keyboards reach it."""
    rule = re.search(r"\.searchbox-on-demand>\.opener\{([^}]*)\}", _flat(bundle))
    assert rule, "no rule for the searchbox opener"
    assert "opacity:0" in rule[1]
    assert "display:none" not in rule[1]
