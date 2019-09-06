Advanced usage
==============
By default ``Spotipy`` doesn't do anything clever to requests that are sent.
Its functionality, however, can be extended in a number of ways.

Request retries
---------------
Should an error response be returned,
:class:`Spotify` can retry requests for a set number of times.
Provide a retry value when initialising the client to enable retries.

Senders
-------
Connection pooling and
`other advantages <https://2.python-requests.org/en/master/user/advanced/#session-objects>`_
of using :class:`Sessions` are available through different :class:`Senders`.
By default :class:`Spotify` uses a :class:`TransientSender`,
which creates a new session for each request.
:class:`SingletonSender` is also available.
As the name implies, it uses a global session for all its instances and requests.
:class:`ReusingSender` creates a session per instance.

Caching
-------
The Spotify Web API returns headers for caching requests.
See the Web API
`overview <https://developer.spotify.com/documentation/web-api/>`_
for further information.
``Spotipy`` does not implement caching, but does expose `Senders`_
which can easily be subclassed for arbitrary extension.
For example the
`CacheControl <https://pypi.org/project/CacheControl/>`_
library provides caching algorithms that wrap around :class:`Session`.

Providing tokens
----------------
The client provides two ways of authenticating requests.
It accepts an access token in the constructor.

.. code:: python

   s = Spotify(token)
   a = s.artist(artist_id)

A context manager ``token`` is provided for using a particular token
for requests within the context.
This is particularly handy if one object is created for all requests
but requests need to use different tokens,
be it due to number of users, token refreshing or scopes.

.. code:: python

   s = Spotify(app_token)
   a = s.artist(artist_id)

   with s.token(user_token):
       user = s.current_user()
