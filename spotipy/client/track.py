from spotipy.client.base import SpotifyBase
from spotipy.serialise import ModelList
from spotipy.model import FullTrack, AudioFeatures, AudioAnalysis


class SpotifyTrack(SpotifyBase):
    def track(
            self,
            track_id: str,
            market: str = None
    ) -> FullTrack:
        """
        Get information for a track.

        Parameters
        ----------
        track_id
            track ID
        market
            an ISO 3166-1 alpha-2 country code or 'from_token'

        Returns
        -------
        FullTrack
            track object
        """
        json = self._get('tracks/' + track_id, market=market)
        return FullTrack(**json)

    def tracks(
            self,
            track_ids: list,
            market: str = None
    ) -> ModelList:
        """
        Get information for multiple tracks.

        Parameters
        ----------
        track_ids
            the track IDs
        market
            an ISO 3166-1 alpha-2 country code or 'from_token'

        Returns
        -------
        ModelList
            list of track objects
        """
        json = self._get('tracks/?ids=' + ','.join(track_ids), market=market)
        return ModelList(FullTrack(**t) for t in json['tracks'])

    def track_audio_analysis(self, track_id: str) -> AudioAnalysis:
        """
        Get a detailed audio analysis for a track.

        The analysis describes the track's structure and musical content,
        including rythm, pitch and timbre.

        Returns
        -------
        AudioAnalysis
            audio analysis
        """
        json = self._get('audio-analysis/' + track_id)
        return AudioAnalysis(**json)

    def track_audio_features(self, track_id: str) -> AudioFeatures:
        """
        Get audio feature information for a track.

        Returns
        -------
        AudioFeatures
            audio features object
        """
        json = self._get('audio-features/' + track_id)
        return AudioFeatures(**json)

    def tracks_audio_features(self, track_ids: list) -> ModelList:
        """
        Get audio feature information for multiple tracks.

        Feature information for a track may be ``None`` if not available.

        Returns
        -------
        ModelList
            list of audio features objects
        """
        json = self._get('audio-features?ids=' + ','.join(track_ids))
        return ModelList(
            AudioFeatures(**a) if a is not None else None
            for a in json['audio_features']
        )
