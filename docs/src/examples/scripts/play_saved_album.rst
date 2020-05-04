Play saved album
================
The following script plays one of your saved albums.

It assumes that your credentials are saved in the environment,
there is at least one album saved in your library,
and you have an active Spotify application open.

.. code:: python

    import tekore as tk

    conf = tk.config_from_environment()
    scope = tk.scope.user_library_read + tk.scope.user_modify_playback_state
    token = tk.prompt_for_user_token(*conf, scope=scope)

    spotify = tk.Spotify(token)
    album = spotify.saved_albums(limit=1).items[0].album
    album_uri = tk.to_uri('album', album.id)
    spotify.playback_start_context(album_uri)
