.. _release-notes:
.. currentmodule:: tekore

Release notes
=============
6.1.0 (2025-12-14)
------------------
Changed
*******
- Remove support for Python 3.9 (:issue:`343`)
- Add support for Python 3.14 (:issue:`343`)

Tooling
*******
- Address deprecations in build (:issue:`342`)

6.0.0 (2024-12-11)
------------------
Changed
*******
- Remove support for Python 3.8 (:issue:`329`)
- Document newly restricted endpoints (:issue:`331`)

Added
*****
- Add and modernise typing especially for lists and dicts (:issue:`330`)
- Explicitly support and test Python 3.13 (:issue:`329`)
- Add support for HTTPX ``0.28`` (:issue:`336`)

Fixed
*****
- Avoid constructing query params manually (:issue:`332`)
- Fix :class:`RetryingSender` to not return ``None``` in
  complex retry scenarios (:issue:`333`)
- Convert :class:`Response` headers to dicts in :class:`SyncSender`
  and :class:`AsyncSender` (:issue:`339`)
- Improve messages in :func:`prompt_for_user_token` and
  :func:`prompt_for_pkce_token` (:issue:`340`)

5.5.1 (2024-09-09)
------------------
Fixed
*****
- Allow for missing ``preview_url`` in :class:`Track <model.Track>`
  (:issue:`326`)
- Add missing undocumented ``is_playable`` to
  :class:`FullAudiobook <model.FullAudiobook>` (:issue:`327`)
- Make ``resume_point`` of :class:`Chapter <model.Chapter>`
  optional (:issue:`328`)

5.5.0 (2024-07-04)
------------------
Fixed
*****
- Add `ugc_image_upload` to required scopes of
  :meth:`SpotifyPlaylistModify.playlist_cover_image_upload` (:issue:`324`)
- Make ``available_markets`` of :class:`Show <model.Show>`,
  :class:`LocalAlbum <model.LocalAlbum>` and
  :class:`LocalTrack <model.LocalTrack>` optional (:issue:`323`)

Added
*****
- Add ``open_browser`` option to
  :meth:`prompt_for_user_token <prompt_for_user_token>` and
  :meth:`prompt_for_pkce_token <prompt_for_pkce_token>` (:issue:`325`)

5.4.0 (2024-02-27)
------------------
Fixed
*****
- Add ``ep`` as a valid enum to :class:`AlbumType <model.AlbumType>`
  for top tracks API responses (:issue:`318`)
- Add undocumented ``smart_shuffle`` to :class:`CurrentlyPlayingContext
  <model.CurrentlyPlayingContext>` (:issue:`320`)

Added
*****
- Support HTTPX ``0.27`` (:issue:`317`)

5.3.1 (2024-01-28)
------------------
Fixed
*****
- :ref:`reference`: remove methods ``playlist_remove_indices`` and
  ``playlist_remove_occurrences``, which were removed from the API
  (:issue:`315`)

5.3.0 (2023-12-22)
------------------
Fixed
*****
- Make ``images`` optional in :class:`Playlist <model.Playlist>`
  to fix getting empty playlists without an image (:issue:`309`)
- Add undocumented ``dict`` to types of ``publisher`` in
  :class:`Show <model.Show>` (:issue:`310`)
- Make ``is_playable`` in :class:`Episode <model.Episode>` optional
  despite API specifications (:issue:`310`)
- Make deprecated ``language`` optional in :class:`Episode <model.Episode>`
  pending removal (:issue:`310`)
- Add undocumented ``dict`` to types of ``duration_ms`` in
  :class:`LocalTrack <model.LocalTrack>` (:issue:`310`)
- Add undocumented ``available_markets`` to
  :class:`FullPlaylistEpisode <model.FullPlaylistEpisode>` (:issue:`310`)

Added
*****
- Add ``restrictions`` to :class:`FullEpisode <model.FullEpisode>`
  (:issue:`310`)
- Support HTTPX ``0.26`` (:issue:`311`)
- Improve ``UnknownModelAttributeWarning`` to include model name (:issue:`313`)

5.2.1 (2023-11-22)
------------------
Fixed
*****
- Exclude Pydantic versions ``2.5.0`` and ``2.5.1`` (:issue:`306`)
- Add missing ``available_markets`` to :class:`FullChapter <model.FullChapter>`
  (:issue:`308`)

5.2.0 (2023-11-05)
------------------
Fixed
*****
- Add undocumented ``is_externally_hosted`` attribute to
  :class:`Audiobook <model.Audiobook>` (:issue:`302`)
- Make ``audio_preview_url`` of :class:`Episode <model.Device>` optional
  (:issue:`305`)

Added
*****
- Add support for short URLs as :func:`is_short_link` and
  :meth:`follow_short_link <Spotify.follow_short_link>` (:issue:`301`)

5.1.1 (2023-10-14)
------------------
Fixed
*****
- Make :class:`Album <model.Album>` optional (:issue:`300`)

5.1.0 (2023-10-04)
------------------
Added
*****
- Support HTTPX ``0.25`` (:issue:`294`)

Fixed
*****
- Remove misleading documentation on models (:issue:`295`)
- Add missing ``supports_volume`` to :class:`Device <model.Device>`
  (:issue:`296`)
- Exclude Pydantic version ``2.4.0`` (:issue:`297`)

5.0.1 (2023-07-06)
------------------
Fixed
*****
- Add missing ``Optional`` annotations to support Pydantic 2 (:issue:`293`)

5.0.0 (2023-06-18)
------------------
Tekore 5 comes with an overhauled response model system based on Pydantic.
Although the underlying change is major, the primary usage of models remains
unchanged. The new models are more robust and easier to maintain.
However, with more careful data validation new issues may arise. Please submit
them on `GitHub <https://github.com/felix-hilden/tekore/issues>`_.

