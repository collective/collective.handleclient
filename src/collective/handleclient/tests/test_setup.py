# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.handleclient.testing import COLLECTIVE_HANDLECLIENT_INTEGRATION_TESTING  # noqa
from plone import api

import unittest2 as unittest


class TestSetup(unittest.TestCase):
    """Test that collective.handleclient is properly installed."""

    layer = COLLECTIVE_HANDLECLIENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.handleclient is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('collective.handleclient'))

    def test_browserlayer(self):
        """Test that ICollectiveHandleclientLayer is registered."""
        from collective.handleclient.interfaces import ICollectiveHandleclientLayer
        from plone.browserlayer import utils
        self.assertIn(ICollectiveHandleclientLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_HANDLECLIENT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['collective.handleclient'])

    def test_product_uninstalled(self):
        """Test if collective.handleclient is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled('collective.handleclient'))
