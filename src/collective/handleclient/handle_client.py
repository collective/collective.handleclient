# -*- coding: utf-8 -*-
"""HandleClient's main class"""

import os
import logging
import requests

# Zope stuff
from zope.annotation import IAnnotations
from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from OFS.SimpleItem import SimpleItem

# CMF stuff
from Products.CMFCore.permissions import ManagePortal
from Products.CMFCore.utils import UniqueObject

KEY = 'collective.handleclient.handle'


class HandleClient(UniqueObject, SimpleItem):
    """
    Tool for managing handle pids.
    """

    id = 'handle_client'
    meta_type = 'Handle Client'
    # class defaults
    baseurl = ''
    username = ''
    prefix = ''
    password = ''

    security = ClassSecurityInfo()

    def create(self, context):
        """
        Request a handle to be created for the content object
        passed in as context. The handle will be the configured prefix
        plus the objects uid. The absolut url is supplied as target url.
        On success the handle will be stored in the context's annotations.
        """
        uid = context.UID()
        target = context.absolute_url()
        handle = '/'.join([self.prefix, uid])
        data = [{'type': 'URL', 'parsed_data': target}]

        resp = self.session.post(
            self.baseurl + handle, json=data
            )
        if int(resp.status_code) == 405:  # EPIC doesn't support POST
            resp = self.session.put(
                self.baseurl + handle, json=data
                )
        if int(resp.status_code) == 201:
            location = resp.headers.get('location')
            annotations = IAnnotations(context)
            annotations[KEY] = handle
            return location
        else:
            logger = logging.getLogger('collective.handle')
            message = self.baseurl + handle
            message += '\n' + resp + '\n'
            for k, v in resp.headers.items():
                message += "%s = %s\n" % (k, v)
            logger.error(message)
            raise HandleError(resp.status_code)

    def read(self, context):
        """
        Returns the 'location' if context is registered, None otherwise.
        Raises HandleError if the call fails.
        """
        handle = self._getHandle(context)
        if handle is None:
            return None
        resp = self.session.get(self.baseurl + handle)
        if resp.status_code in [200, 204]:
            return resp.headers.get("location", "") + resp.text
        raise HandleError(resp.status_code)

    def update(self, context):
        """
        Change the target URL that the handle resolves to.
        Returns None if context is not registered.
        Raises HandleError if the call fails.

        Should be called when context was moved or renamed
        (aka whenever its URL changed).
        """
        handle = self._getHandle(context)
        if handle is None:
            return None
        target = context.absolute_url()
        data = [{'type': 'URL', 'parsed_data': target}]
        resp = self.session.put(
            self.baseurl + handle, json=data
            )
        if int(resp.status_code) == 204:
            return resp.headers.get("location")
        raise HandleError(resp.status_code)

    def delete(self, context):
        """
        Unregister the handle and remove it from the annotation.
        Returns None if context is not registered.
        Raises HandleError if the call fails.
        """
        handle = self._getHandle(context)
        if handle is None:
            return None
        resp = self.session.delete(self.baseurl + handle)
        if int(resp.status_code) != 204:
            raise HandleError(resp.status_code)
        self._removeHandle(context)

    def _getHandle(self, context):
        """
        Helper method looking up the handle in the context's annotation.
        Returns None if not existing.
        """
        annotations = IAnnotations(context)
        return annotations.get(KEY, None)

    def _removeHandle(self, context):
        annotations = IAnnotations(context)
        del annotations[KEY]

    # for the tool configuration

    security.declareProtected(ManagePortal, 'getConfiguration')
    def getConfiguration(self):
        """returns the config (without password) for the configlet"""

        config = {'baseurl': self.baseurl,
                  'username': self.username,
                  'prefix': self.prefix,
                  }
        return config

    security.declareProtected(ManagePortal, 'manage_setConfiguration')
    def manage_setConfiguration(self, request):
        """setting the configuration from data recieved through a form"""
        data = request.form.copy()
        config = data.get('config', None)
        if config is not None:
            self._setConfiguration(config)

    def _setConfiguration(self, config):
        """Update configuration settings from form data"""

        baseurl = config.get('baseurl')
        # make sure the URL ends with exactly one slash
        self.baseurl = baseurl.rstrip('/') + '/'

        username = config.get('username', None)
        prefix = config.get('prefix', None)
        # only one needs to be given as username and prefix are
        # usually the same in the handle system
        self.username = username or prefix
        self.prefix = prefix or username

        self.password = config.get('password')
        self._updateSession()

    def _updateSession(self, verify_ssl=False):
        self.session = requests.Session()
        if not self.password:
            password = os.environ['HANDLE_PASSWORD']
        else:
            password = self.password
        self.session.auth = (self.username, password)
        self.session.verify = verify_ssl
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'User-Agent': 'collective.handleclient',
            })


InitializeClass(HandleClient)


class HandleError(Exception):

    def __init__(self, status):

        messages = {
            400: "400 Bad request.",
            401: "401 Authentication failed.",
            403: "403 You don't have the right to do that.",
            404: "404 Handle not found.",
            405: "405 Method Not Allowed.",
            409: "409 Handle already exists.",
            415: "415 Unsupported Media Type",
            'default': "Handle Server error. ",
            }

        status = int(status)
        message = messages.get(status, None)
        self.message = message or messages.get('default') + str(status)

    def __unicode__(self):
        return unicode(self.message)

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.__str__()
