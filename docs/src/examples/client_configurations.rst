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

    import tekore as tk

    conf = tk.config_from_environment()
    token = tk.prompt_for_user_token(*conf, scope=tk.scope.every)
    spotify = tk.Spotify(token, sender=tk.PersistentSender())

    user = spotify.current_user()

Save the refresh token to avoid authenticating again when restarting.

.. code:: python

    # Load refresh token
    refresh_token = ...
    token = tk.refresh_user_token(*conf[:2], refresh_token)


Server application or multiple users
------------------------------------

Server projects or ones that have multiple users can benefit from
using the application token and swapping in user tokens.

.. code:: python

    import tekore as tk

    conf = tk.config_from_environment()
    cred = tk.Credentials(*conf)
    app_token = cred.request_client_token()

    spotify = tk.Spotify(app_token, sender=tk.PersistentSender())

    # Retrieve user token
    user_token = ...

    with spotify.token_as(user_token):
        user = spotify.current_user()

If multiple clients are instantiated,
consider using a :class:`SingletonSender <tekore.sender.SingletonSender>` instead.
