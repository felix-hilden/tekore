.. _client:

Client
======
Web API endpoints.

.. currentmodule:: tekore

+-------------------------------+--------------------------------------+
| API summary                                                          |
+===============================+======================================+
| :ref:`client-album`           | Album information                    |
+-------------------------------+--------------------------------------+
| :ref:`client-artist`          | Artist information                   |
+-------------------------------+--------------------------------------+
| :ref:`client-audiobook`       | Audiobook information                |
+-------------------------------+--------------------------------------+
| :ref:`client-browse`          | Spotify featured catalogue           |
+-------------------------------+--------------------------------------+
| :ref:`client-chapter`         | Chapter information                  |
+-------------------------------+--------------------------------------+
| :ref:`client-episode`         | Episode information                  |
+-------------------------------+--------------------------------------+
| :ref:`client-follow`          | Follow artists, playlists and users  |
+-------------------------------+--------------------------------------+
| :ref:`client-library`         | Save (like) albums, shows and tracks |
+-------------------------------+--------------------------------------+
| :ref:`client-markets`         | Spotify market information           |
+-------------------------------+--------------------------------------+
| :ref:`client-personalisation` | User top listens                     |
+-------------------------------+--------------------------------------+
| :ref:`client-player`          | Playback operations                  |
+-------------------------------+--------------------------------------+
| :ref:`client-playlist`        | Playlist operations                  |
+-------------------------------+--------------------------------------+
| :ref:`client-search`          | Search functionality                 |
+-------------------------------+--------------------------------------+
| :ref:`client-show`            | Show information                     |
+-------------------------------+--------------------------------------+
| :ref:`client-track`           | Track information and analysis       |
+-------------------------------+--------------------------------------+
| :ref:`client-user`            | User information                     |
+-------------------------------+--------------------------------------+

Each method of the client corresponds to an API call,
with some :ref:`exceptions <client-non-endpoint>`.
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

Required and optional scopes to call any endpoint can be determined in code.
Endpoints provide ``required_scope`` and ``optional_scope``
attributes which return a :class:`Scope`.
A combination of the two is provided in ``scope``.
They can be accessed via the class itself or its instances.

.. code:: python

    scope_cls = tk.Spotify.current_user_top_tracks.scope
    scope_inst = tk.Spotify().current_user_top_tracks.scope
    assert scope_cls == scope_inst

.. autoclass:: Spotify
   :no-members:
   :no-show-inheritance:

.. _client-non-endpoint:

Non-endpoint methods
--------------------
.. autosummary::
   :nosignatures:

   Spotify.chunked
   Spotify.max_limits
   Spotify.token_as
   Spotify.follow_short_link
   is_short_link
   Spotify.send
   Spotify.close

.. automethod:: Spotify.chunked
.. automethod:: Spotify.max_limits
.. automethod:: Spotify.token_as
.. automethod:: Spotify.follow_short_link
.. autofunction:: is_short_link
.. automethod:: Spotify.send
.. automethod:: Spotify.close

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

.. _client-album:

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

.. _client-artist:

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

.. _client-audiobook:

Audiobook API
-------------
.. autosummary::
   :nosignatures:

   Spotify.audiobook
   Spotify.audiobook_chapters
   Spotify.audiobooks

.. automethod:: Spotify.audiobook
.. automethod:: Spotify.audiobook_chapters
.. automethod:: Spotify.audiobooks

.. _client-browse:

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

.. _client-chapter:

Chapter API
-----------
.. autosummary::
   :nosignatures:

   Spotify.chapter
   Spotify.chapters

.. automethod:: Spotify.chapter
.. automethod:: Spotify.chapters

.. _client-episode:

Episode API
-----------
.. autosummary::
   :nosignatures:

   Spotify.episode
   Spotify.episodes

.. automethod:: Spotify.episode
.. automethod:: Spotify.episodes

.. _client-follow:

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
   Spotify.saved_episodes
   Spotify.saved_episodes_add
   Spotify.saved_episodes_contains
   Spotify.saved_episodes_delete
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
.. automethod:: Spotify.saved_episodes
.. automethod:: Spotify.saved_episodes_add
.. automethod:: Spotify.saved_episodes_contains
.. automethod:: Spotify.saved_episodes_delete
.. automethod:: Spotify.saved_shows
.. automethod:: Spotify.saved_shows_add
.. automethod:: Spotify.saved_shows_contains
.. automethod:: Spotify.saved_shows_delete
.. automethod:: Spotify.saved_tracks
.. automethod:: Spotify.saved_tracks_add
.. automethod:: Spotify.saved_tracks_contains
.. automethod:: Spotify.saved_tracks_delete

.. _client-markets:

Markets API
-----------
.. autosummary::
   :nosignatures:

   Spotify.markets

.. automethod:: Spotify.markets

.. _client-personalisation:

Personalisation API
-------------------
.. autosummary::
   :nosignatures:

   Spotify.current_user_top_artists
   Spotify.current_user_top_tracks

.. automethod:: Spotify.current_user_top_artists
.. automethod:: Spotify.current_user_top_tracks

.. _client-player:

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
   Spotify.playback_queue
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
.. automethod:: Spotify.playback_queue
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

.. _client-playlist:

Playlist API
------------
.. autosummary::
   :nosignatures:

   Spotify.playlist
   Spotify.playlists
   Spotify.playlist_create
   Spotify.playlist_change_details
   Spotify.playlist_cover_image
   Spotify.playlist_cover_image_upload
   Spotify.playlist_items
   Spotify.playlist_add
   Spotify.playlist_clear
   Spotify.playlist_remove
   Spotify.playlist_reorder
   Spotify.playlist_replace

See Spotify's guide on `working with playlists <https://developer.spotify.com/
documentation/general/guides/working-with-playlists/>`_
for additional information.

.. automethod:: Spotify.playlist
.. automethod:: Spotify.playlists
.. automethod:: Spotify.playlist_create
.. automethod:: Spotify.playlist_change_details
.. automethod:: Spotify.playlist_cover_image
.. automethod:: Spotify.playlist_cover_image_upload
.. automethod:: Spotify.playlist_items
.. automethod:: Spotify.playlist_add
.. automethod:: Spotify.playlist_clear
.. automethod:: Spotify.playlist_remove
.. automethod:: Spotify.playlist_reorder
.. automethod:: Spotify.playlist_replace

.. _client-search:

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

.. _client-track:

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

.. _client-user:

User API
--------
.. autosummary::
   :nosignatures:

   Spotify.current_user
   Spotify.user

.. automethod:: Spotify.current_user
.. automethod:: Spotify.user
