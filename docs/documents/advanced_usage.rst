.. _advanced-usage:

Advanced usage
==============
Working with access tokens
--------------------------
Retrieving user tokens
**********************
:func:`prompt_for_user_token <spotipy.util.credentials.prompt_for_user_token>`
provides a convenient way of retrieving
an access token that refreshes automatically when about to expire.
However, it is intended for local use as it opens up a browser window.
For situations involving a server, a two-step process should be implemented.

- Redirect a user to a specific URL
- Receive an access token as a result of the authentication

The steps are covered by two methods of the
:class:`Credentials <spotipy.auth.Credentials>` class.
See this recipe on an :ref:`auth-server` for an example implementation.
The same process can be implemented using
:class:`RefreshingCredentials <spotipy.auth.refreshing.RefreshingCredentials>`.

Providing tokens
****************
The :mod:`client <spotipy.client>` provides two ways of authenticating requests.
Firstly an access token is accepted in the client's constructor.

.. code:: python

   s = Spotify(token)
   a = s.artist(artist_id)

Secondly, the client can temporarily use another token for requests.
This is particularly handy if only one client instance is created but there are
many users, several tokens are associated with a single user perhaps due to
different scopes, or tokens are manually refreshed.

.. code:: python

   s = Spotify(app_token)
   a = s.artist(artist_id)

   with s.token_as(user_token):
       user = s.current_user()

Token persistence
*****************
A refresh token is enough to request new user access tokens,
making them a perfect candidate to save to a file or a database.
Whether you are using :mod:`auth <spotipy.auth>` or
:mod:`util <spotipy.util.credentials>`,
the refresh tokens can later be used to retrieve user access tokens.

A refresh token is valid until the user manually revokes it from Spotify.
A new refresh token may also be returned when requesting a new access token.
In practice receiving new refresh tokens seems to be rare,
but it is a possibility as laid out in the OAuth 2
`specification <https://tools.ietf.org/html/rfc6749#section-6>`_.
The spec states that if it does happen the old refresh token may be revoked,
so the new recent token should be used instead.
The most recent refresh token is always returned when refreshing a token,
but any saved refresh tokens need to be updated too.

Application configuration
-------------------------
Should you want to use environment variables or configuration files
to provide application credentials, functions for reading those values
are provided in the :mod:`util <spotipy.util.config>` module.
Set values in your environment or write a configuration file.

.. code:: sh

    export SPOTIPY_CLIENT_ID=your_id
    export SPOTIPY_CLIENT_SECRET=your_secret
    export SPOTIPY_REDIRECT_URI=your_uri

.. code::

    [DEFAULT]
    SPOTIPY_CLIENT_ID=your_id
    SPOTIPY_CLIENT_SECRET=your_secret
    SPOTIPY_REDIRECT_URI=your_uri

Then read those values.
Functions that read configuration return a 3-tuple of configuration variables.

.. code:: python

   from spotipy.util import config_from_environment, config_from_file
   client_id, client_secret, redirect_uri = config_from_environment()
   client_id, client_secret, redirect_uri = config_from_file(filename)

They can then be used to retrieve access tokens.
Note that if all configuration values are defined,
it is possible to use unpacking to provide the configuration.

.. code:: python

   from spotipy import util

   conf = util.config_from_environment()
   token = util.prompt_for_user_token(*conf)

Configuring a user refresh token is also possible.
Define ``SPOTIPY_USER_REFRESH`` and pass in a boolean flag
to read it as a fourth configuration value.

.. code:: python

    util.config_from_environment(return_refresh=True)

Configuration files can be written using another utility function.
This is handy if a user's refresh token needs to be stored.

.. code:: python

    util.config_to_file(filename, (id_, secret, uri, refresh))

Sending requests
----------------
By default Spotipy doesn't do anything clever when sending requests.
Its functionality, however, can be extended in a number of ways
using different kinds of :mod:`senders <spotipy.sender>`.
They provide the immediate
`advantages <https://2.python-requests.org/en/master/user/advanced/#session-objects>`_
of using a :class:`requests.Session`.
They can bring new functionality, use user-defined sessions
and pass additional keyword arguments to :class:`Session.send`.
For example per-instance sessions can be enabled with a
:class:`PersistentSender <spotipy.sender.PersistentSender>`.

.. code:: python

   from spotipy import Spotify
   from spotipy.sender import PersistentSender

   Spotify(sender=PersistentSender())

.. _advanced-caching:

Response caching
----------------
The Spotify Web API returns headers for caching responses.
Spotipy does not implement caching, but a :mod:`sender <spotipy.sender>`
can be implemented to provide it.
For example the
`CacheControl <https://pypi.org/project/CacheControl/>`_
library provides caching algorithms that also wrap around :class:`Session`.
For further information see the Web API
`overview <https://developer.spotify.com/documentation/web-api/>`_.

Traversing paging objects
-------------------------
Many Web API endpoints that would return a large number of the same
type of object return paging objects for performance reasons.
The :class:`client <spotipy.client.Spotify>`
defines a few ways to navigate these pagings.
Next and previous pages can be requested one at a time.

.. code:: python

    tracks = spotify.playlist_tracks('37i9dQZEVXbMDoHDwVN2tF', limit=10)
    t_next = spotify.next(tracks)
    t_prev = spotify.previous(t_next)

To retrieve the whole content additional methods are available.

.. code:: python

    pages = spotify.all_pages(tracks)
    items = spotify.all_items(tracks)
