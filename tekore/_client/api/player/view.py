from ...process import single, model_list
from ...decor import send_and_process, maximise_limit, scopes
from ...base import SpotifyBase
from tekore._auth import scope
from tekore.model import (
    ModelList,
    CurrentlyPlayingContext,
    CurrentlyPlaying,
    PlayHistoryPaging,
    Device
)


class SpotifyPlayerView(SpotifyBase):
    """Player API endpoints that view state."""

    @scopes([scope.user_read_playback_state])
    @send_and_process(single(CurrentlyPlayingContext))
    def playback(
            self,
            market: str = None,
            tracks_only: bool = False
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
        if tracks_only is True:
            additional_types = None
        else:
            additional_types = 'episode'

        return self._get(
            'me/player',
            market=market,
            additional_types=additional_types
        )

    @scopes(
        [scope.user_read_playback_state, scope.user_read_currently_playing],
        [scope.user_read_playback_state, scope.user_read_currently_playing]
    )
    @send_and_process(single(CurrentlyPlaying))
    def playback_currently_playing(
            self,
            market: str = None,
            tracks_only: bool = False
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
        if tracks_only is True:
            additional_types = None
        else:
            additional_types = 'episode'

        return self._get(
            'me/player/currently-playing',
            market=market,
            additional_types=additional_types
        )

    @scopes([scope.user_read_recently_played])
    @send_and_process(single(PlayHistoryPaging))
    @maximise_limit(50)
    def playback_recently_played(
            self,
            limit: int = 20,
            after: int = None,
            before: int = None
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
            'me/player/recently-played',
            limit=limit,
            after=after,
            before=before
        )

    @scopes([scope.user_read_playback_state])
    @send_and_process(model_list(Device, 'devices'))
    def playback_devices(self) -> ModelList[Device]:
        """Get a user's available devices."""
        return self._get('me/player/devices')
