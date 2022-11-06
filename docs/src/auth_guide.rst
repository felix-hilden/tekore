.. _auth-guide:
.. currentmodule:: tekore

Authorisation guide
===================
Introduction
------------
Spotify uses access tokens to authorise requests to the Web API.
They are strings of characters and ordinarily expire in an hour.
There are two levels of authorisation: client and user authorisation,
which yield different types of tokens
and grant access to different parts of the API.
Client tokens, also referred to as *application* tokens can be used to access
generic endpoints, like retrieving albums or tracks.
User tokens are required for endpoints that involve a specific user,
like accessing saved tracks or manipulating playback,
but they also grant access to generic endpoints.

The appropriate authorisation method for an application
depends on the intended number of users.
Simple scripts can be created relatively easily.
Running a web server requires more effort,
but it allows an application to serve any number of users.
For examples of authorisation with application and user tokens
in both server and scripting contexts, see the following:

- :ref:`async-server` - server using application tokens
- :ref:`auth-server` - server using user tokens
- :ref:`creating-scripts`

See :ref:`auth` for reference documentation and
Spotify's `authorisation guide <https://developer.spotify.com/
documentation/general/guides/authorization-guide/>`_
for more information about the underlying authentication procedures.

User authorisation
------------------
User authorisation involves a two-step process.

- A user opens or is redirected to a specific URL in their browser
  and logs in to Spotify to authorise the application.
  Then the user is redirected to a set redirect URI
  with the address containing a code.
- An access token is requested with the code from the redirection result.

This redirection and extraction of data is carried out with a web server.
See this recipe on an :ref:`auth-server` for an example implementation.
Spinning up a server can be replaced with some manual work,
e.g. the user pasting information to a terminal.
For example :func:`prompt_for_user_token` uses this manual way,
but this also makes it unusable on a server.

Refreshing and saving tokens
----------------------------
Access tokens expire after an hour.
Their expiration status can be determined via
:attr:`Token.is_expiring <tekore.Token.is_expiring>`.
How another valid token is obtained depends on the type of the token.
Application tokens can simply be requested again.
To avoid another authorisation when using user tokens,
a :attr:`refresh_token <tekore.Token.refresh_token>`
can be used to request new access tokens.

A refresh token is enough to request new user access tokens,
making them a perfect candidate to save to a file or a database.
It is valid until the user manually revokes it from Spotify.
A new refresh token may also be returned when requesting a new access token.

In practice receiving new refresh tokens seems to be rare,
but it is a possibility as laid out in the
`OAuth 2 specification <https://tools.ietf.org/html/rfc6749#section-6>`_.
The spec states that if it does happen the old refresh token may be revoked,
so the new recent token should be used instead.
The most recent refresh token is always returned when refreshing a token,
but any saved refresh tokens need to be updated too.

A means of saving and loading refresh tokens is provided in :ref:`config`.

Token scopes
------------
The scope of a user token represents its access rights to various endpoints.
By default, tokens cannot be used, for example, to modify a user's library.
Scopes are set during user authorisation,
and requesting additional scopes requires another authorisation.

However, the scope of a token can be gradually expanded
across a number of authorisations.
When authorising, the scope of the resulting token is determined
by the scopes that were set at the start of authorisation.
But when refreshing a token, the scope is expanded to cover all scopes
that the user has granted a particular application in previous authorisations.
This holds for refresh tokens of both new and previously generated tokens.

PKCE user authorisation
-----------------------
User authorisation can be performed using Proof Key for Code Exchange,
an extension to ordinary user authorisation.
It is intended for public clients,
i.e. applications whose client secret might be exposed.
As such, retrieving user tokens with it does not require a client secret.

However, PKCE introduces some restrictions to refreshing user tokens.
The refresh token of a PKCE-authorised token can only be used
to spawn the next token, after which it is invalidated,
which means that if saved, the refresh token needs to be constantly updated
to match the newest available refresh token.
Still, all access tokens are valid for their full duration.

Security concerns
-----------------
There are two main security concerns with authorisation,
besides the obvious leaking of access tokens.

Using a state with user authorisation prevents cross-site request forgery
(`RFC 6749 <https://tools.ietf.org/html/rfc6749#section-10.12>`_).
A string can be sent as state on authorisation.
When a user is redirected back,
the same state should be returned as a query parameter.
:func:`gen_state` is provided to generate random strings to send as state.
:func:`parse_state_from_url` can then be used to extract the returned state.
State is generated and checked automatically when using :class:`UserAuth`.

A client secret might not always be safe
and the redirect URI handler might be vulnerable
(`RFC 7636 <https://tools.ietf.org/html/rfc7636>`_).
The PKCE extension to user authorisation allows
retrieving user tokens without a client secret,
and provides an added layer of security with code challenges and verifiers.
Challenges and verifiers are handled automatically when using
:class:`UserAuth` with PKCE enabled.
Here's a summary of the configuration requirements
for each authorisation method.

+-------------------------+-----------+---------------+--------------+
| Method                  | Client ID | Client secret | Redirect URI |
+=========================+===========+===============+==============+
| Client authorisation    | x         | x             |              |
+-------------------------+-----------+---------------+--------------+
| User authorisation      | x         | x             | x            |
+-------------------------+-----------+---------------+--------------+
| User token refresh      | x         | x             |              |
+-------------------------+-----------+---------------+--------------+
| PKCE user authorisation | x         |               | x            |
+-------------------------+-----------+---------------+--------------+
| PKCE token refresh      | x         |               |              |
+-------------------------+-----------+---------------+--------------+

