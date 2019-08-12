from spotipy.client._base import SpotifyBase


class SpotifyTrack(SpotifyBase):
    def track(self, track_id: str):
        return self._get('tracks/' + track_id)

    def tracks(self, track_ids: list, market: str = 'from_token'):
        """
        Get information on multiple tracks.

        Parameters:
            - track_ids - the track IDs
            - market - An ISO 3166-1 alpha-2 country code or 'from_token'
        """
        return self._get('tracks/?ids=' + ','.join(track_ids), market=market)

    def track_audio_analysis(self, track_id: str):
        return self._get('audio-analysis/' + track_id)

    def track_audio_features(self, track_id: str):
        return self._get('audio-features/' + track_id)

    def tracks_audio_features(self, track_ids: list):
        return self._get('audio-features?ids=' + ','.join(track_ids))
