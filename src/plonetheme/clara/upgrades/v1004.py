"""Mega menu section fields: behavior on Folder, catalog columns."""
import logging

from plone import api
from plone.app.upgrade.utils import loadMigrationProfile


logger = logging.getLogger(__name__)

PROFILE = "profile-plonetheme.clara:default"


def upgrade(context):
    """Upgrade from profile version 1003 to 1004.

    Reimport typeinfo (IMegamenuSection behavior on Folder) and catalog
    (megamenu_proof / megamenu_overview_label metadata columns), then
    refresh existing folders' catalog metadata so the new columns hold
    real values instead of Missing.Value.
    """
    logger.info(
        "Running upgrade step: Mega menu section fields "
        "(behavior on Folder, catalog columns)"
    )
    loadMigrationProfile(context, PROFILE, steps=["typeinfo", "catalog"])

    catalog = api.portal.get_tool("portal_catalog")
    for brain in catalog.unrestrictedSearchResults(portal_type="Folder"):
        obj = brain.getObject()
        catalog.catalog_object(obj, idxs=["portal_type"], update_metadata=True)
    logger.info("Refreshed catalog metadata for existing folders")
