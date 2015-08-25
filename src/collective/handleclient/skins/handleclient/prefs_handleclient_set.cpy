## Controller Python Script "prefs_handleclient_set"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=RESPONSE=None
##title=
##

request=context.REQUEST

portal = context.portal_url.getPortalObject()
handle_client = context.handle_client

request.set('title', 'Handle Client Configuration')

handle_client.manage_setConfiguration(request)

return state.set(status='success', portal_status_message='Handle client configuration updated.')
