.. _getting-started:

Getting started
===============
To use the Web API, you'll need to register an
`application <https://developer.spotify.com/dashboard/applications>`_,
get its credentials and define a whitelisted redirect URI for authentication
requests in your application settings.
Note that a server listening to that address isn't required for a demo,
though it is required for programmatic extraction of user access tokens.

Retrieving a client token
-------------------------
First we'll retrieve a client token for the Spotify application.
It is a token associated with your registered application
and can be used to make basic calls to the API.

.. code:: python

    from spotipy.util import request_client_token

    client_id = 'your_token_here'
    client_secret = 'your_secret_here'
    redirect_uri = 'your_redirect_here'

    app_token = request_client_token(client_id, client_secret, redirect_uri)

Calling the API
---------------
Next the Spotify object should be created.
The following script will list the track numbers and names of songs
on an album given the album ID.

.. code:: python

    from spotipy import Spotify

    spotify = Spotify(app_token)

    album = spotify.album('3RBULTZJ97bvVzZLpxcB0j')
    for track in album.tracks.items:
        print(track.track_number, track.name)

Retrieving a user token
-----------------------
User tokens are another type of access token.
They are associated with a Spotify user account.
Different privileges or `scopes` can be requested when authenticating.
Below we'll retrieve a token that has every possible scope.
The script will open a web page prompting for a Spotify login.
The user is then redirected back and the URL of the redirect is requested
for parsing and retrieving the access token.

.. code:: python

    from spotipy.scope import every
    from spotipy.util import prompt_for_user_token

    user_token = prompt_for_user_token(
        client_id,
        client_secret,
        redirect_uri,
        scope=every
    )

Calling the API as a user
-------------------------
Many endpoints require user authentication,
like the ones with a ``current_user`` prefix and others related to playback.
The following script swaps in the user token and
lists some of the user's most listened tracks.

.. code:: python

    spotify.token = user_token

    tracks = s.current_user_top_tracks(limit=10)
    for track in tracks.items:
        print(track.name)

The snippet below will play Sibelius' Finlandia if the user has
an active (recently used) Spotify application open.
If no active device is found, an error is thrown.

.. code:: python

    finlandia = '3hHWhvw2hjwfngWcFjIzqr'
    s.playback_start(track_ids=[finlandia])
