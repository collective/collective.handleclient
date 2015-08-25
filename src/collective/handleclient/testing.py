# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.handleclient


class CollectiveHandleclientLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=collective.handleclient)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.handleclient:default')


COLLECTIVE_HANDLECLIENT_FIXTURE = CollectiveHandleclientLayer()


COLLECTIVE_HANDLECLIENT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_HANDLECLIENT_FIXTURE,),
    name='CollectiveHandleclientLayer:IntegrationTesting'
)


COLLECTIVE_HANDLECLIENT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_HANDLECLIENT_FIXTURE,),
    name='CollectiveHandleclientLayer:FunctionalTesting'
)


COLLECTIVE_HANDLECLIENT_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_HANDLECLIENT_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CollectiveHandleclientLayer:AcceptanceTesting'
)
