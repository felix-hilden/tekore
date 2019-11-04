.. _getting-started:

Getting started
===============
To use the Web API, you'll need to register an
`application <https://developer.spotify.com/dashboard/applications>`_,
get its credentials and define a redirect URI for authentication requests.
Note that a server listening to that address isn't required for a demo,
though it is required for programmatic extraction of user access tokens.

Retrieving an access token
--------------------------
First we'll retrieve an access token that has every possible right (scope)
to a user's account.
The script will open a web page prompting for a Spotify login.
The user is then redirected back and the URL of the redirect is requested
for parsing and retrieving the access token.

.. code:: python

    from spotipy.scope import every
    from spotipy.util import prompt_for_user_token

    client_id = 'your_token_here'
    client_secret = 'your_secret_here'
    redirect_uri = 'http://localhost'

    token = prompt_for_user_token(
        client_id,
        client_secret,
        redirect_uri,
        scope=every
    )

Calling the API
---------------
Next the Spotify object should be created.
The following script will list some of the user's top tracks.

.. code:: python

    from spotipy import Spotify

    s = Spotify(token)

    tracks = s.current_user_top_tracks(limit=10)
    for track in tracks.items:
        print(track.name)

The snippet below will play Sibelius' Finlandia if the user has
an active (recently used) Spotify application open.
If no active device is found, an error is thrown.

.. code:: python

    finlandia = '3hHWhvw2hjwfngWcFjIzqr'
    s.playback_start(track_ids=[finlandia])
