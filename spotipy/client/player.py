from typing import Union, List

from spotipy.client.base import SpotifyBase
from spotipy.serialise import ModelList
from spotipy.convert import to_uri
from spotipy.model import (
    CurrentlyPlayingContext,
    CurrentlyPlayingTrack,
    PlayHistoryPaging,
    Device
)


class SpotifyPlayer(SpotifyBase):
    def playback(
            self,
            market: Union[str, None] = 'from_token'
    ) -> CurrentlyPlayingContext:
        """
        Get information about user's current playback.

        Requires the user-read-playback-state or
        the user-read-currently-playing scope.

        Parameters
        ----------
        market
            None, an ISO 3166-1 alpha-2 country code or 'from_token'

        Returns
        -------
        CurrentlyPlayingContext
            information about current playback
        """
        json = self._get('me/player', market=market)
        if json is not None:
            return CurrentlyPlayingContext(**json)

    def playback_currently_playing(
            self,
            market: Union[str, None] = 'from_token'
    ) -> CurrentlyPlayingTrack:
        """
        Get user's currently playing track.

        Requires the user-read-playback-state scope.

        Parameters
        ----------
        market
            an ISO 3166-1 alpha-2 country code or 'from_token'

        Returns
        -------
        CurrentlyPlayingTrack
            information about the current track playing
        """
        json = self._get('me/player/currently-playing', market=market)
        if json is not None:
            return CurrentlyPlayingTrack(**json)

    def playback_recently_played(
            self,
            limit: int = 20,
            after: int = None,
            before: int = None
    ) -> PlayHistoryPaging:
        """
        Get tracks from the current user's recently played tracks.

        Only after or before should be specified at one time.
        Requires the user-read-recently-played scope.

        Parameters
        ----------
        limit
            the number of items to return (1..50)
        after
            a unix timestamp in milliseconds, must not be specified with 'before'
        before
            a unix timestamp in milliseconds, must not be specified with 'after'

        Returns
        -------
        PlayHistoryPaging
            cursor-based paging containing play history objects
        """
        json = self._get(
            'me/player/recently-played',
            limit=limit,
            after=after,
            before=before
        )
        return PlayHistoryPaging(**json)

    def playback_devices(self) -> List[Device]:
        """
        Get a user's available devices.

        Requires the user-read-playback-state scope.

        Returns
        -------
        ModelList
            list of device objects
        """
        json = self._get('me/player/devices')
        return ModelList(Device(**d) for d in json['devices'])

    def playback_transfer(self, device_id: str, force_play: bool = False) -> None:
        """
        Transfer playback to another device.

        Requires the user-modify-playback-state scope.
        Note that the API accepts a list of device ids,
        but only actually supports one.

        Parameters
        ----------
        device_id
            device to transfer playback to
        force_play
            true: play after transfer, false: keep current state
        """
        data = {
            'device_ids': [device_id],
            'play': force_play
        }
        self._put('me/player', payload=data)

    def playback_start(
            self,
            context_uri: str = None,
            track_ids: list = None,
            offset: Union[int, str] = None,
            position_ms: int = None,
            device_id: str = None
    ) -> None:
        """
        Start or resume user's playback.

        Requires the user-modify-playback-state scope.

        Use a `context_uri` to start playback of an album, artist, or playlist.
        Use `track_ids` to start playback of one or more tracks.
        Provide `offset` as index or track ID to start playback at some offset.
        Only available when context_uri is an album or playlist,
        or when track_ids is used.

        Parameters
        ----------
        context_uri
            context uri to play, must not be specified with track_ids
        track_ids
            track IDs, must not be specified with context_uri
        offset
            offset into context by index or track ID
        position_ms
            position of track
        device_id
            device to start playback on
        """
        if isinstance(offset, int):
            offset_dict = {'position': offset}
        elif isinstance(offset, str):
            offset_dict = {'uri': to_uri('track', offset)}
        else:
            offset_dict = None

        if track_ids is not None:
            track_uris = [to_uri('track', t) for t in track_ids]
        else:
            track_uris = None

        payload = {
            'context_uri': context_uri,
            'uris': track_uris,
            'offset': offset_dict,
            'position_ms': position_ms,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        self._put('me/player/play', payload=payload, device_id=device_id)

    def playback_pause(self, device_id: str = None) -> None:
        """
        Pause a user's playback.

        Requires the user-modify-playback-state scope.

        Parameters
        ----------
        device_id
            device to pause playback on
        """
        self._put('me/player/pause', device_id=device_id)

    def playback_next(self, device_id: str = None) -> None:
        """
        Skip user's playback to next track.

        Requires the user-modify-playback-state scope.

        Parameters
        ----------
        device_id
            device to skip track on
        """
        self._post('me/player/next', device_id=device_id)

    def playback_previous(self, device_id: str = None) -> None:
        """
        Skip user's playback to previous track.

        Requires the user-modify-playback-state scope.

        Parameters
        ----------
        device_id
            device to skip track on
        """
        self._post('me/player/previous', device_id=device_id)

    def playback_seek(self, position_ms: int, device_id: str = None) -> None:
        """
        Seek to position in current playing track.

        Requires the user-modify-playback-state scope.

        Parameters
        ----------
        position_ms
            position on track
        device_id
            device to seek on
        """
        self._put(
            'me/player/seek',
            position_ms=position_ms,
            device_id=device_id
        )

    def playback_repeat(self, state: str, device_id: str = None) -> None:
        """
        Set repeat mode for playback.

        Requires the user-modify-playback-state scope.

        Parameters
        ----------
        state
            `track`, `context`, or `off`
        device_id
            device to set repeat on
        """
        self._put('me/player/repeat', state=str(state), device_id=device_id)

    def playback_shuffle(self, state: bool, device_id: str = None) -> None:
        """
        Toggle shuffle for user's playback.

        Requires the user-modify-playback-state scope.

        Parameters
        ----------
        state
            shuffle state
        device_id
            device to toggle shuffle on
        """
        state = 'true' if state else 'false'
        self._put('me/player/shuffle', state=state, device_id=device_id)

    def playback_volume(self, volume_percent: int, device_id: str = None) -> None:
        """
        Set volume for user's playback.

        Requires the user-modify-playback-state scope.

        Parameters
        ----------
        volume_percent
            volume to set (0..100)
        device_id
            device to set volume on
        """
        self._put(
            'me/player/volume',
            volume_percent=volume_percent,
            device_id=device_id
        )
