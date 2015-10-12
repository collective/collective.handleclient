# -*- coding: utf-8 -*-

from zope.annotation import IAnnotations
from AccessControl import getSecurityManager
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName


KEY = 'collective.handleclient.handle'  # this should be in config


class HandleView(BrowserView):
    """View methods to deal with handle pids"""

    @property
    def client(self):
        return getToolByName(self.context, 'handle_client')

    def hasHandle(self):
        """
        Returns True if the context is registered.
        False otherwise
        """
        if self.handle() is None:
            return False
        return True

    def handle(self):
        """
        Looks up the handle in the context's annotation.
        Returns None if not found.
        """
        annotations = IAnnotations(self.context)
        return annotations.get(KEY, None)

    def create(self, redirect=False):
        """
        Register the object's UID as PID in the handle system
        Returns the registered location on success
        Raises HandleError on failure
        """
        location = self.client.create(self.context)
        if not redirect:
            return location
        baseurl = self.context.absolute_url()
        return self.request.response.redirect(baseurl + "/handle_view")

    def read(self):
        """
        Gets the current registration from the server
        Returns the registered location on success
        Raises HandleError on failure
        """
        return self.client.read(self.context)

    def update(self):
        """
        Updates the existing registration with the current
        target URL.
        Returns the registered location on success.
        Raises HandleError on failure
        """
        return self.client.update(self.context)

    def delete(self, redirect=False):
        """
        Deletes the existing registration
        Returns None on success.
        Raises HandleError on failure
        """
        result = self.client.delete(self.context)
        if not redirect:
            return result
        baseurl = self.context.absolute_url()
        return self.request.response.redirect(baseurl + "/handle_view")

    def hasDeletePermission(self):
        """
        Helper method to determine whether the current user
        is allowed to unregister a handle.
        """
        sm = getSecurityManager()
        return sm.checkPermission("Handle Client: Delete Handle",
                                  self.context)

    def creationUrl(self):
        """
        Helper method returning the appropriate URL for handle creation
        """
        baseurl = self.context.absolute_url()
        return baseurl + '/createHandle?redirect=True'

    def deletionUrl(self):
        """
        Helper method returning the appropriate URL for handle deletion
        """
        baseurl = self.context.absolute_url()
        return baseurl + '/deleteHandle?redirect=True'
