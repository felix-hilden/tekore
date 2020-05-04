.. _client:

Client
======
Web API endpoints.

.. currentmodule:: tekore

Each method of the client corresponds to an API call, with some exceptions.
Further documentation on endpoints can be viewed in the Web API
`reference <https://developer.spotify.com/documentation/web-api/reference/>`_.

.. code:: python

    import tekore as tk

    # Initialise the client
    spotify = tk.Spotify(token)

    # Call the API
    album = spotify.album('3RBULTZJ97bvVzZLpxcB0j')
    for track in album.tracks.items:
        print(track.track_number, track.name)

Instantiation and options
-------------------------
.. autoclass:: Spotify
   :no-members:
   :no-show-inheritance:

.. automethod:: Spotify.chunked
.. automethod:: Spotify.max_limits
.. automethod:: Spotify.token_as

.. _client-paging:

Paging navigation
-----------------
.. autosummary::
   :nosignatures:

   Spotify.next
   Spotify.previous
   Spotify.all_items
   Spotify.all_pages

.. automethod:: Spotify.next
.. automethod:: Spotify.previous
.. automethod:: Spotify.all_items
.. automethod:: Spotify.all_pages

Album API
---------
.. autosummary::
   :nosignatures:

   Spotify.album
   Spotify.album_tracks
   Spotify.albums

.. automethod:: Spotify.album
.. automethod:: Spotify.album_tracks
.. automethod:: Spotify.albums

Artist API
----------
.. autosummary::
   :nosignatures:

   Spotify.artist
   Spotify.artist_albums
   Spotify.artist_related_artists
   Spotify.artist_top_tracks
   Spotify.artists

.. automethod:: Spotify.artist
.. automethod:: Spotify.artist_albums
.. automethod:: Spotify.artist_related_artists
.. automethod:: Spotify.artist_top_tracks
.. automethod:: Spotify.artists

Browse API
----------
.. autosummary::
   :nosignatures:

   Spotify.categories
   Spotify.category
   Spotify.category_playlists
   Spotify.featured_playlists
   Spotify.new_releases
   Spotify.recommendation_genre_seeds
   Spotify.recommendations

.. automethod:: Spotify.categories
.. automethod:: Spotify.category
.. automethod:: Spotify.category_playlists
.. automethod:: Spotify.featured_playlists
.. automethod:: Spotify.new_releases
.. automethod:: Spotify.recommendation_genre_seeds
.. automethod:: Spotify.recommendations

.. _client-episode:

Episode API
-----------
.. autosummary::
   :nosignatures:

   Spotify.episode
   Spotify.episodes

.. automethod:: Spotify.episode
.. automethod:: Spotify.episodes

Follow API
----------
.. autosummary::
   :nosignatures:

   Spotify.artists_follow
   Spotify.artists_is_following
   Spotify.artists_unfollow
   Spotify.followed_artists
   Spotify.playlist_follow
   Spotify.playlist_is_following
   Spotify.playlist_unfollow
   Spotify.followed_playlists
   Spotify.users_follow
   Spotify.users_is_following
   Spotify.users_unfollow

.. automethod:: Spotify.artists_follow
.. automethod:: Spotify.artists_is_following
.. automethod:: Spotify.artists_unfollow
.. automethod:: Spotify.followed_artists
.. automethod:: Spotify.playlist_follow
.. automethod:: Spotify.playlist_is_following
.. automethod:: Spotify.playlist_unfollow
.. automethod:: Spotify.followed_playlists
.. automethod:: Spotify.users_follow
.. automethod:: Spotify.users_is_following
.. automethod:: Spotify.users_unfollow

.. _client-library:

Library API
-----------
.. autosummary::
   :nosignatures:

   Spotify.saved_albums
   Spotify.saved_albums_add
   Spotify.saved_albums_contains
   Spotify.saved_albums_delete
   Spotify.saved_shows
   Spotify.saved_shows_add
   Spotify.saved_shows_contains
   Spotify.saved_shows_delete
   Spotify.saved_tracks
   Spotify.saved_tracks_add
   Spotify.saved_tracks_contains
   Spotify.saved_tracks_delete

