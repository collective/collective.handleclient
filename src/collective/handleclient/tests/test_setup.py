# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.handleclient.testing \
  import COLLECTIVE_HANDLECLIENT_INTEGRATION_TESTING  # noqa
from plone import api

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles

import unittest2 as unittest


class TestSetup(unittest.TestCase):
    """Test that collective.handleclient is properly installed."""

    layer = COLLECTIVE_HANDLECLIENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """
        Test if collective.handleclient is installed
        with portal_quickinstaller.
        """
        product = 'collective.handleclient'
        self.assertTrue(self.installer.isProductInstalled(product))

    def test_browserlayer(self):
        """Test that ICollectiveHandleclientLayer is registered."""
        from collective.handleclient.interfaces \
          import ICollectiveHandleclientLayer
        from plone.browserlayer import utils
        self.assertIn(ICollectiveHandleclientLayer,
                      utils.registered_layers())

    def test_configuration(self):
        """Test that the handle_client can be configured"""
        client = self.portal.handle_client
        request = self.layer['request']
        initial_config = dict(baseurl='http://example.com',
                              username='123',
                              password='secret')
        request.form['config'] = initial_config
        client.manage_setConfiguration(request)
        config = client.getConfiguration()
        self.assertEqual(config['baseurl'], 'http://example.com/')
        self.assertEqual(config['username'], '123')
        self.assertEqual(config['prefix'], '123')
        self.assertFalse('password' in config.keys())
        self.assertEqual(client.session.headers['Cache-Control'], 'no-cache')


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_HANDLECLIENT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.installer.uninstallProducts(['collective.handleclient'])

    def test_product_uninstalled(self):
        """Test if collective.handleclient is cleanly uninstalled."""
        product = 'collective.handleclient'
        self.assertFalse(self.installer.isProductInstalled(product))