Changed
*******
- Remove support for Python 3.7 (EOL) (:issue:`292`)
- Use Pydantic in response models (:issue:`279`)

  * Many type hints are fixed and improved.
  * Instead of retaining unknown response attributes, they are now discarded.
    However, the same warning message is raised.
  * ``.json`` and ``.asbuiltin`` methods are replaced by Pydantic models'
    ``.json`` and ``.dict``.
  * Models use the builtin ``datetime`` object directly.
  * ``.pprint`` and custom ``__repr__`` are removed in favor of using
    Pydantic's own machinery.
  * The builtin list class is used everywhere instead of the old ``ModelList``.

4.6.1 (2023-05-25)
------------------
Fixed
*****
- :class:`FullAlbum <model.FullAlbum>` - remove "album_group" attribute
  introduced in version 4.6.0 (:issue:`291`)

4.6.0 (2023-04-12)
------------------
Added
*****
- Make enumerations case insensitive (:issue:`285`)
- Support HTTPX 0.24 (:issue:`289`)

Fixed
*****
- :class:`FullChapter <model.FullChapter>` /
  :class:`SimpleChapter <model.SimpleChapter>` - change "restriction" to
  "restrictions" (:issue:`286`)
- :class:`FullAlbum <model.FullAlbum>` - add undocumented "album_group"
  attribute (:issue:`287`)

4.5.0 (2022-11-06)
------------------
Added
*****
- :ref:`errors` - carry scope information with :class:`Unauthorised`
  (:issue:`276`)
- :ref:`client` - add new audiobook (:ref:`client-audiobook`) and chapter
  :ref:`client-chapter` endpoints and "audiobook" as a valid search type. Note
  that audiobooks are currently only available in the US market. The APIs also
  seem to be unreliable. (:issue:`277`)
- :ref:`client` - add new get queue endpoint
  :meth:`playback_queue <Spotify.playback_queue>`. Queue results seem
  inconsistent at this time. (:issue:`278`)

Fixed
*****
- :ref:`models` - add missing "minute" resolution to
  :class:`ReleaseDatePrecision <model.ReleaseDatePrecision>` (:issue:`277`)
- :ref:`models` - parse response models safely everywhere (:issue:`280`)
- :ref:`client` - fix chunking of empty inputs (:issue:`281`)

4.4.1 (2022-10-08)
------------------
Fixed
*****
- Handle changed response to fix paging at search limit (:issue:`275`)

4.4.0 (2022-05-24)
------------------
Added
*****
- Dependency to HTTPX upgraded to include version ``0.23.*`` (:issue:`272`)
- Declare support for Python 3.10 (:issue:`273`)

4.3.0 (2022-03-11)
------------------
Added
*****
- Dependency to HTTPX upgraded to include version ``0.22.*`` (:issue:`267`)
- Expose the underlying credentials manager in :class:`RefreshingCredentials`
  and :class:`RefreshingToken` to facilitate closing their HTTP client, which
  is no longer closed by default as of HTTPX version ``0.22`` (:issue:`267`)

Fixed
*****
- Add missing context "collection" to :class:`ContextType <model.ContextType>`
  for playing saved tracks (:issue:`270`)

4.2.0 (2022-01-19)
------------------
Added
*****
- :ref:`conversions` - add ``user`` as a valid ID type and URL-encode hashes
  of user IDs in :func:`to_url` (:issue:`266`)

