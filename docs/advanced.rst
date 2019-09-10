Advanced usage
==============
Senders
-------
By default ``Spotipy`` doesn't do anything clever to requests that are sent.
Its functionality, however, can be extended in a number of ways
using different kinds of :class:`Sender` classes.
They wrap around :class:`requests.Session` to provide new functionality and
`other advantages <https://2.python-requests.org/en/master/user/advanced/#session-objects>`_
of using sessions.
Here's a short summary of the features of each sender.

- :class:`TransientSender`: Creates a new session for each request (default)
- :class:`PersistentSender`: Reuses a session for requests made on the same instance
- :class:`SingletonSender`: Uses a global session for all instances and requests
- :class:`RetryingSender`: Extends any sender to enable retries on failed requests

For example:

.. code:: python

   from spotipy import Spotify
   from spotipy.sender import PersistentSender

   Spotify(sender=PersistentSender())

Request retries
***************
Should an error response be returned,
a :class:`RetryingSender` can be used to retry requests for a number of times.
To enable retries, pass an instance of the sender to a client.

.. code:: python

   from spotipy import Spotify
   from spotipy.sender import RetryingSender

   s = Spotify(sender=RetryingSender(retries=3))

The retrying sender can be extend any other sender to easily provide
the equivalent, combined functionality.

.. code:: python

   from spotipy import Spotify
   from spotipy.sender import SingletonSender, RetryingSender

   sender = RetryingSender(sender=SingletonSender())
   s = Spotify(sender=sender)

Caching
*******
The Spotify Web API returns headers for caching requests.
See the Web API
`overview <https://developer.spotify.com/documentation/web-api/>`_
for further information.
``Spotipy`` does not implement response caching,
but `Senders`_ can easily be subclassed for arbitrary extension.
For example the
`CacheControl <https://pypi.org/project/CacheControl/>`_
library provides caching algorithms that also wrap around :class:`Session`.

Providing tokens
----------------
The client provides two ways of authenticating requests.
Firstly it accepts an access token in the constructor.

.. code:: python

   s = Spotify(token)
   a = s.artist(artist_id)

Secondly, a context manager ``Spotify.token`` is provided
for using a particular token for requests within the context.
This is particularly handy if one object is created for all requests
but requests need to use different tokens,
be it due to number of users, token refreshing or scopes.

.. code:: python

   s = Spotify(app_token)
   a = s.artist(artist_id)

   with s.token(user_token):
       user = s.current_user()
