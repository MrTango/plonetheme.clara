"""Clara's globalnav chrome pagelet: the mega-panel markup enrichment.

The base pagelet (plone.pageletlayout.pagelets.globalnav) reuses the stock
GlobalSectionsViewlet unchanged and Clara used to style only that native,
titles-only markup. The design mockups' panel carries more than titles:
the opened section's own description, described child links, and a proof
sentence (plonetheme.derico/docs/design/derico.de/site — the Jahresringe
mockups' three-zone
panel). That data cannot be styled into existence, so Clara subclasses the
viewlet and takes over item rendering.

What stays native, what changes:

* The top-level skeleton is byte-compatible with the stock viewlet: the
  ``li.nav-item`` items, ``a.state-….nav-link`` links, and the pure-CSS
  ``input.opener`` + ``label`` toggles are emitted from the inherited
  templates, so _clara-megamenu.scss's bar/toggle rules and clara.js keep
  working against the documented contract.
* A section's first subtree becomes the three-zone panel instead of a bare
  ``ul``: intro (one link over title and description, like the child links,
  plus the overview link), described child links with sublink rows, and the
  proof sentence. Zones render only when
  their data exists — including the overview link, which appears only when
  its behavior field is filled. A second ``label.megamenu-backdrop`` bound
  to the same checkbox provides the pure-CSS click-to-close scrim.
* Depth 1 and 2 items drop their openers: panels never collapse below the
  first level, so those checkboxes were dead weight the CSS had to hide.

Data paths (all brain metadata; rendering never wakes objects):

* child descriptions ride the standard ``Description`` column via
  ``customize_entry``;
* the top-level sections' description, proof sentence, and overview label
  come from one extra depth-1 catalog query (``_section_extras``, memoized
  per request) because ``portal_tabs`` dicts carry no custom columns. The
  proof/label columns are the IMegamenuSection behavior's
  (profiles/default/catalog.xml).
"""

from html import escape

from plone.app.i18n.locales.browser.selector import LanguageSelector
from plone.app.layout.viewlets.common import GlobalSectionsViewlet
from plone.app.multilingual.browser.selector import LanguageSelectorViewlet
from plone.app.multilingual.interfaces import IPloneAppMultilingualInstalled
from plone.base.utils import safe_text
from plone.memoize.view import memoize
from plone.pageletlayout.chrome import ChromePagelet
from plone.pageletlayout.pagelets.globalnav import GlobalnavChromePagelet
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
from zope.i18n import translate

from plonetheme.clara.i18n import _


def _clean(value):
    """A brain metadata value as a stripped string ('' for Missing.Value)."""
    if not isinstance(value, str):
        return ""
    return value.strip()


