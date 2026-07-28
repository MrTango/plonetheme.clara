"""IMegamenuSection behavior.

Two optional editorial fields for the mega-menu panel of a top-level
navigation section (see theme/scss/_clara-megamenu.scss and the Clara
globalnav pagelet): a proof sentence for the panel's third column and a
label for the section overview link. Both render only when filled; an
empty label means no overview link.

Storage is plain attributes on the content object (no factory), so the
values reach the navigation through catalog metadata columns
(profiles/default/catalog.xml) without waking objects.
"""
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import provider

from plonetheme.clara.i18n import _


@provider(IFormFieldProvider)
class IMegamenuSection(model.Schema):
    """Extra mega-menu fields for a top-level navigation section."""

    model.fieldset(
        "settings",
        label=_("Settings"),
        fields=["megamenu_proof", "megamenu_overview_label"],
    )

    megamenu_proof = schema.Text(
        title=_("Navigation proof sentence"),
        description=_(
            "One short proof statement shown beside this section's links "
            "in the navigation panel. Leave empty to omit it."
        ),
        required=False,
    )

    megamenu_overview_label = schema.TextLine(
        title=_("Navigation overview label"),
        description=_(
            "Label for the link to this section's overview page in the "
            "navigation panel. Leave empty to omit the link."
        ),
        required=False,
    )
