.. _getting-started:

Getting started
===============
To use the Web API, you'll need to register an
`application <https://developer.spotify.com/dashboard/applications>`_.
From its page retrieve the client ID and secret,
and define a whitelisted redirect URI in application settings.
Note that a server listening to that address isn't required for a demo,
though it is required for programmatic extraction of user access tokens.

Retrieving a client token
-------------------------
First we'll retrieve a client token for the Spotify application.
It is a token associated with your registered application
and can be used to make basic calls to the API.

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

Retrieving a user token
-----------------------
Many endpoints require user authentication,
for which another type of access token is needed.
User tokens are associated with a Spotify user account.
Different privileges or `scopes` can be requested when authenticating.
Below we'll retrieve a token that has every possible scope.

The script below will open a web page prompting for a Spotify login.
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
an active (recently used) Spotify application open.
If no active device is found, an error is thrown.

.. code:: python

    finlandia = '3hHWhvw2hjwfngWcFjIzqr'
    spotify.playback_start_tracks([finlandia])

What's next?
------------
Have a look at some :ref:`example scripts <examples>` to start familiarising
yourself with the Web API.
:ref:`advanced-usage` provides an overview of what Tekore has to offer
and things to keep in mind when building an actual application.