Fixed
*****
- URL-encode hashes in user IDs in :meth:`user <Spotify.user>` (:issue:`266`)

4.1.0 (2021-11-20)
------------------
- Dependency to HTTPX upgraded to include versions ``0.20.0-0.21.*``
  (:issue:`263`, :issue:`265`)

4.0.0 (2021-09-09)
------------------
Tekore 4.0 is a maintenance release to prepare for the nearly deprecated
Python 3.6, update dependencies and improve backwards compatibility.

Changed
*******
- Removed Python 3.6 support and its conditional dependencies (:issue:`252`)
- Dependency to HTTPX upgraded to include versions
  from ``0.15`` to ``0.19.*`` (:issue:`250`, :issue:`261`)
- Add fields to :class:`Request` and change their meaning to be in line with
  the new HTTPX interface (:issue:`250`)

Added
*****
- Improved documentation for type hints and response models (:issue:`109`)
- Responses can now parse unknown attributes, greatly improving backwards
  compatibility. :class:`UnknownModelAttributeWarning
  <tekore.model.UnknownModelAttributeWarning>` was introduced (:issue:`247`)

3.7.1 (2021-05-04)
------------------
Fixed
*****
- :ref:`models` - add missing but undocumented ``html_description``
  field to :class:`FullShow <model.FullShow>` and
  :class:`SimpleShow <model.SimpleShow>` (:issue:`251`)
- :ref:`models` - require the newly documented ``html_description``
  field in :class:`FullEpisode <model.FullEpisode>` and
  :class:`SimpleEpisode <model.SimpleEpisode>` (:issue:`251`)

3.7.0 (2021-04-08)
------------------
Added
*****
- :ref:`client` - add the new market API (:issue:`249`)
- :ref:`client` - add episode endpoints to library API, and the corresponding
  :class:`SavedEpisode <model.SavedEpisode>` and
  :class:`SavedEpisodePaging <model.SavedEpisodePaging>` models (:issue:`249`)

3.6.2 (2021-03-23)
------------------
Fixed
*****
- :ref:`models` - add missing but undocumented ``html_description``
  field to :class:`FullEpisode <model.FullEpisode>` and
  :class:`SimpleEpisode <model.SimpleEpisode>` (:issue:`246`)

3.6.1 (2021-03-07)
------------------
Fixed
*****
- :ref:`auth` - allow missing scope in token responses and parse it to
  an empty :class:`Scope` (:issue:`245`)

3.6.0 (2021-03-02)
------------------
Added
*****
- :ref:`client` - make context managers async safe on Python 3.7+,
  adds a dependency to the ``contextvars`` backport for Python 3.6
  (:issue:`242`)
- Dependency to HTTPX upgraded to include version ``0.17.*`` (:issue:`243`)

3.5.1 (2021-02-12)
------------------
Fixed
*****
- :ref:`client` - document decreased limit of :meth:`search <Spotify.search>`
  total (:issue:`241`)

3.5.0 (2021-01-15)
------------------
Added
*****
- :ref:`auth` - add :attr:`streaming <scope.streaming>` and
  :attr:`app-remote-control <scope.app_remote_control>`
  as extra scopes (:issue:`237`)

Fixed
*****
- :ref:`client` - fix type hints for context managers (:issue:`239`)

3.4.2 (2020-12-14)
------------------
Fixed
*****
- :ref:`models` - fix model repr for optional lists (:issue:`233`)

3.4.1 (2020-12-04)
------------------
Fixed
*****
- :ref:`client` - document the need for at least one seed in
  :meth:`recommendations <Spotify.recommendations>` (:issue:`229`)
- :ref:`client` - match new behavior of track markets (:issue:`231`)

3.4.0 (2020-11-24)
------------------
Added
*****
- :ref:`conversions` - ignore URL parameters in :func:`from_url` (:issue:`226`)
- :ref:`conversions` - :func:`from_uri`, :func:`from_url` raise proper errors
  with entirely invalid formats, error messages were improved (:issue:`227`)

Fixed
*****
- :ref:`client` - document new behavior of track markets (:issue:`228`)

3.3.0 (2020-10-22)
------------------
Added
*****
- :ref:`config` - warning messages for missing configuration now include the
  variable name which was missing (:issue:`222`)
- :ref:`models` - improved type hints and documentation
  of potentially missing values (:issue:`221`)

Fixed
*****
- :ref:`client` - document new behavior of track markets (:issue:`217`)

3.2.0 (2020-10-16)
------------------
Added
*****
- Support Python 3.9 (:issue:`219`)
- Dependency to HTTPX upgraded to include versions ``0.15.*`` and ``0.16.*``
  (:issue:`216`)
