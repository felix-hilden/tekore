from typing import Union

from tekore.model import RepeatState
from tekore.convert import to_uri
from tekore.client.base import SpotifyBase


def offset_to_dict(offset: Union[int, str]):
    """
    Parse playback start offset to an appropriate payload member.

    If offset is an integer, it is an index to a track position.
    If it is a string, it is a URI of a specific track.
    """
    if isinstance(offset, int):
        return {'position': offset}
    elif isinstance(offset, str):
        return {'uri': to_uri('track', offset)}


class SpotifyPlayerModify(SpotifyBase):
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

    def playback_resume(self, device_id: str = None) -> None:
        """
        Resume user's playback.

        Requires the user-modify-playback-state scope.

        Parameters
        ----------
        device_id
            device to start playback on
        """
        self._put('me/player/play', device_id=device_id)

    def playback_start_tracks(
            self,
            track_ids: list,
            offset: Union[int, str] = None,
            position_ms: int = None,
            device_id: str = None
    ) -> None:
        """
        Start playback of one or more tracks.

        Requires the user-modify-playback-state scope.

        Parameters
        ----------
        track_ids
            track IDs to start playing
        offset
            offset into tracks by index or track ID
        position_ms
            initial position of first played track
        device_id
            device to start playback on
        """
        payload = {
            'uris': [to_uri('track', t) for t in track_ids],
            'offset': offset_to_dict(offset),
            'position_ms': position_ms,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        self._put('me/player/play', payload=payload, device_id=device_id)

    def playback_start_context(
            self,
            context_uri: str,
            offset: Union[int, str] = None,
            position_ms: int = None,
            device_id: str = None
    ) -> None:
        """
        Start playback of a context: an album, artist or playlist.

        Requires the user-modify-playback-state scope.

        Parameters
        ----------
        context_uri
            context to start playing
        offset
            offset into context by index or track ID,
            only available when context is an album or playlist
        position_ms
            initial position of first played track
        device_id
            device to start playback on
        """
        payload = {
            'context_uri': context_uri,
            'offset': offset_to_dict(offset),
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

    def playback_repeat(
            self,
            state: Union[str, RepeatState],
            device_id: str = None
    ) -> None:
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
