"""Two sites in one Zope for tests/test_theme_parity.py: Clara's and a plain one.

Imports plone.blicca.auroraeditor, which Clara does not depend on: importing
this module skips the importer when the editor is not installed.
"""

import pytest
from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import SITE_OWNER_NAME
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from plone.testing import zope
from Products.CMFPlone.factory import addPloneSite
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.component.hooks import setSite

from plonetheme.clara.testing import FIXTURE


auroraeditor = pytest.importorskip("plone.blicca.auroraeditor")
volto = pytest.importorskip("plone.volto")

PLAIN_SITE_ID = "plain"
EDITOR_PROFILES = (
    "plone.restapi:default",
    "plone.blicca.auroraeditor:default",
    "plone.blicca.auroraeditor:article",
)


def add_plain_site(app):
    """A site built like PLONE_FIXTURE builds Clara's, minus Clara."""
    manager = getSecurityManager()
    zope.login(app["acl_users"], SITE_OWNER_NAME)
    try:
        site = addPloneSite(app, PLAIN_SITE_ID, extension_ids=PLONE_FIXTURE.extensionProfiles)
        site.portal_workflow.setDefaultChain("")
        # Barceloneta's navigation portlet would narrow the content column
        # below the `default` token and leave those blocks uncompared.
        for name in ("plone.leftcolumn", "plone.rightcolumn"):
            column = getUtility(IPortletManager, name=name)
            assignments = getMultiAdapter((site, column), IPortletAssignmentMapping)
            for key in list(assignments):
                del assignments[key]
    finally:
        setSecurityManager(manager)
        setSite(None)


def install_editor(site):
    setSite(site)
    for profile in EDITOR_PROFILES:
        applyProfile(site, profile)


class ThemeParityLayer(PloneSandboxLayer):
    """Clara's site plus a plain Barceloneta one, both with the editor's Article."""

    defaultBases = (FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # The plain site first: the editor's install diagnostics would run on
        # every profile of a half-built site and log errors.
        add_plain_site(app)
        # Article's volto.* behaviors are registered by plone.volto's ZCML
        self.loadZCML(package=volto)
        self.loadZCML(package=auroraeditor)

    def setUpPloneSite(self, portal):
        install_editor(portal.getPhysicalRoot()[PLAIN_SITE_ID])
        install_editor(portal)  # last, so the site hook ends on Clara's site


THEME_PARITY_FIXTURE = ThemeParityLayer()

THEME_PARITY_TESTING = FunctionalTesting(
    bases=(THEME_PARITY_FIXTURE, zope.WSGI_SERVER_FIXTURE),
    name="PlonethemeClaraLayer:ThemeParityTesting",
)
