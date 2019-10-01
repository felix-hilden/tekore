Advanced usage
==============
Providing tokens
----------------
The client provides two ways of authenticating requests.
Firstly it accepts an access token in the constructor.

.. code:: python

   s = Spotify(token)
   a = s.artist(artist_id)

Secondly, the client can temporarily use another token to make requests.
This is particularly handy if only one client instance is created but there are
many users, tokens are manually refreshed or a user has different scopes.

.. code:: python

   s = Spotify(app_token)
   a = s.artist(artist_id)

   with s.token_as(user_token):
       user = s.current_user()


Configuration with environment variables
----------------------------------------
Should you want to use environment variables to provide application credentials,
a function for reading those values is provided in the ``util`` module.

.. code:: python

   from spotipy.util import credentials_from_environment
   client_id, client_secret, redirect_uri = credentials_from_environment()

Those values can then be used to retrieve access tokens.
Note that if all configuration values are defined, the following is possible.

.. code:: python

   from spotipy import util

   conf = util.credentials_from_environment()
   token = util.prompt_for_user_token(*conf)


Retrieving user tokens
----------------------
``util.prompt_for_user_token`` provides a convenient way of retrieving
an access token that refreshes automatically when about to expire.
However, it is intended for local use as it opens up a browser window.
For situations involving a server, a two-step process should be implemented.

- Redirect a user to a specific URL
- Receive an access token as a result of the authentication

The steps are covered by ``user_authorisation_url`` and ``request_user_token``,
two methods of the :class:``Credentials` class in the ``auth`` module.
Note that ``request_user_token`` does not return
an automatically refreshing token but an expiring one.


Senders
-------
By default ``spotipy`` doesn't do anything clever to requests that are sent.
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
