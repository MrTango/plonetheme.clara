"""Reimport registry.xml (Clara bundle + navigation_depth)."""
import logging

from plone.app.upgrade.utils import loadMigrationProfile


logger = logging.getLogger(__name__)

PROFILE = "profile-plonetheme.clara:default"


def upgrade(context):
    """Upgrade from profile version 1000 to 1001: reimport the registry only."""
    logger.info("Running upgrade step: Reimport registry.xml (Clara bundle + navigation_depth)")
    loadMigrationProfile(context, PROFILE, steps=["plone.app.registry"])