- Error messages for :func:`parse_code_from_url`, :func:`parse_state_from_url`
  and :meth:`Credentials.pkce_user_authorisation` were improved (:issue:`218`)
- :class:`Spotify` and :ref:`senders`, both synchronous and asynchronous,
  can now be closed directly with :meth:`close <Spotify.close>` (:issue:`220`)

3.1.0 (2020-09-13)
------------------
Added
*****
- :class:`StrEnum <model.StrEnum>` - model enumerations now inherit from
  ``str``, making e.g. using it as a key for sorting possible (:issue:`214`)

Fixed
*****
- :class:`PrivateUser <model.PrivateUser>` - a birthday attribute was added.
  It is not obtainable with new tokens but is returned for old tokens that have
  the now-invalid ``user-read-birthday`` scope (:issue:`52`, :issue:`197`)

3.0.1 (2020-09-05)
------------------
Fixed
*****
- :meth:`featured_playlists <Spotify.featured_playlists>` - allow missing
  owner in :class:`Playlist <model.Playlist>` models (:issue:`212`)

3.0.0 (2020-09-03)
------------------
The next major iteration of Tekore brings fewer breaking changes than in 2.0,
but packs a number of improvements to authorisation and senders.
Most notably, PKCE is now provided as an option for user authorisation
and Requests is no longer used to perform web requests.
HTTPX, which was already in use with async, is used exclusively instead.

Added
*****
- :ref:`auth` - PKCE can be used in user authorisation, providing added
  security for public clients by removing the need to use a client secret.
  (:issue:`189`)
- :class:`UserAuth` - implement user authorisation with security checks,
  the caller simply provides the resulting URI after redirection (:issue:`207`)
- :ref:`senders` - Tekore's own :class:`Request` and :class:`Response` wrappers
  are now used in the sender interface (:issue:`139`)
- Classes now have a readable ``repr`` (:issue:`191`)
- Dependency to HTTPX upgraded to include version ``0.14.*`` (:issue:`202`)
- :func:`gen_state` - generate state for user authorisation (:issue:`207`)
- :func:`parse_state_from_url` - parse state from URL parameters (:issue:`207`)

Removed
*******
- :ref:`client-playlist` - methods for playlist tracks and
  ``episodes_as_tracks`` argument of :meth:`Spotify.playlist` deprecated in 2.0
  (:issue:`178`, :issue:`202`)
- Dependency to Requests dropped in favor of HTTPX (:issue:`139`)
- :ref:`senders` - :class:`TransientSender` and :class:`SingletonSender`
  along with their asynchronous variants were removed (:issue:`139`)
- :ref:`senders` - default sender and keyword argument options were removed
  (:issue:`139`)

Changed
*******
- :ref:`errors` - web exceptions now inherit from :class:`Exception` rather
  than the underlying HTTP library's top-level exception. They always contain
  the relevant :class:`Request` and :class:`Response` (:issue:`139`)
- :ref:`senders` - as the only concrete senders, :class:`PersistentSender` and
  :class:`AsyncPersistentSender` are now implemented in :class:`SyncSender` and
  :class:`AsyncSender`, respectively (:issue:`139`)
- :class:`CachingSender` - argument order is now in line with
  :class:`RetryingSender` (:issue:`139`)
- :ref:`senders` - clients (:class:`Spotify` and :class:`Credentials`) now
  inherit from :class:`ExtendingSender` (:issue:`139`)
- :ref:`auth` - raise a more descriptive error if secret is required
  but not provided (:issue:`210`)

Fixed
*****
- :ref:`client` - fix chunking errors that occurred when passing certain
  parameters as positional arguments (:issue:`205`)

2.1.3 (2020-08-04)
------------------
Fixed
*****
- :ref:`client` - correctly return :class:`ModelList <model.ModelList>`
  when chunking input (:issue:`196`)
- :ref:`auth` - fix error handling when response does not contain an error
  description (:issue:`199`)
- :meth:`playback <Spotify.playback>` and
  :meth:`playback_currently_playing <Spotify.playback_currently_playing>` -
  correctly handle local tracks (:issue:`200`)

2.1.2 (2020-07-21)
------------------
Fixed
*****
- :class:`FullShow <model.FullShow>` - add undocumented ``total_episodes``
  parameter, mark ``total_episodes`` of :class:`SimpleShow <model.SimpleShow>`
  undocumented (:issue:`194`)

2.1.1 (2020-07-02)
------------------
Fixed
*****
- :class:`SimpleShow <model.SimpleShow>` - add optional ``total_episodes``
  parameter (:issue:`190`)

2.1.0 (2020-05-31)
------------------
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
