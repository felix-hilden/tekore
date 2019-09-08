from spotipy.client.base import SpotifyBase


class SpotifyTrack(SpotifyBase):
    def track(self, track_id: str):
        """
        Get information for a track.
        """
        return self._get('tracks/' + track_id)

    def tracks(self, track_ids: list, market: str = 'from_token'):
        """
        Get information for multiple tracks.

        Parameters
        ----------
        track_ids
            the track IDs
        market
            an ISO 3166-1 alpha-2 country code or 'from_token'
        """
        return self._get('tracks/?ids=' + ','.join(track_ids), market=market)

    def track_audio_analysis(self, track_id: str):
        """
        Get a detailed audio analysis for a track.

        The analysis describes the track's structure and musical content,
        including rythm, pitch and timbre.
        """
        return self._get('audio-analysis/' + track_id)

    def track_audio_features(self, track_id: str):
        """
        Get audio feature information for a track.
        """
        return self._get('audio-features/' + track_id)

    def tracks_audio_features(self, track_ids: list):
        """
        Get audio feature information for multiple tracks
        """
        return self._get('audio-features?ids=' + ','.join(track_ids))
