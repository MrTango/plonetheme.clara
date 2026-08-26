"""Tests for the Clara mega-panel globalnav markup (pagelets.py).

The panel contract: a top-level section with children renders the native
li/link/opener skeleton plus the three-zone panel (intro, described links,
proof) and the pure-CSS backdrop label. Zones without data are absent —
including the overview link — and everything arrives escaped.
"""
import pytest
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from plonetheme.clara.pagelets import ClaraGlobalnavChromePagelet
from plonetheme.clara.testing import INTEGRATION_TESTING


class TestMegamenuMarkup:
    """Markup emitted by the Clara globalnav pagelet."""

    layer = INTEGRATION_TESTING

    @pytest.fixture(autouse=True)
    def _setup(self, integration):
        self.portal = integration["portal"]
        self.request = integration["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        # a fully equipped section: description, proof, custom overview label
        services = api.content.create(
            self.portal,
            "Folder",
            id="services",
            title="Services",
            description="What we build and maintain.",
        )
        services.megamenu_proof = "Twenty years of experience."
        services.megamenu_overview_label = "Browse all services"
        services.reindexObject()
        odoo = api.content.create(
            services,
            "Folder",
            id="odoo",
            title="Odoo",
            description="Business processes, connected.",
        )
        api.content.create(odoo, "Document", id="dev", title="Development")

        # a bare section: no description, no proof, no custom label
        bare = api.content.create(
            self.portal, "Folder", id="bare", title="Bare & Plain"
        )
        api.content.create(bare, "Document", id="child", title="Child Page")

    def _render(self):
        pagelet = ClaraGlobalnavChromePagelet(self.portal, self.request)
        pagelet.update()
        return pagelet.render_globalnav()

    def _panel(self, markup, section_id):
        """The section's <li> chunk, so assertions don't cross panels."""
        start = markup.index(f'<li class="{section_id}')
        end = markup.index("</li>", markup.index("megamenu-backdrop", start))
        return markup[start : end + 5]

    def test_native_skeleton_kept(self):
        markup = self._render()
        panel = self._panel(markup, "services")
        assert 'class="services has_subtree nav-item"' in panel
        assert 'aria-haspopup="true"' in panel
        assert '<input id="navitem-services" type="checkbox" class="opener" />' in panel
        assert '<label for="navitem-services" role="button"' in panel

    def test_three_zones_render(self):
        panel = self._panel(self._render(), "services")
        assert 'class="has_subtree dropdown megamenu-panel"' in panel
        assert '<h2 class="megamenu-title">Services</h2>' in panel
        # like the child links, ONE anchor wraps title and description:
        # the description is a click target too
        assert (
            '<h2 class="megamenu-title">Services</h2>'
            '<p class="megamenu-description">What we build and maintain.</p>'
            "</a>"
            in panel
        )
        assert 'class="megamenu-intro-link"' in panel
        assert ">Browse all services</a>" in panel
        assert (
            '<p class="megamenu-proof">Twenty years of experience.</p>' in panel
        )
        assert 'aria-label="Close menu"' in panel
        assert 'for="navitem-services"' in panel.split("megamenu-backdrop")[1]

    def test_child_links_carry_descriptions_and_sublinks(self):
        panel = self._panel(self._render(), "services")
        assert "<strong>Odoo</strong>" in panel
        assert "<span>Business processes, connected.</span>" in panel
        assert '<ul class="megamenu-sublinks" aria-label="Odoo">' in panel
        assert ">Development</a>" in panel
        # panels never collapse below the first level: exactly ONE opener
        assert panel.count('type="checkbox"') == 1

    def test_empty_zones_are_absent(self):
        panel = self._panel(self._render(), "bare")
        assert "megamenu-description" not in panel
        assert "megamenu-proof" not in panel
        # no overview label set -> no overview link at all
        assert "megamenu-overview" not in panel
        # the title is escaped in the heading
        assert "Bare &amp; Plain</h2>" in panel

    def test_sections_without_children_stay_plain_links(self):
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        api.content.create(self.portal, "Document", id="solo", title="Solo")
        markup = self._render()
        start = markup.index('<li class="solo')
        chunk = markup[start : markup.index("</li>", start) + 5]
        assert "megamenu-panel" not in chunk
        assert "opener" not in chunk
        assert 'aria-haspopup' not in chunk


class TestMegamenuFullPage:
    """End to end: the Clara layer's provider override wins the lookup and
    the panel ships inside a really published page."""

    layer = INTEGRATION_TESTING

    @pytest.fixture(autouse=True)
    def _setup(self, integration):
        self.portal = integration["portal"]
        self.request = integration["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        section = api.content.create(
            self.portal,
            "Folder",
            id="leistungen",
            title="Leistungen",
            description=(
                "Anwendungsentwicklung mit offenem Fundament und einem "
                "klaren Plan für die Jahre nach dem Start."
            ),
        )
        section.megamenu_proof = (
            "Zwanzig Jahre Python-Erfahrung fließen in Architektur, "
            "Betrieb und Weiterentwicklung ein."
        )
        section.megamenu_overview_label = "Alle Leistungen"
        section.reindexObject()
        odoo = api.content.create(
            section,
            "Folder",
            id="odoo",
            title="Odoo",
            description="Geschäftsprozesse verbinden und dauerhaft weiterentwickeln",
        )
        for cid, ctitle in (
            ("entwicklung", "Entwicklung"),
            ("beratung", "Beratung"),
            ("betrieb", "Betrieb"),
        ):
            api.content.create(odoo, "Document", id=cid, title=ctitle)
        api.content.create(
            section,
            "Folder",
            id="plone",
            title="Plone",
            description=(
                "Inhalte, Workflows und Berechtigungen verlässlich organisieren"
            ),
        )
        api.content.create(
            section,
            "Folder",
            id="python",
            title="Django, Pyramid & FastAPI",
            description="Passende Python-Architekturen für individuelle Anwendungen",
        )
        self.page = api.content.create(
            self.portal, "Document", id="ueber", title="Über uns"
        )

    def test_published_page_carries_the_panel(self, tmp_path):
        import os
        from contextlib import suppress

        from plone.api.exc import InvalidParameterError
        from plone.app.testing import logout

        for obj in (
            self.portal["leistungen"],
            self.portal["leistungen"]["odoo"],
            *self.portal["leistungen"]["odoo"].objectValues(),
            self.portal["leistungen"]["plone"],
            self.portal["leistungen"]["python"],
            self.page,
        ):
            # no workflow chain in the sandbox site: already public
            with suppress(InvalidParameterError):
                api.content.transition(obj, "publish")
        logout()
        view = self.page.restrictedTraverse("pagelet_view")
        html = view()
        assert 'class="has_subtree dropdown megamenu-panel"' in html
        assert "megamenu-proof" in html
        assert "megamenu-backdrop" in html

        snapshot_dir = os.environ.get("CLARA_SNAPSHOT_DIR")
        if snapshot_dir:
            with open(
                os.path.join(snapshot_dir, "megamenu-page.html"),
                "w",
                encoding="utf-8",
            ) as fh:
                fh.write(html)


