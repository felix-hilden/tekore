from tekore.client.process import single, model_list
from tekore.client.base import SpotifyBase, send_and_process
from tekore.serialise import ModelList
from tekore.model import FullTrack, AudioFeatures, AudioAnalysis


class SpotifyTrack(SpotifyBase):
    @send_and_process(single(FullTrack))
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
        return self._get('tracks/' + track_id, market=market)

    @send_and_process(model_list(FullTrack, 'tracks'))
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
        return self._get('tracks/?ids=' + ','.join(track_ids), market=market)

    @send_and_process(single(AudioAnalysis))
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
        return self._get('audio-analysis/' + track_id)

    @send_and_process(single(AudioFeatures))
    def track_audio_features(self, track_id: str) -> AudioFeatures:
        """
        Get audio feature information for a track.

        Returns
        -------
        AudioFeatures
            audio features object
        """
        return self._get('audio-features/' + track_id)

    @send_and_process(model_list(AudioFeatures, 'audio_features'))
    def tracks_audio_features(self, track_ids: list) -> ModelList:
        """
        Get audio feature information for multiple tracks.

        Feature information for a track may be ``None`` if not available.

        Returns
        -------
        ModelList
            list of audio features objects
        """
        return self._get('audio-features?ids=' + ','.join(track_ids))
