.. _advanced-usage:
.. currentmodule:: tekore

Advanced usage
==============
Working with access tokens
--------------------------
Authorisation methods
*********************
There are many authorisation options for both applications and users.
Here's a summary, see :ref:`auth` for more details.

- **Subject**: is the resulting token an application or user token
- **Creation**: is the method for generating new tokens or refreshing them
- **Type**: is the resulting token expiring or automatically refreshing

.. |exp-app-new| replace:: :meth:`Credentials.request_client_token`
.. |exp-usr-new| replace:: :meth:`Credentials.request_user_token`
.. |exp-usr-ref| replace:: :meth:`Credentials.refresh_user_token`
.. |exp-a-u-ref| replace:: :meth:`Credentials.refresh`
.. |ref-app-new| replace:: :meth:`RefreshingCredentials.request_client_token`
.. |ref-usr-new| replace:: :meth:`RefreshingCredentials.request_user_token`
.. |ref-usr-ref| replace:: :meth:`RefreshingCredentials.refresh_user_token`
.. |utl-app-new| replace:: :func:`request_client_token`
.. |utl-usr-new| replace:: :func:`prompt_for_user_token`
.. |utl-usr-ref| replace:: :func:`refresh_user_token`

+----------+----------+------------+-------+---------------+
| Subject  | Creation | Type       | Notes | Method        |
+==========+==========+============+=======+===============+
| App      | New      | Expiring   |       | |exp-app-new| |
+----------+----------+------------+-------+---------------+
| User     | New      | Expiring   | 1     | |exp-usr-new| |
+----------+----------+------------+-------+---------------+
| User     | Refresh  | Expiring   |       | |exp-usr-ref| |
+----------+----------+------------+-------+---------------+
| A+U      | Refresh  | Expiring   | 2     | |exp-a-u-ref| |
+----------+----------+------------+-------+---------------+
| App      | New      | Refreshing |       | |ref-app-new| |
+----------+----------+------------+-------+---------------+
| User     | New      | Refreshing | 1     | |ref-usr-new| |
+----------+----------+------------+-------+---------------+
| User     | Refresh  | Refreshing |       | |ref-usr-ref| |
+----------+----------+------------+-------+---------------+
| App      | New      | Refreshing | 3     | |utl-app-new| |
+----------+----------+------------+-------+---------------+
| User     | New      | Refreshing | 3, 4  | |utl-usr-new| |
+----------+----------+------------+-------+---------------+
| User     | Refresh  | Refreshing | 3     | |utl-usr-ref| |
+----------+----------+------------+-------+---------------+

**Notes**

1. These methods are paired with the first step of user authorisation:
   redirecting the user to a URL to login with Spotify.
2. This is a subject-agnostic refresh, fit for both app and user tokens.
   For application tokens, a new token is returned.
3. These methods wrap around :class:`RefreshingCredentials` internally.
4. Requires manually pasting text to a terminal, is not usable on a server.

:class:`UserAuth` can be used to simplify the implementation
of user authorisation with either one of the credentials clients.

Security
********
Using a state with user authorisation prevents cross-site request forgery
(`RFC 6749 <https://tools.ietf.org/html/rfc6749#section-10.12>`_).
A string can be sent as state on authorisation.
When a user is redirected back,
the same state should be returned as a query parameter.
:func:`gen_state` is provided to generate random strings to send as state.
:func:`parse_state_from_url` can then be used to extract the returned state.
State is generated and checked automatically when using :class:`UserAuth`.

Expanding scopes
****************
The scope of a token can be gradually expanded.
When authorising with a user, the scope of the resulting token is determined
by the scopes that were set at the start of authorisation.
But when refreshing a token, the scope is expanded to cover all scopes
that the user has granted a particular application in previous authorisations.
This holds for refresh tokens of both new and previously generated tokens.

Providing tokens
****************
The :ref:`client <client>` provides two ways of authenticating requests.
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

Token persistence
*****************
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

Client options
--------------
The :ref:`client <client>` provides options and toggles
to customise behavior in a variety of ways.

Maximise limits
***************
The Web API limits the number of resources returned in many endpoints.
By default, these limits are below their maximum values, matching API defaults.
However, they can be maximised when instantiating a client or as a context.

.. code:: python

    spotify = tk.Spotify(max_limits_on=True)
    spotify.max_limits_on = False

    with spotify.max_limits():
        tracks = spotify.all_items(spotify.search('piano')[0])

Chunked requests
****************
Endpoints that accept lists of resources often limit
the amount of items that can be passed in.
To help with this restriction, those lists can be chunked.

.. code:: python

    spotify = tk.Spotify(chunked_on=True)
    spotify.chunked_on = False

    with spotify.chunked():
        # Go nuts with e.g. spotify.artists_follow


