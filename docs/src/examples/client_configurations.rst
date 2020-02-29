Client configurations
=====================
Here are some examples of client configurations.
Adjust the configurations based on the number of instances
or type of :class:`Sender <tekore.sender.Sender>` you want.

Local application, single user
------------------------------

If you don't want to or can't spin up a server,
authentication can be completed with some manual work.

.. code:: python

    from tekore import Spotify, util
    from tekore.scope import every
    from tekore.sender import PersistentSender

    conf = util.config_from_environment()
    token = util.prompt_for_user_token(*conf, scope=every)
    s = Spotify(token=token, sender=PersistentSender())

    user = s.current_user()

Save the refresh token to avoid authenticating again when restarting.

.. code:: python

    # Load refresh token
    refresh_token = ...
    token = util.refresh_user_token(*conf[:2], refresh_token)


Server application or multiple users
------------------------------------

Server projects or ones that have multiple users can benefit from
using the application token and swapping in user tokens.

.. code:: python

    from tekore import Spotify, Credentials
    from tekore.util import config_from_environment
    from tekore.sender import PersistentSender

    conf = config_from_environment()
    cred = Credentials(*conf)
    app_token = cred.request_client_token()

    s = Spotify(token=app_token, sender=PersistentSender())

    # Retrieve user token
    user_token = ...

    with s.token_as(user_token):
        user = s.current_user()

If multiple clients are instantiated,
consider using a :class:`SingletonSender <tekore.sender.SingletonSender>` instead.
