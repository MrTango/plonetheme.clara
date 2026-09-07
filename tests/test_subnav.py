"""Tests for the page-tail sub-navigation (pagelets.SubnavChromePagelet).

The gate is the DEFAULT PAGE, not a list of view names. A folder that has one
renders that page, so its children are nowhere on screen and this element is
the only way down; a folder without one renders a listing view that already
shows them. Two consequences are pinned here: the element stays silent in the
listing case, and — because ``context`` IS the default page when one is set —
the children come from the canonical folder rather than from the context.

What it lists is the folder's FOLDERISH children only: this is a way down the
tree, not an index of everything filed beside the default page.
"""
import re
from pathlib import Path

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
        # three sub-sections, so visiting the folder shows none of them.
        odoo = api.content.create(self.portal, "Folder", id="odoo", title="Odoo")
        api.content.create(
            odoo, "Document", id="index", title="Odoo",
            description="Business processes, connected.",
        )
        api.content.create(
            odoo, "Folder", id="dev", title="Development",
            description="Modules & integrations.",
        )
        api.content.create(
            odoo, "Folder", id="consulting", title="Consulting",
            description="Clarify goals and processes.",
        )
        api.content.create(
            odoo, "Folder", id="operations", title="Operations",
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

    def test_only_folderish_children_are_listed(self):
        """A way down the tree, not an index of the folder's loose pages.

        Documents, News Items and the rest are leaves of the section being
        read; before this gate they turned the tail of every section page into
        a dump of whatever happened to sit beside the default page.
        """
        api.content.create(
            self.odoo, "Document", id="note", title="A loose page"
        )
        api.content.create(
            self.odoo, "News Item", id="news", title="A news item"
        )
        assert self._titles(self.odoo.index) == [
            "Development",
            "Consulting",
            "Operations",
        ]

    def test_a_folder_of_only_loose_pages_renders_nothing(self):
        leaves = api.content.create(
            self.portal, "Folder", id="leaves", title="Leaves"
        )
        api.content.create(leaves, "Document", id="index", title="Leaves")
        api.content.create(leaves, "Document", id="one", title="One")
        api.content.create(leaves, "Document", id="two", title="Two")
        leaves.setDefaultPage("index")
        assert self._pagelet(leaves.index).render() == ""

    # -- when it stays silent ----------------------------------------------

    def test_folder_without_a_default_page_renders_nothing(self):
        """Its listing view already shows the children."""
        assert self._pagelet(self.listing).render() == ""

    def test_leaf_page_renders_nothing(self):
        """A child that is not anybody's default page has nothing below it."""
        api.content.create(self.odoo, "Document", id="leaf", title="Leaf")
        assert self._pagelet(self.odoo.leaf).render() == ""

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
        api.content.create(self.odoo, "Folder", id="bare", title="Bare")
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


# --------------------------------------------------------------------------- #
# How the tiles lay out. Pinned against the compiled bundle because the defect
# this replaces was a CSS one: a `max-inline-size` of a third, meant to keep a
# wrapped orphan from stretching, applied on a phone too and turned the row
# into three ~90px columns. The mechanism below has no column count in it, so
# there is nothing left to be wrong at one width and right at another.
# --------------------------------------------------------------------------- #

BUNDLE = (
    Path(__file__).resolve().parent.parent
    / "src" / "plonetheme" / "clara" / "static" / "clara.min.css"
)


@pytest.fixture(scope="module")
def subnav_css():
    assert BUNDLE.exists(), (
        f"compiled bundle missing at {BUNDLE} — run `pnpm run build` in "
        f"plonetheme.clara first."
    )
    css = re.sub(r"/\*.*?\*/", "", BUNDLE.read_text(), flags=re.DOTALL)
    return re.sub(r"\s+", "", css)


@pytest.fixture(scope="module")
def subnav_list_rule(subnav_css):
    bodies = re.findall(r"\.subnav-list\{([^}]*)\}", subnav_css)
    assert bodies, ".subnav-list is not styled in the compiled bundle"
    return bodies[0]


class TestSubnavLayout:
    """§5 elastic CSS: the row decides how many tiles fit, not a breakpoint."""

    def test_tiles_are_an_elastic_track_list(self, subnav_list_rule):
        assert "display:grid" in subnav_list_rule
        assert "repeat(auto-fit,minmax(" in subnav_list_rule, (
            "the track list must be auto-fit + minmax: auto-fit collapses the "
            "tracks no item reaches (a two-child folder gets halves, not "
            "thirds) and keeps the ones items do reach (a wrapped orphan stays "
            "a third wide instead of stretching the whole row)"
        )

    def test_the_track_floor_collapses_to_the_row_on_a_phone(
        self, subnav_list_rule
    ):
        """`min(100%, 18rem)`, not a bare `18rem`. On a 390px phone the row is
        narrower than one tile; without the `100%` term the track keeps asking
        for 18rem and the tile overflows its own list."""
        assert "minmax(min(100%,18rem),1fr)" in subnav_list_rule

    def test_no_column_count_is_hardcoded(self, subnav_list_rule):
        """No `repeat(3, …)`: the row counts its own tracks."""
        assert not re.search(r"repeat\(\d", subnav_list_rule)

    def test_no_tile_is_capped_to_a_fraction_of_the_row(self, subnav_css):
        """The regression itself. Any rule that hands a `.subnav-list` child a
        `max-inline-size` is asserting a column count the row has not agreed
        to, and on a phone that count is wrong by three."""
        capped = [
            rule
            for rule in re.findall(r"([^{}]*\.subnav-list[^{}]*)\{([^}]*)\}",
                                   subnav_css)
            if "max-inline-size" in rule[1]
        ]
        assert not capped, f"tile width capped by {capped}"
