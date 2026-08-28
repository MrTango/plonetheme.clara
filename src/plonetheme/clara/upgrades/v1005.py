"""Sub-navigation chrome pagelet."""
import logging

from plone.app.upgrade.utils import loadMigrationProfile


logger = logging.getLogger(__name__)

PROFILE = "profile-plonetheme.clara:default"


def upgrade(context):
    """Register plonetheme.clara.subnav in the whole-body layout manager.

    Upgrade from profile version 1004 to 1005.

    Only the ``viewlets`` step: the new element is one entry in the
    ``plone.pageletlayout.layout`` order, and profiles/default/viewlets.xml
    inserts it with ``insert-after`` rather than restating the order, so this
    reimport is additive and idempotent — it cannot disturb an integrator's
    own reordering of the other elements, and re-running it cannot duplicate
    the entry (the importer removes a name before re-inserting it).
    """
    logger.info("Running upgrade step: Sub-navigation chrome pagelet")
    loadMigrationProfile(context, PROFILE, steps=["viewlets"])
