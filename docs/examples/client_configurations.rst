Client configurations
=====================
Here are some examples of client configurations.
Adjust the configurations based on the number of instances
or type of :class:`Sender` you want.

Local application, single user
------------------------------

If you don't want to or can't spin up a server,
authentication can be completed with some manual work.

.. code:: python

    from spotipy import Spotify, util
    from spotipy.scope import every
    from spotipy.sender import PersistentSender

    conf = util.credentials_from_environment()
    token = util.prompt_for_user_token(*conf, scope=every)
    s = Spotify(token=token, sender=PersistentSender())

    user = s.current_user()

Save the refresh token to avoid authenticating again when restarting.

.. code:: python

    # Load refresh token
    refresh_token = ...
    token = util.refresh_user_token(*conf, refresh_token)


Server application or multiple users
------------------------------------

Server projects or ones that have multiple users can benefit from
using the application token and swapping in user tokens.

.. code:: python

    from spotipy import Spotify, Credentials
    from spotipy.util import credentials_from_environment
    from spotipy.sender import PersistentSender

    conf = credentials_from_environment()
    cred = Credentials(*conf)
    app_token = cred.request_client_token()

    s = Spotify(token=app_token, sender=PersistentSender())

    # Retrieve user token
    user_token = ...

    with s.token_as(user_token):
        user = s.current_user()

If multiple clients are instantiated,
consider using a :class:`SingletonSender` instead.
