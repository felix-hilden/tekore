.. _auth:
.. currentmodule:: tekore

Authorisation
=============
Web API authorisation.

.. autosummary::
   :nosignatures:

   Credentials
   Token
   RefreshingCredentials
   RefreshingToken
   AccessToken
   scope
   Scope

   request_client_token
   prompt_for_user_token
   refresh_user_token
   prompt_for_pkce_token
   refresh_pkce_token
   UserAuth
   gen_state
   parse_code_from_url
   parse_state_from_url

See also: :ref:`auth-guide`.

Expiring credentials
--------------------
.. autoclass:: Credentials
.. autoclass:: Token
.. autoclass:: AccessToken

Refreshing credentials
----------------------
.. autoclass:: RefreshingCredentials
   :no-show-inheritance:
.. autoclass:: RefreshingToken

.. _auth-scopes:

Scopes
------
Scopes are used in user authorisation
to retrieve tokens with additional privileges.
:class:`scope` is an enumeration of every possible such privilege.

.. code:: python

    import tekore as tk

    cred = (client_id, client_secret, redirect_uri)
    scope = tk.scope.user_read_email + tk.scope.user_read_private
    token = tk.prompt_for_user_token(*cred, scope)

See Spotify's `Authorization scopes
<https://developer.spotify.com/documentation/general/guides/scopes/>`_
guide for scope descriptions.
Scopes that are required or optional are listed
in each endpoint's documentation, see :ref:`client`.
They can also be determined programmatically.

.. autoclass:: scope
   :special-members:
   :undoc-members:
   :exclude-members: __module__
.. autoclass:: Scope
   :special-members:

Utilities
---------
Authorisation utilities.

.. note::

   These utilities are meant to get users up and running quickly.
   Consider implementing authorisation procedures
   that suit your needs specifically.
   See :ref:`auth-server` for more details.

.. autosummary::
   :nosignatures:

   request_client_token
   prompt_for_user_token
   refresh_user_token
   prompt_for_pkce_token
   refresh_pkce_token
   UserAuth
   gen_state
   parse_code_from_url
   parse_state_from_url

.. autofunction:: request_client_token
.. autofunction:: prompt_for_user_token
.. autofunction:: refresh_user_token
.. autofunction:: prompt_for_pkce_token
.. autofunction:: refresh_pkce_token
.. autoclass:: UserAuth
.. autofunction:: gen_state
.. autofunction:: parse_code_from_url
.. autofunction:: parse_state_from_url
