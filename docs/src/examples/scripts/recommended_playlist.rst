Recommended tracks playlist
===========================
The following script recommends songs based on your top tracks
and creates a playlist from them.

It assumes that your credentials are saved in the environment
and you have used Spotify enough to have top tracks.

.. code:: python

    import tekore as tk

    conf = tk.config_from_environment()
    scope = tk.scope.user_top_read + tk.scope.playlist_modify_private
    token = tk.prompt_for_user_token(*conf, scope=scope)

    spotify = tk.Spotify(token)
    top_tracks = spotify.current_user_top_tracks(limit=5).items
    top_track_ids = [t.id for t in top_tracks]
    recommendations = spotify.recommendations(track_ids=top_track_ids).tracks

    user = spotify.current_user()
    playlist = spotify.playlist_create(
        user.id,
        'Tekore Recommendations',
        public=False,
        description='Recommendations based on your top tracks <3'
    )
    uris = [t.uri for t in recommendations]
    spotify.playlist_add(playlist.id, uris=uris)
