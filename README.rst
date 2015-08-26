==============================================================================
collective.handleclient
==============================================================================

Plone add-on to interact with a Handle-based Persistent
Identifier (PID) service. Driving use case is the internal
coordination portal of the EUDAT project. The client has been
developed against version 2 of the European PID Consortium's
(EPIC) API. While it may also work with other PID providers
such as DataCite/DOI this has not been tested yet.

Features
--------

- A configurable tool where site administrators define the base URL
  for the handle service to use including the prefix and credentials.

- Plone's internal UIDs are used as suffix together with the
  configured prefix to construct the handle.

- An 'object' action is added through which a PID registration
  can be triggered and checked for individual content items.

- Per default, only 'Managers' - but not 'Site Administrators' - can 
  unregister a PID. 


Examples
--------

This add-on can not yet be seen in action at a public site.


Documentation
-------------

Full documentation for end users will become available as the
package matures.


Translations
------------

This product has not yet been translated into other languages.


Installation
------------

Once there is a release available on PyPI you can
install collective.handleclient by adding it to your buildout::

   [buildout]

    ...

    eggs =
        collective.handleclient


and then running "bin/buildout"

Until then you need to clone the repository and add it
to the development section in your buildout config as well.


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.handleclient/issues
- Source Code: https://github.com/collective/collective.handleclient


Support
-------

If you are having issues, please contact the author.


License
-------

The project is licensed under the GPLv2.
