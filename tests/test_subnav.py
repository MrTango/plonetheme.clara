"""Tests for the page-tail sub-navigation (pagelets.SubnavChromePagelet).

The gate is the DEFAULT PAGE, not a list of view names. A folder that has one
renders that page, so its children are nowhere on screen and this element is
the only way down; a folder without one renders a listing view that already
shows them. Two consequences are pinned here: the element stays silent in the
listing case, and — because ``context`` IS the default page when one is set —
the children come from the canonical folder rather than from the context.
"""
import pytest
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.interface import alsoProvides

from plonetheme.clara.interfaces import IPlonethemeClaraLayer
from plonetheme.clara.pagelets import SubnavChromePagelet
from plonetheme.clara.testing import INTEGRATION_TESTING


class TestSubnav:
    """What the sub-navigation lists, and when it stays silent."""

    layer = INTEGRATION_TESTING

    @pytest.fixture(autouse=True)
    def _setup(self, integration):
        self.portal = integration["portal"]
        self.request = integration["request"]
        # The chrome pagelet's template is registered on Clara's layer; the
        # IContentTemplate lookup in render() needs it on the request.
        alsoProvides(self.request, IPlonethemeClaraLayer)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        # The case the element exists for: a folder with a default page over
        # three children, so visiting the folder shows none of them.
        odoo = api.content.create(self.portal, "Folder", id="odoo", title="Odoo")
        api.content.create(
            odoo, "Document", id="index", title="Odoo",
            description="Business processes, connected.",
        )
        api.content.create(
            odoo, "Document", id="dev", title="Development",
            description="Modules & integrations.",
        )
        api.content.create(
            odoo, "Document", id="consulting", title="Consulting",
            description="Clarify goals and processes.",
        )
        api.content.create(
            odoo, "Document", id="operations", title="Operations",
            description="Deployment, backups, updates.",
        )
        odoo.setDefaultPage("index")
        self.odoo = odoo

        # No default page: this folder renders a listing view of its children.
        listing = api.content.create(
            self.portal, "Folder", id="listing", title="Listing"
        )
        api.content.create(listing, "Document", id="child", title="Child")
        self.listing = listing

    def _pagelet(self, context):
        pagelet = SubnavChromePagelet(context, self.request)
        pagelet.update()
        return pagelet

    def _titles(self, context):
        return [item["title"] for item in self._pagelet(context).items]

    # -- what it lists ------------------------------------------------------

    def test_default_page_lists_the_folders_other_children(self):
        assert self._titles(self.odoo.index) == [
            "Development",
            "Consulting",
            "Operations",
        ]

    def test_the_default_page_is_not_listed_beside_itself(self):
        assert "Odoo" not in self._titles(self.odoo.index)

    def test_description_is_the_tile_text(self):
        items = self._pagelet(self.odoo.index).items
        assert items[0]["description"] == "Modules & integrations."
        assert items[0]["url"] == self.odoo.dev.absolute_url()

    def test_order_follows_the_folder_not_the_catalog(self):
        self.odoo.moveObjectsToTop(["operations"])
        self.odoo.reindexObject()
        for child in ("index", "dev", "consulting", "operations"):
            self.odoo[child].reindexObject()
        assert self._titles(self.odoo.index)[0] == "Operations"

    def test_exclude_from_nav_is_honoured(self):
        self.odoo.consulting.exclude_from_nav = True
        self.odoo.consulting.reindexObject()
        assert self._titles(self.odoo.index) == ["Development", "Operations"]

    # -- when it stays silent ----------------------------------------------

    def test_folder_without_a_default_page_renders_nothing(self):
        """Its listing view already shows the children."""
        assert self._pagelet(self.listing).render() == ""

    def test_leaf_page_renders_nothing(self):
        """A child that is not anybody's default page has nothing below it."""
        assert self._pagelet(self.odoo.dev).render() == ""

    def test_portal_root_renders_nothing(self):
        """Otherwise the front page repeats the global navigation at its foot."""
        api.content.create(self.portal, "Document", id="home", title="Home")
        self.portal.default_page = "home"
        assert self._pagelet(self.portal.home).render() == ""

    def test_folder_whose_only_child_is_its_default_page_renders_nothing(self):
        solo = api.content.create(
            self.portal, "Folder", id="solo", title="Solo"
        )
        api.content.create(solo, "Document", id="index", title="Solo")
        solo.setDefaultPage("index")
        assert self._pagelet(solo.index).render() == ""

    # -- markup -------------------------------------------------------------

    def test_markup_contract(self):
        markup = self._pagelet(self.odoo.index).render()
        assert 'class="element-subnav"' in markup
        assert 'aria-labelledby="subnav-heading"' in markup
        assert 'id="subnav-heading"' in markup
        assert 'class="subnav-title"' in markup
        assert 'class="subnav-text"' in markup
        assert self.odoo.dev.absolute_url() in markup

    def test_titles_and_descriptions_arrive_escaped(self):
        markup = self._pagelet(self.odoo.index).render()
        assert "Modules &amp; integrations." in markup
        assert "Modules & integrations." not in markup

    def test_a_child_without_a_description_gets_no_empty_line(self):
        api.content.create(self.odoo, "Document", id="bare", title="Bare")
        items = self._pagelet(self.odoo.index).items
        assert items[-1] == {
            "title": "Bare",
            "description": "",
            "url": self.odoo.bare.absolute_url(),
        }
        assert self._pagelet(self.odoo.index).render().count("subnav-text") == 3


class TestSubnavRegistration:
    """The element's place in the whole-body layout order."""

    def test_viewlets_xml_anchors_after_the_body(self):
        """insert-after, so plone.pageletlayout keeps owning the sequence."""
        import plonetheme.clara

        package_dir = plonetheme.clara.__path__[0]
        with open(
            f"{package_dir}/profiles/default/viewlets.xml", encoding="utf-8"
        ) as fh:
            xml = fh.read()
        assert 'manager="plone.pageletlayout.layout"' in xml
        assert 'name="plonetheme.clara.subnav"' in xml
        assert 'insert-after="plone.pageletlayout.body"' in xml
