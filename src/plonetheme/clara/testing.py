"""Testing setup for plonetheme.clara."""
import os

import plone.app.theming
import plone.pageletlayout
import plone.restapi
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.testing.zope import WSGI_SERVER_FIXTURE

import plonetheme.clara


class PlonethemeClaraLayer(PloneSandboxLayer):
    """Custom testing layer for plonetheme.clara."""

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        # Compile .po -> .mo so add-on translations load during tests.
        os.environ.setdefault("zope_i18n_compile_mo_files", "true")
        self.loadZCML(package=plone.app.theming)
        self.loadZCML(package=plone.restapi)
        # Clara depends on plone.pageletlayout (its integration base); load the
        # base ZCML so profile-plone.pageletlayout:default is registered and
        # Clara's dependency-profile install resolves it (wayfinder ticket 04).
        self.loadZCML(package=plone.pageletlayout)
        self.loadZCML(package=plonetheme.clara)

    def setUpPloneSite(self, portal):
        """Set up Plone site."""
        self.applyProfile(portal, "plonetheme.clara:default")


FIXTURE = PlonethemeClaraLayer()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name="PlonethemeClaraLayer:IntegrationTesting",
)

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name="PlonethemeClaraLayer:FunctionalTesting",
)

ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(FIXTURE, WSGI_SERVER_FIXTURE),
    name="PlonethemeClaraLayer:AcceptanceTesting",
)


# Test credentials
TEST_USER_ID = "testuser"
TEST_USER_NAME = "testuser"
SITE_OWNER_NAME = SITE_OWNER_NAME
SITE_OWNER_PASSWORD = SITE_OWNER_PASSWORD
