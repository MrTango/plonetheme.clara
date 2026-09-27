"""Clara's chrome pagelets: mega-menu globalnav, sub-navigation, language
switch and the on-demand searchbox."""

from html import escape

from plone import api
from plone.app.i18n.locales.browser.selector import LanguageSelector
from plone.app.layout.viewlets.common import GlobalSectionsViewlet
from plone.app.multilingual.browser.selector import LanguageSelectorViewlet
from plone.app.multilingual.interfaces import IPloneAppMultilingualInstalled
from plone.base.utils import safe_text
from plone.memoize.view import memoize
from plone.pageletlayout.chrome import ChromePagelet
from plone.pageletlayout.pagelets.globalnav import GlobalnavChromePagelet
from plone.pageletlayout.pagelets.header import SearchboxChromePagelet
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
from zope.i18n import translate

from plonetheme.clara.i18n import _


def _escaped(template, value):
    """``template`` filled with escaped ``value``, or '' when it is empty."""
    return template.format(escape(safe_text(value))) if value else ""


def _clean(value):
    """A brain metadata value as a stripped string ('' for Missing.Value)."""
    if not isinstance(value, str):
        return ""
    return value.strip()


class ClaraMegamenuSectionsViewlet(GlobalSectionsViewlet):
    """GlobalSectionsViewlet with mega-panel markup: the stock top level, a
    section's panel with intro, described links and proof sentence."""

    # -- extra entry data ---------------------------------------------------

    @property
    @memoize
    def _section_extras(self):
        """id -> {description, proof, overview_label} for depth-1 items."""
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog.searchResults(
            path={"query": self.navtree_path, "depth": 1},
            is_default_page=False,
        )
        return {
            brain.getId: {
                "description": _clean(brain.Description),
                "proof": _clean(getattr(brain, "megamenu_proof", "")),
                "overview_label": _clean(
                    getattr(brain, "megamenu_overview_label", "")
                ),
            }
            for brain in brains
        }

    def customize_tab(self, entry, tab):
        extras = self._section_extras.get(entry["uid"], {})
        entry["description"] = extras.get("description", "")
        entry["proof"] = extras.get("proof", "")
        entry["overview_label"] = extras.get("overview_label", "")

    def customize_entry(self, entry, brain):
        entry["description"] = _clean(brain.Description)

    # -- depth-aware markup -------------------------------------------------

    _panel_markup_template = (
        '<div class="has_subtree dropdown megamenu-panel">'
        '<div class="megamenu-intro">'
        '<a class="megamenu-intro-link" href="{url}">'
        '<h2 class="megamenu-title">{title}</h2>'
        "{description}"
        "</a>"
        "{overview}"
        "</div>"
        '<ul class="megamenu-links">{sub}</ul>'
        "{proof}"
        "</div>"
        '<label class="megamenu-backdrop" for="navitem-{uid}"'
        ' aria-label="{close_label}"></label>'
    )
    _child_markup_template = (
        '<li class="{id} nav-item">'
        '<a href="{url}" class="state-{review_state} nav-link megamenu-link">'
        '<span class="megamenu-link-text">'
        "<strong>{title}</strong>{description}</span></a>"
        "{sub}"
        "</li>"
    )
    _grandchild_markup_template = (
        '<li class="{id} nav-item">'
        '<a href="{url}" class="state-{review_state} nav-link">{title}</a>'
        "</li>"
    )

    def render_item(self, item, path, depth=0):
        if depth == 0:
            return self._render_section(item)
        if depth == 1:
            return self._render_child(item)
        return self._grandchild_markup_template.format(**item)

    def _render_section(self, item):
        """A top-level item: native li/link/opener; panel when it has children."""
        sub = self.build_tree(item["path"], first_run=False, depth=1)
        if not sub:
            item.update(
                {"sub": "", "opener": "", "aria_haspopup": "", "has_sub_class": ""}
            )
            return self._item_markup_template.format(**item)

        panel = self._panel_markup_template.format(
            url=item["url"],
            uid=item["uid"],
            title=item["title"],
            sub=sub,
            close_label=translate(
                _("megamenu_close_label", default="Close menu"),
                context=self.request,
            ),
            description=_escaped(
                '<p class="megamenu-description">{}</p>', item.get("description")
            ),
            overview=_escaped(
                '<p class="megamenu-overview-row">'
                f'<a class="megamenu-overview" href="{item["url"]}">{{}}</a></p>',
                item.get("overview_label"),
            ),
            proof=_escaped('<p class="megamenu-proof">{}</p>', item.get("proof")),
        )
        item.update(
            {
                "sub": panel,
                "opener": self._opener_markup_template.format(**item),
                "aria_haspopup": ' aria-haspopup="true"',
                "has_sub_class": " has_subtree",
            }
        )
        return self._item_markup_template.format(**item)

    def _render_child(self, item):
        """A panel link: bold title + optional description, sublink row."""
        sub = self.build_tree(item["path"], first_run=False, depth=2)
        return self._child_markup_template.format(
            id=item["id"],
            url=item["url"],
            review_state=item["review_state"],
            title=item["title"],
            description=_escaped("<span>{}</span>", item.get("description")),
            sub=(
                f'<ul class="megamenu-sublinks" aria-label="{item["title"]}">'
                f"{sub}</ul>"
                if sub
                else ""
            ),
        )

    def build_tree(self, path, first_run=True, depth=0):
        """Depth-tracking variant; wrapping happens in the items' renderers."""
        return "".join(
            self.render_item(item, path, depth)
            for item in self.navtree.get(path, [])
        )


