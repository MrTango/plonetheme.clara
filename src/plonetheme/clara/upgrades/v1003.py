"""Clara styles everything: disable Diazo, ungate the bundle."""
import logging

from plone import api
from plone.app.upgrade.utils import loadMigrationProfile


logger = logging.getLogger(__name__)

PROFILE = "profile-plonetheme.clara:default"


def upgrade(context):
    """Upgrade from profile version 1002 to 1003.

    Reimport registry.xml so existing sites pick up the 2026-07-19 decision:
    Clara does the styling, no Diazo at all. The bundle's X-Theme-Disabled
    expression gate is dropped (Clara loads on every page, classic templates
    included) and plone.app.theming is disabled, which removes the injected
    `diazo` bundle (barceloneta.min.css) from the classic pages.

    Also moves the stock events aggregator off the classic-only event_listing
    view onto the covered summary_view (same fix post_install applies on
    fresh sites).
    """
    logger.info(
        "Running upgrade step: Clara styles everything (disable Diazo, ungate bundle)"
    )
    loadMigrationProfile(context, PROFILE, steps=["plone.app.registry"])

    from plonetheme.clara.setuphandlers import _cover_event_listing

    _cover_event_listing(api.portal.get())
