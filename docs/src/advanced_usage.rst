.. _advanced-usage:

Advanced usage
==============
Working with access tokens
--------------------------
Retrieving user tokens
**********************
:func:`prompt_for_user_token <tekore.util.credentials.prompt_for_user_token>`
provides a convenient way of retrieving
an access token that refreshes automatically when about to expire.
However, it is intended for local use as it opens up a browser window.
For situations involving a server, a two-step process should be implemented.

- Redirect a user to a specific URL
- Receive an access token as a result of the authentication

The steps are covered by two methods of the
:class:`Credentials <tekore.auth.expiring.Credentials>` class.
See this recipe on an :ref:`auth-server` for an example implementation.
The same process can be implemented using
:class:`RefreshingCredentials <tekore.auth.refreshing.RefreshingCredentials>`.

Providing tokens
****************
The :mod:`client <tekore.client>` provides two ways of authenticating requests.
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
Whether you are using :mod:`auth <tekore.auth>` or
:mod:`util <tekore.util.credentials>`,
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

Client options
--------------
The :mod:`client <tekore.client>` provides options and toggles
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
Should you want to use environment variables or configuration files
to provide application credentials, functions for reading those values
are provided in the :mod:`util <tekore.util.config>` module.
Set values in your environment or write a configuration file.

.. code:: sh

    export SPOTIFY_CLIENT_ID=your_id
    export SPOTIFY_CLIENT_SECRET=your_secret
    export SPOTIFY_REDIRECT_URI=your_uri

.. code::

    [DEFAULT]
    SPOTIFY_CLIENT_ID=your_id
    SPOTIFY_CLIENT_SECRET=your_secret
    SPOTIFY_REDIRECT_URI=your_uri

Then read those values.
Functions that read configuration return a 3-tuple of configuration variables.

.. code:: python

   client_id, client_secret, redirect_uri = tk.config_from_environment()
   client_id, client_secret, redirect_uri = tk.config_from_file(filename)

They can then be used to retrieve access tokens.
Note that if all configuration values are defined,
it is possible to use unpacking to provide the configuration.

.. code:: python

   conf = tk.config_from_environment()
   token = tk.prompt_for_user_token(*conf)

Configuring a user refresh token is also possible.
Define ``SPOTIFY_USER_REFRESH`` and pass in a boolean flag
to read it as a fourth configuration value.

.. code:: python

    tk.config_from_environment(return_refresh=True)

Configuration files can be written using another utility function.
This is handy if a user's refresh token needs to be stored.

.. code:: python

    tk.config_to_file(filename, (id_, secret, uri, refresh))

Using senders
-------------
By default Tekore doesn't do anything clever when sending requests.
Its functionality, however, can be extended in a number of ways
using different kinds of :mod:`senders <tekore.sender>`.
They can be used for connection persistence, retrying and caching.
User-defined sessions and additional keyword arguments
to :func:`requests.Session.send` can also be passed in.
For example, per-instance sessions can be enabled with a
:class:`PersistentSender <tekore.sender.PersistentSender>`.

.. code:: python

   tk.Spotify(sender=tk.PersistentSender())

Keepalive connections, retries and caching make up a performance-boosting
and convenient sender setup, easily constructed from simple building blocks.
Less errors, less requests and faster responses, particularly for
busy applications that request the same static resources repeatedly.

.. code:: python

    tk.sender.default_sender_instance = tk.CachingSender(
        max_size=256,
        sender=tk.RetryingSender(
            retries=2,
            sender=tk.PersistentSender()
        )
    )

For more detailed information, see :ref:`performance`.

Traversing paging objects
-------------------------
Many Web API endpoints that would return a large number of the same
type of object return paging objects for performance reasons.
The :class:`client <tekore.client.Spotify>`
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

Async support
-------------
Tekore provides support for asynchronous programming with async-await.
Async mode may be enabled when instantiating a client.

.. code:: python

    tk.Credentials(*conf, asynchronous=True)
    tk.Spotify(token, asynchronous=True)

Note that the boolean parameter above overrides any conflicting
:class:`Sender <tekore.sender.Sender>` that is set as default
or simultaneously passed in to the client.
Alternatively, an asynchronous sender may be passed directly into a client.

.. code:: python

    spotify = tk.Spotify(token, sender=tk.AsyncPersistentSender())

Now every call to an endpoint returns an awaitable instead of a response.
:mod:`asyncio` can then be used to execute asynchronous requests.
See the :mod:`sender <tekore.sender>` module
and :ref:`examples` for more information.

.. code:: python

    import asyncio

    async def now_playing():
        return await spotify.playback_currently_playing()

    np = asyncio.run(now_playing())

While asynchronous :class:`Credentials <tekore.auth.expiring.Credentials>`
is supported, it is worth considering that concurrently refreshing tokens
may lead to multiple refreshes for one token.
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

    from requests import Session

    sess = Session()
    sess.headers = {'Accept-Language': 'ru'}

    spotify = tk.Spotify(token, sender=tk.PersistentSender(session=sess))
    artist = spotify.artist('2LbinT29RFLaXOGAN0jfQN')
    print(artist.name)