.. automethod:: Spotify.saved_albums
.. automethod:: Spotify.saved_albums_add
.. automethod:: Spotify.saved_albums_contains
.. automethod:: Spotify.saved_albums_delete
.. automethod:: Spotify.saved_shows
.. automethod:: Spotify.saved_shows_add
.. automethod:: Spotify.saved_shows_contains
.. automethod:: Spotify.saved_shows_delete
.. automethod:: Spotify.saved_tracks
.. automethod:: Spotify.saved_tracks_add
.. automethod:: Spotify.saved_tracks_contains
.. automethod:: Spotify.saved_tracks_delete

Personalisation API
-------------------
.. autosummary::
   :nosignatures:

   Spotify.current_user_top_artists
   Spotify.current_user_top_tracks

.. automethod:: Spotify.current_user_top_artists
.. automethod:: Spotify.current_user_top_tracks

Player API
----------
.. autosummary::
   :nosignatures:

   Spotify.playback
   Spotify.playback_currently_playing
   Spotify.playback_devices
   Spotify.playback_next
   Spotify.playback_pause
   Spotify.playback_previous
   Spotify.playback_queue_add
   Spotify.playback_recently_played
   Spotify.playback_repeat
   Spotify.playback_resume
   Spotify.playback_seek
   Spotify.playback_shuffle
   Spotify.playback_start_context
   Spotify.playback_start_tracks
   Spotify.playback_transfer
   Spotify.playback_volume

.. automethod:: Spotify.playback
.. automethod:: Spotify.playback_currently_playing
.. automethod:: Spotify.playback_devices
.. automethod:: Spotify.playback_next
.. automethod:: Spotify.playback_pause
.. automethod:: Spotify.playback_previous
.. automethod:: Spotify.playback_queue_add
.. automethod:: Spotify.playback_recently_played
.. automethod:: Spotify.playback_repeat
.. automethod:: Spotify.playback_resume
.. automethod:: Spotify.playback_seek
.. automethod:: Spotify.playback_shuffle
.. automethod:: Spotify.playback_start_context
.. automethod:: Spotify.playback_start_tracks
.. automethod:: Spotify.playback_transfer
.. automethod:: Spotify.playback_volume

Playlist API
------------
.. autosummary::
   :nosignatures:

   Spotify.playlist
   Spotify.playlist_change_details
   Spotify.playlist_cover_image
   Spotify.playlist_cover_image_upload
   Spotify.playlist_create
   Spotify.playlist_tracks
   Spotify.playlist_tracks_add
   Spotify.playlist_tracks_clear
   Spotify.playlist_tracks_remove
   Spotify.playlist_tracks_remove_indices
   Spotify.playlist_tracks_remove_occurrences
   Spotify.playlist_tracks_reorder
   Spotify.playlist_tracks_replace
   Spotify.playlists

.. automethod:: Spotify.playlist
.. automethod:: Spotify.playlist_change_details
.. automethod:: Spotify.playlist_cover_image
.. automethod:: Spotify.playlist_cover_image_upload
.. automethod:: Spotify.playlist_create
.. automethod:: Spotify.playlist_tracks
.. automethod:: Spotify.playlist_tracks_add
.. automethod:: Spotify.playlist_tracks_clear
.. automethod:: Spotify.playlist_tracks_remove
.. automethod:: Spotify.playlist_tracks_remove_indices
.. automethod:: Spotify.playlist_tracks_remove_occurrences
.. automethod:: Spotify.playlist_tracks_reorder
.. automethod:: Spotify.playlist_tracks_replace
.. automethod:: Spotify.playlists

Search API
----------
.. automethod:: Spotify.search

.. _client-show:

Show API
--------
.. autosummary::
   :nosignatures:

   Spotify.show
   Spotify.show_episodes
   Spotify.shows

.. automethod:: Spotify.show
.. automethod:: Spotify.show_episodes
.. automethod:: Spotify.shows

Track API
---------
.. autosummary::
   :nosignatures:

   Spotify.track
   Spotify.track_audio_analysis
   Spotify.track_audio_features
   Spotify.tracks
   Spotify.tracks_audio_features

.. automethod:: Spotify.track
.. automethod:: Spotify.track_audio_analysis
.. automethod:: Spotify.track_audio_features
.. automethod:: Spotify.tracks
.. automethod:: Spotify.tracks_audio_features

User API
--------
.. autosummary::
   :nosignatures:

   Spotify.current_user
   Spotify.user

.. automethod:: Spotify.current_user
.. automethod:: Spotify.user
