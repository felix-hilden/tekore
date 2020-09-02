.. _creating-scripts:
.. currentmodule:: tekore

Creating local scripts
======================
The examples below give a framework for creating scripts to be run locally.

First we specify our client configuration and authorise a user.
Once complete, the configuration is written to a file, along with the user's
refresh token which can be used to spawn new tokens without authorising again.

.. note::

    The code below uses the default redirect URI
    ``https://example.com/callback``, which doesn't need to be configured.
    However, if another redirect URI *has* been configured, it will not work.

.. code:: python

    import tekore as tk

    client_id = 'your_client_id'
    client_secret = 'your_client_secret'
    redirect_uri = 'https://example.com/callback'   # Or your redirect uri
    conf = (client_id, client_secret, redirect_uri)
    file = 'tekore.cfg'

    token = tk.prompt_for_user_token(*conf, scope=tk.scope.every)
    tk.config_to_file(file, conf + (token.refresh_token,))

That file can then be read whenever a script is started,
and a refreshed token requested without user interaction.
Thanks to the self-refreshing tokens returned by :func:`refresh_user_token`,
even long-running scripts can simply use the same token indefinitely.

.. note::

    When only application tokens are needed, ``client_id`` and
    ``client_secret`` can be written to a file without initial authorisation.

.. code:: python

    import tekore as tk

    file = 'tekore.cfg'
    conf = tk.config_from_file(file, return_refresh=True)
    token = tk.refresh_user_token(*conf[:2], conf[3])

    spotify = tk.Spotify(token)
    print(spotify.current_user_top_artists())

The same principle applies to configuration residing in the system environment,
which can be accessed with :func:`config_from_environment`,
though configuration cannot be written to environment variables.
These snippets could also be combined to a single script
checking for the existence of configuration or even just the refresh token
to decide whether a new authorisation is needed or not.
