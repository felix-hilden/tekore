Analyse track from playlist
===========================
The following script retrieves a track from one of your playlists
and analyses its features.

It assumes that your credentials are saved in the environment and
you have followed or created at least one playlist and it has a track on it.
Podcast episodes or a locally saved tracks are ignored,
because they cannot be analysed.

.. code:: python

    import tekore as tk

    conf = tk.config_from_environment()
    token = tk.prompt_for_user_token(*conf)

    spotify = tk.Spotify(token)
    playlist = spotify.followed_playlists(limit=1).items[0]
    track = spotify.playlist_items(playlist.id, limit=1).items[0].track
    name = f'"{track.name}" from {playlist.name}'

    if track.episode:
        print(f'Cannot analyse episodes!\nGot {name}.')
    elif track.track and track.is_local:
        print(f'Cannot analyse local tracks!\nGot {name}.')
    else:
        print(f'Analysing {name}...\n')
        analysis = spotify.track_audio_features(track.id)
        print(repr(analysis))
