.. _release-notes:
.. currentmodule:: tekore

Release notes
=============
Unreleased
----------
Added
*****
- :ref:`client` - required and optional scopes can now be determined in code
  for any endpoint of the client (:issue:`180`)
- Dependency to HTTPX upgraded to include version ``0.13.*`` (:issue:`186`)

Fixed
*****
- :ref:`errors` - correctly fall back to :class:`ClientError` and
  :class:`ServerError` when encountering an unknown status code (:issue:`185`)

2.0.0 (2020-05-27)
------------------
This release significantly improves the overall structure of the library
and provides quality of life enhancements to various tasks.
Most notably, submodules were removed in favor of a flat structure.
Everything is now imported from the top level
with the exception of :ref:`models`.

Removed
*******
- Importing from submodules (:issue:`81`)
- :class:`OAuthError` in :ref:`auth` - see below for details (:issue:`154`)

Deprecated
**********
- :ref:`client-playlist` - methods specifically for playlist tracks
  and ``episodes_as_tracks`` argument of :meth:`Spotify.playlist`
  (:issue:`178`)

Added
*****
- :ref:`auth` - a list of :class:`scopes <scope>` and strings is accepted
  in `scope` arguments (:issue:`81`)
- :class:`Scope` operations were expanded to properly handle all combinations
  of :class:`str`, :class:`scope` and :class:`Scope` (:issue:`177`)
- :ref:`client-playlist` - new methods to fully support episodes in playlists.
  The new endpoints are direct counterparts to ``playlist_tracks_*`` methods.
  (:issue:`178`)

Changed
*******
Import structure
~~~~~~~~~~~~~~~~
Submodules were removed in favor of a flat structure.
In addition to simply relocating objects, some changes were made as well.
(:issue:`81`)

- Options for :ref:`senders` and :ref:`config` are now set at the top level
- :class:`AuthorisationScopes` was renamed to :class:`scope`, and its alias
  `scopes` is no longer available
- Ready-made :ref:`scopes <auth-scopes>` `read`, `write` and `every` are now
  accessed via the :class:`scope` enumeration

Response models
~~~~~~~~~~~~~~~
These changes aim to make :ref:`models` consistent
and serialisation clear. (:issue:`149`)

- The JSON encoder used internally was made private
- Hierarchies and names of model base classes and member types changed
- Instead of using ``str``, models are now converted to JSON using their
  :meth:`json <model.Serialisable.json>` method
- As a result of the change above, the ``repr`` of models can be viewed simply
  with ``print``. The ``repr`` of model lists was significantly improved.
  Viewing attributes of models produces consistent results.
- The :meth:`asbuiltin <model.Serialisable.asbuiltin>` method
  replaces :meth:`asdict` for models and was also added for lists of models.
  Enumerations and timestamps are no longer preserved in the conversion.
- :meth:`pprint <model.Serialisable.pprint>` output is now compact by default

Playlist items
~~~~~~~~~~~~~~
Boolean attributes of :class:`FullTrack <model.FullTrack>` and
:class:`FullEpisode <model.FullEpisode>` on a playlist were previously also
available elsewhere, but had :class:`None` values. They were removed.
The booleans are still available in playlist-related calls with the new
:class:`FullPlaylistTrack <model.FullPlaylistTrack>` and
:class:`FullPlaylistEpisode <model.FullPlaylistEpisode>`.
:class:`LocalPlaylistTrack <model.LocalPlaylistTrack>` now also provides
these booleans. (:issue:`170`)

Miscellaneous
~~~~~~~~~~~~~
- Exceptions thrown in :ref:`auth` now match :ref:`client`.
  Because of that, :class:`OAuthError` was removed.
  :ref:`errors` now inherit from a common base class. (:issue:`154`)
- :attr:`Token.scope` and :class:`RefreshingToken.scope` now return
  a :class:`Scope` instead of a string. (:issue:`177`)
- Default :ref:`sender <senders>` changed from :class:`TransientSender` to
  :class:`PersistentSender`, also affects :class:`Client` behavior
  (:issue:`141`)

Fixed
*****
- Properly close sessions in :class:`PersistentSender` (:issue:`179`)
- Members of :class:`AlbumGroup <model.AlbumGroup>` are now strings
  as intended, rather than one-element tuples (:issue:`181`)
- Include readme to source distributions to fix setup (:issue:`182`)

1.7.0 (2020-04-28)
------------------
Added
*****
- Most imports can be done directly at the top level (:issue:`174`)

