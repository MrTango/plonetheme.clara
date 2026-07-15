"""Shared upgrade step utilities for plonetheme.clara."""
from plone.app.upgrade.utils import loadMigrationProfile


def reload_gs_profile(context):
    """Reload the default GenericSetup profile."""
    loadMigrationProfile(context, "profile-plonetheme.clara:default")
