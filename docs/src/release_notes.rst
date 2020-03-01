Release notes
=============
Unreleased
----------
Added
*****
- :meth:`playlist_tracks_clear <tekore.client.api.SpotifyPlaylist.playlist_tracks_clear>`
  convenience endpoint for deleting tracks from a playlist (:issue:`155`)

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