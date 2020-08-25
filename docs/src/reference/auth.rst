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
   UserAuth
   gen_state
   parse_code_from_url
   parse_state_from_url

Access tokens are used in authorisation by the Web API.
There are two methods of authorisation, called
client credentials flow and authorisation code flow.
They are used to retrieve application and user credentials, respectively.
The former can be used in generic endpoints like the ones for albums,
the latter is required for endpoints that involve a specific user.
User authorisation involves a two-step process.

- Redirect a user to a specific URL
- Request an access token with data from the redirection

See Spotify's `authorisation guide <https://developer.spotify.com/
documentation/general/guides/authorization-guide/>`_
for more information about the underlying authentication procedures.

.. code:: python

    import tekore as tk

    cred = tk.Credentials(client_id, client_secret, redirect_uri)

    # Client credentials flow
    app_token = cred.request_client_token()

    # Authorisation code flow
    url = cred.user_authorisation_url()
    code = ...  # Redirect user to login and retrieve code
    user_token = cred.request_user_token(code)

This redirection and extraction of data is carried out with a web server.
See this recipe on an :ref:`auth-server` for an example implementation.
Spinning up a server can be replaced with some manual work,
e.g. the user pasting information to a terminal.
For example :func:`prompt_for_user_token` uses this manual way,
but this also makes it unusable on a server.

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
:class:`RefreshingCredentials` directly.
For that purpose, a number of `utilities`_ are provided.
They also include other useful constructs related to authorisation.

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
   UserAuth
   gen_state
   parse_code_from_url
   parse_state_from_url

.. autofunction:: request_client_token
.. autofunction:: prompt_for_user_token
.. autofunction:: refresh_user_token
.. autoclass:: UserAuth
.. autofunction:: gen_state
.. autofunction:: parse_code_from_url
.. autofunction:: parse_state_from_url
