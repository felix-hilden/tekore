from __future__ import annotations

from tekore._auth import scope
from tekore._client.base import SpotifyBase
from tekore._client.decor import scopes, send_and_process
from tekore._client.process import nothing
from tekore._convert import to_uri
from tekore.model import RepeatState


def offset_to_dict(offset: int | str | None) -> dict | None:
    """
    Parse playback start offset to an appropriate payload member.

    If offset is an integer, it is an index to a track position.
    If it is a string, it is a URI of a specific track.
    """
    if isinstance(offset, int):
        return {"position": offset}
    if isinstance(offset, str):
        return {"uri": to_uri("track", offset)}
    return None


class SpotifyPlayerModify(SpotifyBase):
    """Player API endpoints that modify state."""

    @scopes([scope.user_modify_playback_state])
    @send_and_process(nothing)
    def playback_transfer(self, device_id: str, force_play: bool = False) -> None:
        """
        Transfer playback to another device.

        Parameters
        ----------
        device_id
            device to transfer playback to
        force_play
            true: play after transfer, false: keep current state
        """
        payload = {"device_ids": [device_id], "play": force_play}
        return self._put("me/player", payload=payload)

    @scopes([scope.user_modify_playback_state])
    @send_and_process(nothing)
    def playback_resume(self, device_id: str | None = None) -> None:
        """
        Resume user's playback.

        Parameters
        ----------
        device_id
            device to start playback on
        """
        return self._put("me/player/play", device_id=device_id)

    @scopes([scope.user_modify_playback_state])
    @send_and_process(nothing)
    def playback_start_tracks(
        self,
        track_ids: list[str],
        offset: int | str | None = None,
        position_ms: int | None = None,
        device_id: str | None = None,
    ) -> None:
        """
        Start playback of one or more tracks.

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
            "uris": [to_uri("track", t) for t in track_ids],
            "offset": offset_to_dict(offset),
            "position_ms": position_ms,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        return self._put("me/player/play", payload=payload, device_id=device_id)

    @scopes([scope.user_modify_playback_state])
    @send_and_process(nothing)
    def playback_start_context(
        self,
        context_uri: str,
        offset: int | str | None = None,
        position_ms: int | None = None,
        device_id: str | None = None,
    ) -> None:
        """
        Start playback of a context: an album, artist or playlist.

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
            "context_uri": context_uri,
            "offset": offset_to_dict(offset),
            "position_ms": position_ms,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        return self._put("me/player/play", payload=payload, device_id=device_id)

    @scopes([scope.user_modify_playback_state])
    @send_and_process(nothing)
    def playback_queue_add(self, uri: str, device_id: str | None = None) -> None:
        """
        Add a track or an episode to a user's queue.

        Parameters
        ----------
        uri
            resource to add, track or episode
        device_id
            devide to extend the queue on
        """
        return self._post("me/player/queue", uri=uri, device_id=device_id)

    @scopes([scope.user_modify_playback_state])
    @send_and_process(nothing)
    def playback_pause(self, device_id: str | None = None) -> None:
        """
        Pause a user's playback.

        Parameters
        ----------
        device_id
            device to pause playback on
        """
        return self._put("me/player/pause", device_id=device_id)

    @scopes([scope.user_modify_playback_state])
    @send_and_process(nothing)
    def playback_next(self, device_id: str | None = None) -> None:
        """
        Skip user's playback to next track.

        Parameters
        ----------
        device_id
            device to skip track on
        """
        return self._post("me/player/next", device_id=device_id)

    @scopes([scope.user_modify_playback_state])
    @send_and_process(nothing)
    def playback_previous(self, device_id: str | None = None) -> None:
        """
        Skip user's playback to previous track.

        Parameters
        ----------
        device_id
            device to skip track on
        """
        return self._post("me/player/previous", device_id=device_id)

    @scopes([scope.user_modify_playback_state])
    @send_and_process(nothing)
    def playback_seek(self, position_ms: int, device_id: str | None = None) -> None:
        """
        Seek to position in current playing track.

        Parameters
        ----------
        position_ms
            position on track
        device_id
            device to seek on
        """
        return self._put("me/player/seek", position_ms=position_ms, device_id=device_id)

    @scopes([scope.user_modify_playback_state])
    @send_and_process(nothing)
    def playback_repeat(
        self, state: str | RepeatState, device_id: str | None = None
    ) -> None:
        """
        Set repeat mode for playback.

        Parameters
        ----------
        state
            `track`, `context`, or `off`
        device_id
            device to set repeat on
        """
        return self._put("me/player/repeat", state=str(state), device_id=device_id)

    @scopes([scope.user_modify_playback_state])
    @send_and_process(nothing)
    def playback_shuffle(self, state: bool, device_id: str | None = None) -> None:
        """
        Toggle shuffle for user's playback.

        Parameters
        ----------
        state
            shuffle state
        device_id
            device to toggle shuffle on
        """
        state_arg = "true" if state else "false"
        return self._put("me/player/shuffle", state=state_arg, device_id=device_id)

    @scopes([scope.user_modify_playback_state])
    @send_and_process(nothing)
    def playback_volume(
        self, volume_percent: int, device_id: str | None = None
    ) -> None:
        """
        Set volume for user's playback.

        Parameters
        ----------
        volume_percent
            volume to set (0..100)
        device_id
            device to set volume on
        """
        return self._put(
            "me/player/volume", volume_percent=volume_percent, device_id=device_id
        )
