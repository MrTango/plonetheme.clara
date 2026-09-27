"""IMegamenuSection: a section's proof sentence and overview-link label for
its mega-menu panel. Plain attributes, read through catalog metadata."""
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
