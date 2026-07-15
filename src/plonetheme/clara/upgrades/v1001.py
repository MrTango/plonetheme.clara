"""Reimport registry.xml (Clara bundle + navigation_depth)."""
import logging

from plone.app.upgrade.utils import loadMigrationProfile

logger = logging.getLogger(__name__)

PROFILE = "profile-plonetheme.clara:default"


def upgrade(context):
    """Reimport registry.xml so existing sites pick up the Clara bundle
    registration and navigation_depth=3.

    Upgrade from profile version 1000 to 1001. Only the registry import step
    is re-run (purge_old=False), leaving the rest of the profile untouched.
    """
    logger.info("Running upgrade step: Reimport registry.xml (Clara bundle + navigation_depth)")
    loadMigrationProfile(context, PROFILE, steps=["plone.app.registry"])
