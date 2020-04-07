Release notes
=============
1.6.0 (2020-04-07)
------------------
Added
*****
- Support for podcasts: new APIs for
  :class:`episodes <tekore.client.api.SpotifyEpisode>`
  and :class:`shows <tekore.client.api.SpotifyShow>`.
  New :class:`scope <tekore.scope.AuthorisationScopes>`
  ``user-read-playback-position`` for returning episode resume points.
  New endpoints for saving shows in
  :class:`library <tekore.client.api.SpotifyLibrary>`.
  :meth:`playback_queue_add <tekore.client.api.SpotifyPlayer.playback_queue_add>`
  now accepts episode URIs.
  :meth:`playback <tekore.client.api.SpotifyPlayer.playback>` and
  :meth:`playback_currently_playing <tekore.client.api.SpotifyPlayer.playback_currently_playing>`
  can return currently playing episodes and shows.
  :meth:`playlist <tekore.client.api.SpotifyPlaylist.playlist>` and
  :meth:`playlist_tracks <tekore.client.api.SpotifyPlaylist.playlist_tracks>`
  can return episodes on playlists.
  :meth:`search <tekore.client.api.SpotifySearch.search>` allows for searching
  episodes and shows.
  (:issue:`164`)
- Dependency to HTTPX upgraded to include version ``0.12.*`` (:issue:`166`)

Fixed
*****
- Errors are now correctly raised when parsing responses in
  :meth:`playlist <tekore.client.api.SpotifyPlaylist.playlist>` and
  :meth:`playlist_tracks <tekore.client.api.SpotifyPlaylist.playlist_tracks>`
  (:issue:`164`)
- Conversions :func:`to_url <tekore.convert.to_url>` now return URLs with
  prefix ``https`` instead of ``http``, in line with API and application
  behavior. :func:`from_url <tekore.convert.from_url>` now correctly
  accepts ``https`` addresses for conversion. (:issue:`165`)
- The ``repr`` of local items can now be produced without errors (:issue:`171`)

1.5.0 (2020-03-11)
------------------
Added
*****
- :class:`RetryingSender <tekore.sender.RetryingSender>`
  avoid unnecessary retries and reduce total wait time (:issue:`163`)

Fixed
*****
- :meth:`category_playlists <tekore.client.api.SpotifyBrowse.category_playlists>`
  require category parameter (:issue:`160`)
- :class:`AsyncPersistentSender <tekore.sender.AsyncPersistentSender>`
  persist connections appropriately (:issue:`161`)
- :meth:`playback_queue_add <tekore.client.api.SpotifyPlayer.playback_queue_add>`
  match endpoint address to changed API (:issue:`162`)

1.4.0 (2020-03-02)
------------------
Added
*****
- :meth:`playlist_tracks_clear <tekore.client.api.SpotifyPlaylist.playlist_tracks_clear>`
  convenience endpoint for deleting tracks from a playlist (:issue:`155`)
- :mod:`convert <tekore.convert>`
  accept shows and episodes as valid types (:issue:`159`)

Fixed
*****
- :meth:`playlist_tracks_add <tekore.client.api.SpotifyPlaylist.playlist_tracks_add>`
  insert tracks in correct order when chunking (:issue:`156`)

1.3.0 (2020-02-26)
------------------
Added
*****
- :meth:`playback_queue_add <tekore.client.api.SpotifyPlayer.playback_queue_add>`
  add tracks to queue (:issue:`152`)
- :mod:`serialise <tekore.serialise>`
  readable ``repr`` for response models (:commit:`32911c3a`)
- :class:`CachingSender <tekore.sender.CachingSender>`
  option to specify maximum cache size (:issue:`143`)
- :mod:`client <tekore.client>`
  optionally send long lists of resources as chunks (:issue:`153`)

1.2.0 (2020-02-17)
------------------
Added
*****
- :mod:`client <tekore.client>`
  optionally use maximum limits by default in all paging calls (:issue:`66`)

Fixed
*****
- :mod:`paging <tekore.client.paging.SpotifyPaging>` all items or
  pages of a :meth:`search <tekore.client.api.SpotifySearch.search>`
  respects API limits (:issue:`145`)
- :mod:`paging <tekore.client.paging.SpotifyPaging>`
  always return an awaitable when asynchronous (:issue:`146`)

1.1.0 (2020-02-02)
------------------
Added
*****
- Async support in authentication and API endpoints (:issue:`131`)
- :class:`CachingSender <tekore.sender.CachingSender>`
  a sender for response caching (:issue:`4`)
- :mod:`config <tekore.util.config>`
  reading missing values produces a warning (:commit:`0fa61801`)

Fixed
*****
- :meth:`playlist <tekore.client.api.SpotifyPlaylist.playlist>`
  parse correctly when fields is specified (:issue:`142`)

1.0.1 (2020-01-17)
------------------
Fixed
*****
- :class:`PlaylistTrack <tekore.model.playlist.PlaylistTrack>`
  accept missing video thumbnail (:issue:`132`)

1.0.0 (2020-01-14)
------------------
- Packaging improvements
- Declare versioning scheme

0.1.0 (2020-01-14)
------------------
Initial release of Tekore!