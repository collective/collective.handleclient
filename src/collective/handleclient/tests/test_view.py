# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.handleclient.testing \
  import COLLECTIVE_HANDLECLIENT_INTEGRATION_TESTING  # noqa

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles

import unittest2 as unittest
from mock import Mock


KEY = 'collective.handleclient.handle'


class TestView(unittest.TestCase):
    """Test the browser view calls of collective.handleclient"""

    layer = COLLECTIVE_HANDLECLIENT_INTEGRATION_TESTING

    def setUp(self):
        """
        Custom shared utility setup for tests.
        """
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Document', 'page', title=u'Page')
        client = self.portal.handle_client
        request = self.layer['request']
        initial_config = dict(baseurl='http://example.com',
                              username='123',
                              password='secret')
        request.form['config'] = initial_config
        client.manage_setConfiguration(request)
        uid = self.portal.page.UID()
        self.handle = '/'.join([client.prefix, uid])
        self.handle_url = client.baseurl + self.handle

    def test_hasHandle4unregistered(self):
        """
        Test traversal to check for handle of an unregistered object
        """
        view = self.portal.page.restrictedTraverse('hasHandle')
        has_handle = view.hasHandle()
        self.assertFalse(has_handle)
        handle = view.handle()
        self.assertEqual(handle, None)

    def test_registration(self):
        """
        Test handle registration and subsequent checks.
        """
        client = self.portal.handle_client

        response = Mock()
        response.status_code = 201
        response.headers = {"location": self.handle_url}
        client.session.post = Mock(return_value=response)

        view = self.portal.page.restrictedTraverse('hasHandle')

        self.assertEqual(view.create(), self.handle_url)
        self.assertTrue(view.hasHandle())
        self.assertEqual(view.handle(), self.handle)

        response.status_code = 204
        response.text = ''
        client.session.get = Mock(return_value=response)
        client.session.put = Mock(return_value=response)
        client.session.delete = Mock(return_value=response)

        self.assertEqual(view.read(), self.handle_url)
        self.assertEqual(view.update(), self.handle_url)

        self.assertTrue(view.hasDeletePermission())
        self.assertEqual(view.delete(), None)

    def test_redirect(self):
        """
        Test that the redirection flag is honored.
        """
        client = self.portal.handle_client
        page = self.portal.page

        response = Mock()
        response.status_code = 201
        response.headers = {"location": self.handle_url}
        client.session.post = Mock(return_value=response)

        view = self.portal.page.restrictedTraverse('hasHandle')
        url = page.absolute_url() + '/handle_view'
        self.assertEqual(view.create(redirect=True), url)

        response.status_code = 204
        response.text = ''
        client.session.delete = Mock(return_value=response)
        self.assertEqual(view.delete(redirect=True), url)
