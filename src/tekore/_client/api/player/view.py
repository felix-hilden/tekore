from __future__ import annotations

from tekore._auth import scope
from tekore._client.base import SpotifyBase
from tekore._client.decor import maximise_limit, scopes, send_and_process
from tekore._client.process import model_list, single
from tekore.model import (
    CurrentlyPlaying,
    CurrentlyPlayingContext,
    Device,
    PlayHistoryPaging,
    Queue,
)


class SpotifyPlayerView(SpotifyBase):
    """Player API endpoints that view state."""

    @scopes([scope.user_read_playback_state])
    @send_and_process(single(CurrentlyPlayingContext))
    def playback(
        self, market: str | None = None, tracks_only: bool = False
    ) -> CurrentlyPlayingContext:
        """
        Get information about user's current playback.

        Parameters
        ----------
        market
            an ISO 3166-1 alpha-2 country code or 'from_token'
        tracks_only
            return only tracks in the currently playing item,
            if True, episodes have None as the currently playing item

        Returns
        -------
        CurrentlyPlayingContext
            information about current playback
        """
        additional_types = None if tracks_only else "episode"

        return self._get("me/player", market=market, additional_types=additional_types)

    @scopes(
        [scope.user_read_playback_state, scope.user_read_currently_playing],
        [scope.user_read_playback_state, scope.user_read_currently_playing],
    )
    @send_and_process(single(CurrentlyPlaying))
    def playback_currently_playing(
        self, market: str | None = None, tracks_only: bool = False
    ) -> CurrentlyPlaying:
        """
        Get user's currently playing track.

        Only one of the scopes above is required.

        Parameters
        ----------
        market
            an ISO 3166-1 alpha-2 country code or 'from_token'
        tracks_only
            return only tracks in the currently playing item,
            if True, episodes have None as the currently playing item

        Returns
        -------
        CurrentlyPlaying
            information about the current track playing
        """
        additional_types = None if tracks_only else "episode"

        return self._get(
            "me/player/currently-playing",
            market=market,
            additional_types=additional_types,
        )

    @scopes([scope.user_read_recently_played])
    @send_and_process(single(PlayHistoryPaging))
    @maximise_limit(50)
    def playback_recently_played(
        self, limit: int = 20, after: int | None = None, before: int | None = None
    ) -> PlayHistoryPaging:
        """
        Get tracks from the current user's recently played tracks.

        Only ``after`` or ``before`` should be specified at one time.

        Parameters
        ----------
        limit
            the number of items to return (1..50)
        after
            a unix timestamp in milliseconds, must not be specified with 'before'
        before
            a unix timestamp in milliseconds, must not be specified with 'after'
        """
        return self._get(
            "me/player/recently-played", limit=limit, after=after, before=before
        )

    @scopes([scope.user_read_playback_state])
    @send_and_process(model_list(Device, "devices"))
    def playback_devices(self) -> list[Device]:
        """Get a user's available devices."""
        return self._get("me/player/devices")

    @scopes([scope.user_read_playback_state])
    @send_and_process(single(Queue))
    def playback_queue(self) -> Queue:
        """
        Get items in a user's queue.

        The result also include items in the current playback context
        even though they are not explicitly in the queue.
        The number of items in the queue is inconsistent,
        but from manual experimentation at least two items are returned.
        """
        return self._get("me/player/queue")
