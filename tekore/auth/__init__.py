"""
Web API authorisation.

Access tokens are used in authorisation by the Web API.
There are two methods of authorisation, called
client credentials flow and authorisation code flow.
They are used to retrieve application and user credentials, respectively.
The former can be used in generic endpoints like the ones for albums,
the latter is required for endpoints that involve a specific user.

.. code:: python

    from tekore.auth import Credentials

    cred = Credentials(client_id, client_secret, redirect_uri)

    # Client credentials flow
    app_token = cred.request_client_token()

    # Authorisation code flow
    url = cred.user_authorisation_url()
    code = ...  # Redirect user to login and retrieve code
    user_token = cred.request_user_token(code)

Tokens expire after an hour.
Their expiration status can be determined via
:attr:`Token.is_expiring <tekore.auth.expiring.Token.is_expiring>`.
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
:class:`RefreshingCredentials <tekore.auth.refreshing.RefreshingCredentials>`.
It is a drop-in replacement for
:class:`Credentials <tekore.auth.expiring.Credentials>`
but returns tokens that refresh themselves automatically.

Expiring credentials
--------------------
.. autoclass:: tekore.auth.expiring.Credentials
   :members:

.. autoclass:: tekore.auth.expiring.Token
   :members:

Refreshing credentials
----------------------
.. autoclass:: tekore.auth.refreshing.RefreshingCredentials
   :members:

.. autoclass:: tekore.auth.refreshing.RefreshingToken
   :members:
"""

from tekore.auth.expiring import Credentials
from tekore.auth.refreshing import RefreshingCredentials
