.. _advanced-usage:
.. currentmodule:: tekore

Advanced usage
==============
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
    items = spotify.playlist_items('37i9dQZEVXbMDoHDwVN2tF', limit=10)
    t_next = spotify.next(items)
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

.. note::

    :ref:`client` context managers are async safe on Python 3.7+, meaning that
    they can be used in many tasks without affecting the state of other tasks.
    *However*, setting values outside of all contexts modifies the persistent
    value directly, and as such may affect other tasks.

.. warning::

    :ref:`client` context managers are **not** async safe on Python 3.6
    due to missing async implementation in the PyPI backport of
    the ``contextvars`` package from the standard library of Python 3.7.

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