Summary of authorisation methods
--------------------------------
Authorisation methods are provided on three levels
for both application and user access tokens.
At the lowest level :class:`Credentials` provides ordinary access tokens.
:class:`RefreshingCredentials` has similar functionality,
but returns self-refreshing tokens.
Finally, utility functions that wrap around :class:`RefreshingCredentials`
are provided for easy one-time authorisation.

A summary of all authorisation methods can be found below.
See each method's documentation in :ref:`auth` for more details.
References to classes :class:`Credentials` and :class:`RefreshingCredentials`
are abbreviated as :class:`C` and :class:`RC` for brevity.

- **Creation**: is the method for generating new tokens or refreshing them
- **Type**: is the resulting token expiring or automatically refreshing

.. |exp-app-new| replace::
   :meth:`C.request_client_token <Credentials.request_client_token>`
.. |exp-usr-new| replace::
   :meth:`C.request_user_token <Credentials.request_user_token>`
.. |exp-usr-ref| replace::
   :meth:`C.refresh_user_token <Credentials.refresh_user_token>`
.. |exp-pkc-new| replace::
   :meth:`C.request_pkce_token <Credentials.request_pkce_token>`
.. |exp-pkc-ref| replace::
   :meth:`C.refresh_pkce_token <Credentials.refresh_pkce_token>`
.. |exp-a-u-ref| replace::
   :meth:`C.refresh <Credentials.refresh>`
.. |ref-app-new| replace::
   :meth:`RC.request_client_token <RefreshingCredentials.request_client_token>`
.. |ref-usr-new| replace::
   :meth:`RC.request_user_token <RefreshingCredentials.request_user_token>`
.. |ref-usr-ref| replace::
   :meth:`RC.refresh_user_token <RefreshingCredentials.refresh_user_token>`
.. |ref-pkc-new| replace::
   :meth:`RC.request_pkce_token <Credentials.request_pkce_token>`
.. |ref-pkc-ref| replace::
   :meth:`RC.refresh_pkce_token <Credentials.refresh_pkce_token>`
.. |utl-app-new| replace:: :func:`request_client_token`
.. |utl-usr-new| replace:: :func:`prompt_for_user_token`
.. |utl-usr-ref| replace:: :func:`refresh_user_token`
.. |utl-pkc-new| replace:: :func:`prompt_for_pkce_token`
.. |utl-pkc-ref| replace:: :func:`refresh_pkce_token`

**Application tokens**

+----------+------------+-------+---------------+
| Creation | Type       | Notes | Method        |
+==========+============+=======+===============+
| New      | Expiring   |       | |exp-app-new| |
+----------+------------+-------+---------------+
| Refresh  | Expiring   | 1     | |exp-a-u-ref| |
+----------+------------+-------+---------------+
| New      | Refreshing |       | |ref-app-new| |
+----------+------------+-------+---------------+
| New      | Refreshing | 2     | |utl-app-new| |
+----------+------------+-------+---------------+

**User tokens**

There are two variants of each user authorisation method.
One uses ordinary OAuth 2 authorisation, the other uses the PKCE extension.

+----------+------------+-------+---------------+---------------+
| Creation | Type       | Notes | Ordinary      | PKCE variant  |
+==========+============+=======+===============+===============+
| New      | Expiring   | 3     | |exp-usr-new| | |exp-pkc-new| |
+----------+------------+-------+---------------+---------------+
| Refresh  | Expiring   |       | |exp-usr-ref| | |exp-pkc-new| |
+----------+------------+-------+---------------+---------------+
| Refresh  | Expiring   | 1     | |exp-a-u-ref| | |exp-a-u-ref| |
+----------+------------+-------+---------------+---------------+
| New      | Refreshing | 3     | |ref-usr-new| | |ref-pkc-new| |
+----------+------------+-------+---------------+---------------+
| Refresh  | Refreshing |       | |ref-usr-ref| | |ref-pkc-ref| |
+----------+------------+-------+---------------+---------------+
| New      | Refreshing | 2, 4  | |utl-usr-new| | |utl-pkc-new| |
+----------+------------+-------+---------------+---------------+
| Refresh  | Refreshing | 2     | |utl-usr-ref| | |utl-pkc-ref| |
+----------+------------+-------+---------------+---------------+

:class:`UserAuth` can be used to simplify the implementation of user
authorisation with either one of the credentials clients, with or without PKCE.

**Notes**

1. This is a subject-agnostic refresh,
   fit for both app and user tokens with or without PKCE.
   For application tokens, a new token is returned.
2. These functions wrap around :class:`RefreshingCredentials` internally
   to provide a shorthand for one-off authorisation.
3. These methods are paired with the first step of user authorisation:
   redirecting the user to a URL to login with Spotify.
4. Requires manually pasting text to a terminal, is not usable on a server.

Authorising requests
--------------------
The :ref:`client <client>` provides two ways of authorising requests.
Firstly an access token is accepted in the client's constructor.

.. code:: python

   import tekore as tk

   s = tk.Spotify(token)
   a = s.artist(artist_id)

Secondly, the client can temporarily use another token for requests.
This is particularly handy if only one client instance is created but there are
many users, or if tokens are manually refreshed.

.. code:: python

   s = tk.Spotify(app_token)
   a = s.artist(artist_id)

   with s.token_as(user_token):
       user = s.current_user()
