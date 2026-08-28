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

from plone.app.layout.viewlets.common import GlobalSectionsViewlet
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
