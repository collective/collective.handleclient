# -*- coding: utf-8 -*-
"""Init and utils."""

from zope.i18nmessageid import MessageFactory

_ = MessageFactory('collective.handleclient')

from Products.CMFCore import utils 
from Products.CMFCore.permissions import setDefaultRoles

import handle_client

setDefaultRoles('Handle Client: Delete Handle', ('Manager',))

# group the tool
tools = ( handle_client.HandleClient,
          )


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    utils.ToolInit(
        'Handle Client', tools=tools,
        icon='tool.gif',
        ).initialize(context)
