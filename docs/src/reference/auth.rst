.. _auth:
.. currentmodule:: tekore

Authorisation
=============
Web API authorisation.

.. autosummary::
   :nosignatures:

   Credentials
   AccessToken
   Token

   RefreshingCredentials
   RefreshingToken

   scope
   Scope

   parse_code_from_url
   prompt_for_user_token
   refresh_user_token
   request_client_token

Access tokens are used in authorisation by the Web API.
There are two methods of authorisation, called
client credentials flow and authorisation code flow.
They are used to retrieve application and user credentials, respectively.
The former can be used in generic endpoints like the ones for albums,
the latter is required for endpoints that involve a specific user.

.. code:: python

    import tekore as tk

    cred = tk.Credentials(client_id, client_secret, redirect_uri)

    # Client credentials flow
    app_token = cred.request_client_token()

    # Authorisation code flow
    url = cred.user_authorisation_url()
    code = ...  # Redirect user to login and retrieve code
    user_token = cred.request_user_token(code)

Tokens expire after an hour.
Their expiration status can be determined via
:attr:`Token.is_expiring <tekore.Token.is_expiring>`.
Client tokens can simply be retrieved again.
To avoid another authorisation when using user tokens, a refresh token
can be used to request a new access token with an equivalent scope.

.. code:: python

    # Specialised refresh
    app_token = cred.request_client_token()
    user_token = cred.refresh_user_token(user_token.refresh_token)

    # Type-agnostic refresh
    app_token = cred.refresh(app_token)
    user_token = cred.refresh(user_token)

Another way of dealing with token expiration is provided with
:class:`RefreshingCredentials`.
It is a drop-in replacement for :class:`Credentials`
but returns tokens that refresh themselves automatically.
Access tokens can also be retrieved without instantiating
:class:`Credentials` classes directly.
For that purpose, a number of `utility functions`_ are provided.

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
Scopes are used in user authorisation to retrieve tokens with additional privileges.
:class:`scope` is an enumeration of every possible such privilege.

.. code:: python

    import tekore as tk

    cred = (client_id, client_secret, redirect_uri)
    scope = tk.scope.user_read_email + tk.scope.user_read_private
    token = tk.prompt_for_user_token(*cred, scope)

.. autoclass:: scope
   :undoc-members:
.. autoclass:: Scope

Utility functions
-----------------
Utilities for retrieving access tokens.

.. note::

   These functions are intended for getting up and running quickly.
   Consider implementing a proper authentication procedure.
   See :ref:`auth-server` for more details.

.. code:: python

    import tekore as tk

    conf = tk.config_from_environment()

    # Request tokens
    app_token = tk.request_client_token(*conf[:2])
    user_token = tk.prompt_for_user_token(*conf)

    # Reload user token
    user_token = tk.refresh_user_token(*conf[:2], refresh_token)

.. autofunction:: prompt_for_user_token
.. autofunction:: parse_code_from_url
.. autofunction:: refresh_user_token
.. autofunction:: request_client_token