class ClaraGlobalnavChromePagelet(GlobalnavChromePagelet):
    """The base globalnav pagelet, rendering Clara's mega-panel viewlet."""

    def update(self):
        self.sections = ClaraMegamenuSectionsViewlet(
            self.context, self.request, self.view or self
        )
        # browser:viewlet would stamp this; direct instantiation must too
        self.sections.__name__ = "plone.global_sections"
        self.sections.update()


class SubnavChromePagelet(ChromePagelet):
    """A folder's folderish children, below the folder's default page.

    Only on a default page (other than the front page): there the children
    are nowhere else on screen. ``canonical_object()`` is the folder.
    """

    def update(self):
        self.items = []
        state = getMultiAdapter(
            (self.context, self.request), name="plone_context_state"
        )
        # is_portal_root() already accounts for the default-page case: it is
        # true both for the site root itself and for a default page whose
        # parent is the site root.
        if not state.is_default_page() or state.is_portal_root():
            return
        folder = state.canonical_object()
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog(
            path={"query": "/".join(folder.getPhysicalPath()), "depth": 1},
            is_folderish=True,
            is_default_page=False,
            exclude_from_nav=False,
            sort_on="getObjPositionInParent",
        )
        self.items = [
            {
                "url": brain.getURL(),
                "title": _clean(safe_text(brain.Title)) or brain.getId,
                "description": _clean(safe_text(brain.Description)),
            }
            for brain in brains
        ]

    def render(self):
        """Nothing at all when there are no children."""
        if not self.items:
            return ""
        return super().render()


class LanguageSelectorChromePagelet(ChromePagelet):
    """The header language switch: one row of language codes.

    Reuses plone.app.i18n's ``LanguageSelector``, or plone.app.multilingual's
    subclass when installed (links to the page's translation). Picked in
    ``update()`` because the two layers are siblings, so two registrations
    would be ambiguous. The native name stays as the accessible name.
    """

    def update(self):
        selector_class = LanguageSelector
        if IPloneAppMultilingualInstalled.providedBy(self.request):
            selector_class = LanguageSelectorViewlet
        selector = selector_class(self.context, self.request, self.view or self, None)
        # browser:viewlet stamps __name__ on its synthesized class;
        # instantiated directly it is None.
        selector.__name__ = "plone.app.multilingual.languageselector"
        selector.update()
        self.available = selector.available()
        self.languages = []
        if not self.available:
            return
        # The base selector gives no url; plone.app.multilingual's does.
        view_url = getMultiAdapter(
            (self.context, self.request), name="plone_context_state"
        ).view_url()
        for info in selector.languages():
            code = info["code"]
            self.languages.append(
                {
                    "code": code,
                    "label": code.upper(),
                    "name": info.get("native") or info.get("name") or code,
                    "url": info.get("url") or f"{view_url}?set_language={code}",
                    "selected": bool(info.get("selected")),
                }
            )

    def render(self):
        """Nothing at all when there is no choice to offer."""
        if not self.available:
            return ""
        return super().render()


class ClaraSearchboxChromePagelet(SearchboxChromePagelet):
    """The searchbox, optionally behind a toggle (``search_on_demand``)."""

    def update(self):
        super().update()
        self.on_demand = api.portal.get_registry_record(
            "plonetheme.clara.search_on_demand", default=False
        )
