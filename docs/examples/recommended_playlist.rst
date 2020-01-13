Recommended tracks playlist
===========================
The following script recommends songs based on your top tracks
and creates a playlist from them.

It assumes that your credentials are saved in the environment
and you have used Spotify enough to have top tracks.

.. code:: python

    from tekore import util, Spotify
    from tekore.scope import scopes

    conf = util.config_from_environment()
    scope = scopes.user_top_read + scopes.playlist_modify_private
    token = util.prompt_for_user_token(*conf, scope=scope)

    spotify = Spotify(token)
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
    track_ids = [t.id for t in recommendations]
    spotify.playlist_tracks_add(playlist.id, track_ids=track_ids)
