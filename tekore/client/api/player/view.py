from typing import List

from tekore.client.process import single, model_list
from tekore.client.base import SpotifyBase, send_and_process
from tekore.serialise import ModelList
from tekore.model import (
    CurrentlyPlayingContext,
    CurrentlyPlaying,
    PlayHistoryPaging,
    Device
)


class SpotifyPlayerView(SpotifyBase):
    @send_and_process(single(CurrentlyPlayingContext))
    def playback(
            self,
            market: str = None
    ) -> CurrentlyPlayingContext:
        """
        Get information about user's current playback.

        Requires the user-read-playback-state or
        the user-read-currently-playing scope.

        Parameters
        ----------
        market
            an ISO 3166-1 alpha-2 country code or 'from_token'

        Returns
        -------
        CurrentlyPlayingContext
            information about current playback
        """
        return self._get('me/player', market=market)

    @send_and_process(single(CurrentlyPlaying))
    def playback_currently_playing(
            self,
            market: str = None
    ) -> CurrentlyPlaying:
        """
        Get user's currently playing track.

        Requires the user-read-playback-state scope.

        Parameters
        ----------
        market
            an ISO 3166-1 alpha-2 country code or 'from_token'

        Returns
        -------
        CurrentlyPlaying
            information about the current track playing
        """
        return self._get('me/player/currently-playing', market=market)

    @send_and_process(single(PlayHistoryPaging))
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
        return self._get(
            'me/player/recently-played',
            limit=limit,
            after=after,
            before=before
        )

    @send_and_process(model_list(Device, 'devices'))
    def playback_devices(self) -> List[Device]:
        """
        Get a user's available devices.

        Requires the user-read-playback-state scope.

        Returns
        -------
        ModelList
            list of device objects
        """
        return self._get('me/player/devices')