Deprecated
**********
- Importing from submodules, removed in Tekore 2.0 (:issue:`81`)

Fixed
*****
- :meth:`recommendations <Spotify.recommendations>` documentation changed to
  reflect that only IDs are accepted as seeds, not URIs or URLs (:issue:`173`)
- :meth:`track_audio_analysis <Spotify.track_audio_analysis>`
  allow for missing attributes in analysis (:issue:`175`)

1.6.0 (2020-04-07)
------------------
Added
*****
- :ref:`client` - Support for podcasts. New APIs for
  :ref:`episodes <client-episode>` and :ref:`shows <client-show>`.
  New :class:`scope` ``user-read-playback-position``
  for returning episode resume points.
  New endpoints for saving shows in a user's :ref:`library <client-library>`.
  :meth:`playback_queue_add <Spotify.playback_queue_add>` now accepts episodes.
  :meth:`playback <Spotify.playback>` and
  :meth:`playback_currently_playing <Spotify.playback_currently_playing>`
  can return currently playing episodes and shows.
  :meth:`playlist <Spotify.playlist>` and
  :meth:`playlist_tracks <Spotify.playlist_tracks>`
  can return episodes on playlists.
  :meth:`search <Spotify.search>` allows for searching episodes and shows.
  (:issue:`164`)
- Dependency to HTTPX upgraded to include version ``0.12.*`` (:issue:`166`)

Fixed
*****
- Errors are now correctly raised when parsing responses in
  :meth:`playlist <Spotify.playlist>` and
  :meth:`playlist_tracks <Spotify.playlist_tracks>` (:issue:`164`)
- Conversions :func:`to_url` now return URLs with prefix ``https`` instead of
  ``http``, in line with API and application behavior. :func:`from_url` now
  correctly accepts ``https`` addresses for conversion. (:issue:`165`)
- :ref:`models` - The ``repr`` of local items can now be produced without
  errors (:issue:`171`)

1.5.0 (2020-03-11)
------------------
Added
*****
- :class:`RetryingSender` -
  avoid unnecessary retries and reduce total wait time (:issue:`163`)

Fixed
*****
- :meth:`category_playlists <Spotify.category_playlists>`
  require category parameter (:issue:`160`)
- :class:`AsyncPersistentSender` -
  persist connections appropriately (:issue:`161`)
- :meth:`playback_queue_add <Spotify.playback_queue_add>`
  match endpoint address to changed API (:issue:`162`)

1.4.0 (2020-03-02)
------------------
Added
*****
- :meth:`playlist_tracks_clear <Spotify.playlist_tracks_clear>` -
  convenience endpoint for deleting tracks from a playlist (:issue:`155`)
- :ref:`conversions` - accept shows and episodes as valid types (:issue:`159`)

Fixed
*****
- :meth:`playlist_tracks_add <Spotify.playlist_tracks_add>` -
  insert tracks in correct order when chunking (:issue:`156`)

1.3.0 (2020-02-26)
------------------
Added
*****
- :meth:`playback_queue_add <Spotify.playback_queue_add>` -
  add tracks to queue (:issue:`152`)
- :ref:`models` - readable ``repr`` for models (:commit:`32911c3a`)
- :class:`CachingSender` - option to specify maximum cache size (:issue:`143`)
- :ref:`client` - optionally send long lists of resources as chunks
  circumventing API limits (:issue:`153`)

1.2.0 (2020-02-17)
------------------
Added
*****
- :ref:`client` - optionally use maximum limits in all paging calls
  (:issue:`66`)

Fixed
*****
- :ref:`client-paging` - respect API limits when retrieving all items or pages
  of a :meth:`search <Spotify.search>` (:issue:`145`)
- :ref:`client-paging` - always return an awaitable when asynchronous
  (:issue:`146`)

1.1.0 (2020-02-02)
------------------
Added
*****
- Async support in authentication and API endpoints (:issue:`131`)
- :class:`CachingSender` - a sender for response caching (:issue:`4`)
- :ref:`config` - reading missing values produces a warning
  (:commit:`0fa61801`)

Fixed
*****
- :meth:`playlist <Spotify.playlist>` -
  parse correctly when fields is specified (:issue:`142`)

1.0.1 (2020-01-17)
------------------
Fixed
*****
- :class:`PlaylistTrack <model.PlaylistTrack>` -
  accept missing video thumbnail (:issue:`132`)

1.0.0 (2020-01-14)
------------------
- Packaging improvements
- Declare versioning scheme

0.1.0 (2020-01-14)
------------------
Initial release of Tekore!
