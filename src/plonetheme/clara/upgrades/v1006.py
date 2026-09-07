"""Language switch chrome pagelet."""
import logging

from plone.app.upgrade.utils import loadMigrationProfile


logger = logging.getLogger(__name__)

PROFILE = "profile-plonetheme.clara:default"


def upgrade(context):
    """Register plonetheme.clara.languageselector in the whole-body layout manager.

    Upgrade from profile version 1005 to 1006.

    Only the ``viewlets`` step, for the reason 1005 gives: the new element is
    one entry in the ``plone.pageletlayout.layout`` order, and
    profiles/default/viewlets.xml inserts it with ``insert-after`` rather than
    restating the order, so this reimport is additive and idempotent.
    """
    logger.info("Running upgrade step: Language switch chrome pagelet")
    loadMigrationProfile(context, PROFILE, steps=["viewlets"])
