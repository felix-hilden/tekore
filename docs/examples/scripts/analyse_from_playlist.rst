Analyse track from playlist
===========================
The following script retrieves a track from one of your playlists
and analyses its features.

It assumes that your credentials are saved in the environment and
you have followed or created at least one playlist and it has a track on it.

.. code:: python

    from tekore import util, Spotify

    conf = util.config_from_environment()
    token = util.prompt_for_user_token(*conf)

    spotify = Spotify(token)
    playlist = spotify.followed_playlists(limit=1).items[0]
    track = spotify.playlist_tracks(playlist.id, limit=1).items[0].track

    print(f'Analysing {track.name}...\n')
    analysis = spotify.track_audio_features(track.id)
    analysis.pprint()
