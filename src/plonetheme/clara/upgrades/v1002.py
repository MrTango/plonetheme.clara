"""Add mega menu close JS (clara.js) to the Clara bundle."""
import logging

from plone.app.upgrade.utils import loadMigrationProfile

logger = logging.getLogger(__name__)

PROFILE = "profile-plonetheme.clara:default"


def upgrade(context):
    """Reimport registry.xml so existing sites pick up the bundle's
    jscompilation (clara.js: outside-click / Escape / one-panel-at-a-time
    close gestures for the mega menu).

    Upgrade from profile version 1001 to 1002. Only the registry import step
    is re-run (purge_old=False), leaving the rest of the profile untouched.
    """
    logger.info("Running upgrade step: Add mega menu close JS (clara.js) to the Clara bundle")
    loadMigrationProfile(context, PROFILE, steps=["plone.app.registry"])