Application configuration
-------------------------
It is generally advisable to separate configuration from code,
and more importantly keep secrets outside public version control.
To facilitate that, environment variables and configuration files
can be used to provide application credentials.
Set values in your environment or write a configuration file,
then read the configuration.

.. code:: sh

    export SPOTIFY_CLIENT_ID=your_id
    export SPOTIFY_CLIENT_SECRET=your_secret
    export SPOTIFY_REDIRECT_URI=your_uri

.. code::

    [DEFAULT]
    SPOTIFY_CLIENT_ID=your_id
    SPOTIFY_CLIENT_SECRET=your_secret
    SPOTIFY_REDIRECT_URI=your_uri

.. code:: python

   client_id, client_secret, redirect_uri = tk.config_from_environment()
   client_id, client_secret, redirect_uri = tk.config_from_file(filename)

These values can then be used to retrieve access tokens.
Note that if all configuration values are defined,
it is possible to use unpacking to provide the configuration.

.. code:: python

   conf = tk.config_from_environment()
   cred = tk.Credentials(*conf)

Configuring a user refresh token is also possible.
Define ``SPOTIFY_USER_REFRESH`` and pass in a boolean flag
to read it as a fourth configuration value.

.. code:: python

    tk.config_from_environment(return_refresh=True)

Configuration files can be written too.
This is handy if a user's refresh token needs to be stored.

.. code:: python

    tk.config_to_file(filename, (id_, secret, uri, refresh))

For more information see :ref:`config`.

Using senders
-------------
By default Tekore doesn't do anything clever when sending requests.
Its functionality, however, can be extended in a number of ways
using different kinds of :ref:`senders <senders>`.
Builtin senders can be used for retrying and caching.

Keepalive connections, retries and caching make up a performance-boosting
and convenient setup, easily constructed from simple building blocks.
Less errors, less requests and faster responses, particularly for
busy applications that request the same static resources repeatedly.

.. code:: python

    sender = tk.CachingSender(
        max_size=256,
        sender=tk.RetryingSender(retries=2)
    )

    tk.Spotify(sender=sender)

Traversing paging objects
-------------------------
Many Web API endpoints that would return a large number of the same
type of object return paging objects for performance reasons.
The :ref:`client <client>` defines a few ways to navigate these pagings.
Next and previous pages can be requested one at a time.

.. code:: python

    import tekore as tk

    spotify = tk.Spotify(token)
    tracks = spotify.playlist_tracks('37i9dQZEVXbMDoHDwVN2tF', limit=10)
    t_next = spotify.next(tracks)
    t_prev = spotify.previous(t_next)

To retrieve the whole content additional methods are available.

.. code:: python

    pages = spotify.all_pages(tracks)
    items = spotify.all_items(tracks)

.. _async:

Async support
-------------
Tekore provides support for asynchronous programming with async-await.
Async mode may be enabled when instantiating a :class:`Client`.

.. code:: python

    tk.Credentials(*conf, asynchronous=True)
    tk.Spotify(token, asynchronous=True)

Alternatively, an asynchronous sender may be passed directly into a client.

.. code:: python

    spotify = tk.Spotify(token, sender=tk.AsyncSender())

.. note::

   The boolean parameter above overrides any conflicting :ref:`sender <senders>`
   that is set as default or simultaneously passed in to the client.

Now every call to an endpoint returns an awaitable instead of a response.
:mod:`asyncio` can then be used to execute asynchronous requests.
See :ref:`senders` and :ref:`examples` for more information.

.. code:: python

    import asyncio

    async def now_playing():
        return await spotify.playback_currently_playing()

    np = asyncio.run(now_playing())

While asynchronous :class:`Credentials` is supported, it is worth considering
that concurrently refreshing tokens may lead to multiple refreshes for one token.
Synchronous credentials clients are recommended.

Localisation
------------
Many API calls that retrieve track information accept a ``market`` or
``country`` parameter with which only tracks or albums available in that
market are returned. This sometimes changes track IDs as well.
When calling with a user token, this country code can also be
``from_token``, in which case the results are for the user's locale.

.. code:: python

    spotify.search('sheeran', market='SE')
    spotify.search('horse', market='from_token')

In addition to returning results relevant to a specific market,
results can be requested in specific languages.
This is helpful for example in viewing names with non-latin alphabet.

.. code:: python

    from httpx import Client

    client = Client(headers={'Accept-Language': 'ru'})
    spotify = tk.Spotify(token, sender=tk.SyncSender(client))

    artist = spotify.artist('2LbinT29RFLaXOGAN0jfQN')
    print(artist.name)
