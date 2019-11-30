Play saved album
================
The following script plays one of your saved albums.

It assumes that your credentials are saved in the environment,
there is at least one album saved in your library,
and you have an active Spotify application open.

.. code:: python

    from spotipy import util, Spotify
    from spotipy.scope import scopes
    from spotipy.convert import to_uri

    cred = util.credentials_from_environment()
    scope = scopes.user_library_read + scopes.user_modify_playback_state
    token = util.prompt_for_user_token(*cred, scope=scope)

    spotify = Spotify(token)
    album = spotify.saved_albums(limit=1).items[0].album
    album_uri = to_uri('album', album.id)
    spotify.playback_start_context(album_uri)
