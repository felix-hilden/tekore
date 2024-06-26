.. _getting-started:

Getting started
===============
To use the Web API, you'll need to register an `application`_.
From its page retrieve the client ID and secret.
They are your application's credentials to the API.
A walkthrough of creating an application and setting it up can be found `here
<https://developer.spotify.com/documentation/general/guides/app-settings/>`_.

Retrieving a client token
-------------------------
First we'll retrieve a client token for the Spotify application.
It is a token associated with your application
and can be used to make basic calls to the API.

.. autolink-concat::
.. code:: python

    import tekore as tk

    client_id = 'your_id_here'
    client_secret = 'your_secret_here'

    app_token = tk.request_client_token(client_id, client_secret)

Calling the API
---------------
Next the Spotify object should be created.
The following script will list the track numbers and names of songs
on an album given the album ID.

.. code:: python

    spotify = tk.Spotify(app_token)

    album = spotify.album('3RBULTZJ97bvVzZLpxcB0j')
    for track in album.tracks.items:
        print(track.track_number, track.name)

Response attributes can be directly accessed with dot notation as above.
To quickly inspect a response or any part of it, print its contents.

.. code:: python

    print(album)
    print(album.artists[0])

Retrieving a user token
-----------------------
Many endpoints require user authorisation,
for which another type of access token is needed.
User tokens are associated with a Spotify user account.

Retrieving them requires some more setting up.
A redirect URI should be whitelisted in `application`_ settings.
It is the address to which users are redirected
after authorising the application.
Alternatively, the default redirect URI ``https://example.com/callback``
can be used with a client with no other redirect URIs whitelisted.

Different privileges or `scopes` can be requested when authorising.
Below we'll retrieve a token that has every possible scope.
The script will open a web page prompting for a Spotify login.
To only display the authorization URI, without opening it in a browser,
set `open_browser` to `False` in `prompt_for_user_token`.
The user is then redirected back to the whitelisted redirect URI.
Paste the redirected URI in full to the shell to finalise token retrieval.

.. code:: python

    redirect_uri = 'your_uri_here'

    user_token = tk.prompt_for_user_token(
        client_id,
        client_secret,
        redirect_uri,
        scope=tk.scope.every
    )

.. note::

    :func:`prompt_for_user_token` eliminates the need for a web server,
    which would normally be used to complete authorisation,
    by requesting the user to manually enter information to the shell.
    However, that also makes it unusable on a server.
    Other authorisation methods are introduced in :ref:`auth-guide`.

Calling the API as a user
-------------------------
The following script replaces the application token with a user token and
lists some of the user's most listened tracks.

.. code:: python

    spotify.token = user_token

    tracks = spotify.current_user_top_tracks(limit=10)
    for track in tracks.items:
        print(track.name)

The snippet below will play Sibelius' Finlandia if the user has
a recently used Spotify application open.
If no active device is found, an error is thrown.

.. code:: python

    finlandia = '3hHWhvw2hjwfngWcFjIzqr'
    spotify.playback_start_tracks([finlandia])

Saving the configuration
------------------------
Currently, we need to go through the authorisation process every time
the script is run. Let's save the configuration to avoid this in the future.

.. code:: python

    conf = (client_id, client_secret, redirect_uri, user_token.refresh_token)
    tk.config_to_file('tekore.cfg', conf)

Now we can replace the authorisation lines with reconstructing the token.

.. code:: python

    conf = tk.config_from_file('tekore.cfg', return_refresh=True)
    user_token = tk.refresh_user_token(*conf[:2], conf[3])

.. note::

    This approach is not scalable to multi-user scenarios.
    See :ref:`auth-guide` for more information.

How to read the documentation
-----------------------------
The reference documentation is built for easy navigation.
Each endpoint (like :meth:`playback <tekore.Spotify.playback>`) contains
a description, required and optional scopes, arguments and return information.
Notably, the return type often contains a link to the relevant response model.
Follow them to discover the attributes that a model has.
Further links can be followed down the model hierarchy.

What's next?
------------
Our :ref:`auth-guide` details different authorisation options.
:ref:`advanced-usage` provides an overview of things to keep in mind
when building an actual application and what Tekore has to offer for that.
You could also have a look at some :ref:`example scripts <examples>`
to start familiarising yourself with the Web API.

.. _application: https://developer.spotify.com/dashboard/applications