class ClaraMegamenuSectionsViewlet(GlobalSectionsViewlet):
    """GlobalSectionsViewlet with depth-aware mega-panel item markup."""

    # -- extra entry data ---------------------------------------------------

    @property
    @memoize
    def _section_extras(self):
        """id -> {description, proof, overview_label} for depth-1 items.

        One catalog query per render on top of the viewlet's own; the
        portal_tabs dicts don't carry the behavior's metadata columns.
        """
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

        description = item.get("description", "")
        proof = item.get("proof", "")
        overview_label = item.get("overview_label", "")
        panel = self._panel_markup_template.format(
            url=item["url"],
            uid=item["uid"],
            title=item["title"],
            sub=sub,
            close_label=translate(
                _("megamenu_close_label", default="Close menu"),
                context=self.request,
            ),
            description=(
                f'<p class="megamenu-description">{escape(safe_text(description))}</p>'
                if description
                else ""
            ),
            overview=(
                '<p class="megamenu-overview-row">'
                f'<a class="megamenu-overview" href="{item["url"]}">'
                f"{escape(safe_text(overview_label))}</a></p>"
                if overview_label
                else ""
            ),
            proof=(
                f'<p class="megamenu-proof">{escape(safe_text(proof))}</p>'
                if proof
                else ""
            ),
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
        description = item.get("description", "")
        return self._child_markup_template.format(
            id=item["id"],
            url=item["url"],
            review_state=item["review_state"],
            title=item["title"],
            description=(
                f"<span>{escape(safe_text(description))}</span>"
                if description
                else ""
            ),
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
        # see the base class: browser:viewlet would stamp this; direct
        # instantiation must, too.
        self.sections.__name__ = "plone.global_sections"
        self.sections.update()


class SubnavChromePagelet(ChromePagelet):
    """The page-tail sub-navigation: a folder's children, below its own page.

    Gated on the DEFAULT PAGE, not on a list of view names. A folder that has
    a default page renders that page, so its children are nowhere on screen and
    this element is the only way down; a folder WITHOUT one renders a listing
    view, which already shows them. Reading the content state instead of the
    layout name means no hardcoded list of listing views to keep current, and
    no false positive on a custom one.

    That gate also fixes where the children come from. When a folder has a
    default page, ``self.context`` IS that page — a Document, with no children
    of its own — so querying the context would render nothing on exactly the
    pages this element exists for. ``canonical_object()`` resolves back to the
    folder, and it is only meaningful once ``is_default_page()`` is true.

    ``is_portal_root()`` covers the front page, whose canonical object is the
    site root: without it every top-level section would be listed at the foot
    of the home page, which is the global navigation said twice.

    Only FOLDERISH children are listed. This element is a way DOWN the site
    tree — the sections below the one being read — not an index of everything
    filed in the folder. A folder's loose Documents, News Items or Images are
    leaves of the current page, not branches off it, and listing them turned
    the tail of a section page into a dump of whatever happened to sit beside
    its default page. ``is_folderish`` rather than ``portal_type="Folder"``:
    the test is "does this have a subtree", so a Large Plone Folder or a
    project's own folderish type qualifies without being enumerated here.

    Brain metadata only — rendering never wakes an object.

    Markup (templates/subnav.pt), kept comment-free because a chrome template's
    comments ship on every response: a labelled <nav> landmark around an <h2>
    and a list of tiles, one <a> per tile wrapping both lines so there is no
    nested interactive element to tab past. Styling: theme/scss/_clara-subnav.scss.
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
        """Nothing at all when there is nothing to point at.

        A folder whose only child is its own default page filters down to zero
        items, and an empty heading over an empty list is worse than silence.
        """
        if not self.items:
            return ""
        return super().render()


class LanguageSelectorChromePagelet(ChromePagelet):
    """The language switch: one row of language codes in the header.

    A NEW element in the whole-body layout, and the reason it has to be one:
    ``plone.app.multilingual`` registers its selector for
    ``plone.app.layout.viewlets.interfaces.IPortalHeader``, a manager the
    pagelet layout never renders. On a Clara site the switch is therefore not
    styled wrong — it is absent, at every width, however many languages the
    site has. Nothing short of an element of its own puts it back.

    It belongs to Clara rather than to a brand theme for the reason the
    sub-navigation does: a multilingual site's switch is generic, and a brand
    layer only re-points its tokens.

    The lookups are ``plone.app.i18n``'s ``LanguageSelector`` — the languages
    tool, the bindings, the ordering — REUSED, not ported (the ticket-09
    rule). Which selector is asked depends on the request: with
    ``plone.app.multilingual`` installed its subclass answers, so a link goes
    through ``@@multilingual-selector`` to the *translation* of the current
    page; without it the base answers and a link is the plain
    ``?set_language=`` switch. Picking by layer inside ``update()`` rather
    than by a second registration is deliberate: the two browser layers are
    siblings, not a chain, so two registrations would be an ambiguous
    multi-adapter lookup rather than an override.

    Codes, not flags. ``showFlags()`` is honoured to the extent Clara can:
    the theme draws with type, a flag is a country and not a language, and
    the header row has no place for a 16px raster. The native name rides
    along as the link's accessible name, so nothing is lost to a screen
    reader.

    Markup (templates/languageselector.pt), comment-free because a chrome
    template's comments ship on every response. Styling:
    theme/scss/_clara-language.scss.
    """

    def update(self):
        selector_class = LanguageSelector
        if IPloneAppMultilingualInstalled.providedBy(self.request):
            selector_class = LanguageSelectorViewlet
        selector = selector_class(self.context, self.request, self.view or self, None)
        # browser:viewlet stamps __name__ on its synthesized class;
        # instantiated directly it is None (the ticket-07 wrapper gotcha).
        selector.__name__ = "plone.app.multilingual.languageselector"
        selector.update()
        self.available = selector.available()
        self.languages = []
        if not self.available:
            return
        # The base selector hands over no link at all — classically the
        # template built one, and this is that line, kept here so the
        # template stays a template. plone.app.multilingual's subclass DOES
        # hand one over (through @@multilingual-selector, to the translation
        # of this page rather than to this page in another language), and it
        # wins wherever it is there.
        view_url = getMultiAdapter(
            (self.context, self.request), name="plone_context_state"
        ).view_url()
        for info in selector.languages():
            code = info["code"]
            self.languages.append(
                {
                    "code": code,
                    # the painted label: the code, the way the switch is
                    # written when there is one row for it and no room for
                    # "Deutsch · English · Nederlands"
                    "label": code.upper(),
                    "name": info.get("native") or info.get("name") or code,
                    "url": info.get("url") or f"{view_url}?set_language={code}",
                    "selected": bool(info.get("selected")),
                }
            )

    def render(self):
        """Nothing at all when there is no choice to offer.

        ``available()`` is false on a site with one language, and on one whose
        languages tool is configured never to show a selector — the setting an
        integrator reaches for when language comes from the URL alone.
        """
        if not self.available:
            return ""
        return super().render()
