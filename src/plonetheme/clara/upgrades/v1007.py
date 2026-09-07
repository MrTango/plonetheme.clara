"""Hide the stock multilingual language selector."""
import logging

from plone.app.upgrade.utils import loadMigrationProfile


logger = logging.getLogger(__name__)

PROFILE = "profile-plonetheme.clara:default"


def upgrade(context):
    """Hide plone.app.multilingual's own selector in plone.portalheader.

    Upgrade from profile version 1006 to 1007.

    1006 gave a multilingual site its switch back on the premise that
    plone.app.multilingual registers its selector for a viewlet manager the
    pagelet layout never renders. plone.pageletlayout bridges the stock
    managers now, plone.portalheader among them, so that premise is gone: the
    stock selector renders one row under the header on every page, beside the
    element that exists to replace it.

    Only the ``viewlets`` step, for the reason 1005 and 1006 give: what
    changed is one entry in profiles/default/viewlets.xml, and both of that
    file's nodes are additive — ``<hidden>`` appends to the manager's hidden
    set (plone.pageletlayout hides three of its own viewlets there), the
    ``<order>`` node anchors with ``insert-after``.
    """
    logger.info("Running upgrade step: Hide the stock multilingual language selector")
    loadMigrationProfile(context, PROFILE, steps=["viewlets"])
