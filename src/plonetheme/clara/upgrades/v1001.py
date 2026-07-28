"""Reimport registry.xml (Clara bundle + navigation_depth)."""
import logging

from .base import reload_gs_profile

logger = logging.getLogger(__name__)


def upgrade(context):
    """A custom upgrade step

    Upgrade from profile version 1000 to 1001.
    """
    logger.info("Running upgrade step: Reimport registry.xml (Clara bundle + navigation_depth)")
    reload_gs_profile(context)
