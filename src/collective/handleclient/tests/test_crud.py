# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.handleclient.testing \
  import COLLECTIVE_HANDLECLIENT_INTEGRATION_TESTING  # noqa
from zope.annotation import IAnnotations

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles

import unittest2 as unittest
from mock import Mock

from collective.handleclient.handle_client import HandleError

KEY = 'collective.handleclient.handle'


class TestCRUD(unittest.TestCase):
    """Test the CRUD calls of collective.handleclient"""

    layer = COLLECTIVE_HANDLECLIENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
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

    def test_create(self):
        """Test creation of a handle"""
        client = self.portal.handle_client
        page = self.portal.page

        response = Mock()
        response.status_code = 201
        response.headers = {"location": self.handle_url}

        client.session.post = Mock(return_value=response)
        hdl = client.create(page)

        self.assertEqual(hdl, self.handle_url)

    def test_epic_create(self):
        """Test EPIC's creation of a handle - they require a 'put'"""
        client = self.portal.handle_client
        page = self.portal.page

        response1 = Mock()
        response1.status_code = 405
        response2 = Mock()
        response2.status_code = 201
        response2.headers = {"location": self.handle_url}

        client.session.post = Mock(return_value=response1)
        client.session.put = Mock(return_value=response2)
        hdl = client.create(page)

        self.assertEqual(hdl, self.handle_url)

    def test_failed_create(self):
        """Test that a failed create request raises HandleError"""
        client = self.portal.handle_client
        page = self.portal.page

        response = Mock()
        response.status_code = 403
        response.headers = {"location": self.handle_url}

        client.session.post = Mock(return_value=response)
        message = "403 You don't have the right to do that."
        with self.assertRaisesRegexp(HandleError, message):
            client.create(page)

    def test_read_unregistered(self):
        """Test reading the registration of an unregistered object"""
        client = self.portal.handle_client
        page = self.portal.page

        response = Mock()
        response.status_code = 204
        response.headers = {"location": self.handle_url}

        client.session.get = Mock(return_value=response)
        hdl = client.read(page)

        self.assertEqual(hdl, None)

    def test_read_registered(self):
        """Test reading the registration of a registered object"""
        client = self.portal.handle_client
        page = self.portal.page

        # fake the registration
        annotations = IAnnotations(page)
        annotations[KEY] = self.handle

        response = Mock()
        response.status_code = 204
        response.headers = {"location": self.handle_url}
        response.text = ''

        client.session.get = Mock(return_value=response)
        hdl = client.read(page)

        self.assertEqual(hdl, self.handle_url)

    def test_not_found(self):
        """Test read resulting in 'not found' raises HandleError"""
        client = self.portal.handle_client
        page = self.portal.page

        # fake the registration
        annotations = IAnnotations(page)
        annotations[KEY] = self.handle

        response = Mock()
        response.status_code = 404
        client.session.get = Mock(return_value=response)

        with self.assertRaisesRegexp(HandleError, "404 Handle not found."):
            client.read(page)

    def test_update_unregistered(self):
        """
        Test updating the registration of an unregistered object
        returns None
        """
        client = self.portal.handle_client
        page = self.portal.page

        response = Mock()
        response.status_code = 204
        response.headers = {"location": self.handle_url}

        client.session.put = Mock(return_value=response)
        hdl = client.update(page)

        self.assertEqual(hdl, None)

    def test_update_registered(self):
        """Test updating the registration of a registered object"""
        client = self.portal.handle_client
        page = self.portal.page

        # fake the registration
        annotations = IAnnotations(page)
        annotations[KEY] = self.handle

        response = Mock()
        response.status_code = 204
        response.headers = {"location": self.handle_url}
        response.text = ''

        client.session.put = Mock(return_value=response)
        hdl = client.update(page)

        self.assertEqual(hdl, self.handle_url)

    def test_delete(self):
        """Test unregistering a registered object"""
        client = self.portal.handle_client
        page = self.portal.page

        # fake the registration
        annotations = IAnnotations(page)
        annotations[KEY] = self.handle

        response = Mock()
        response.status_code = 204

        client.session.delete = Mock(return_value=response)
        client.delete(page)

        self.assertTrue(KEY not in annotations)
