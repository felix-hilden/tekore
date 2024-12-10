from __future__ import annotations

from tekore._client.base import SpotifyBase
from tekore._client.chunked import chunked, join_lists
from tekore._client.decor import scopes, send_and_process
from tekore._client.process import model_list, single
from tekore.model import AudioAnalysis, AudioFeatures, FullTrack


class SpotifyTrack(SpotifyBase):
    """Track API endpoints."""

    @scopes()
    @send_and_process(single(FullTrack))
    def track(self, track_id: str, market: str | None = None) -> FullTrack:
        """
        Get information for a track.

        Parameters
        ----------
        track_id
            track ID
        market
            an ISO 3166-1 alpha-2 country code or 'from_token'
        """
        return self._get("tracks/" + track_id, market=market)

    @scopes()
    @chunked("track_ids", 1, 50, join_lists)
    @send_and_process(model_list(FullTrack, "tracks"))
    def tracks(
        self, track_ids: list[str], market: str | None = None
    ) -> list[FullTrack]:
        """
        Get information for multiple tracks.

        Parameters
        ----------
        track_ids
            the track IDs, max 50 without chunking
        market
            an ISO 3166-1 alpha-2 country code or 'from_token'
        """
        return self._get("tracks", ids=",".join(track_ids), market=market)

    @scopes()
    @send_and_process(single(AudioAnalysis))
    def track_audio_analysis(self, track_id: str) -> AudioAnalysis:
        """
        Get a detailed audio analysis for a track.

        .. warning::

            This endpoint is unavailable to new third-party applications (:issue:`331`)

        The analysis describes the track's structure and musical content,
        including rythm, pitch and timbre.
        """
        return self._get("audio-analysis/" + track_id)

    @scopes()
    @send_and_process(single(AudioFeatures))
    def track_audio_features(self, track_id: str) -> AudioFeatures:
        """
        Get audio feature information for a track.

        .. warning::

            This endpoint is unavailable to new third-party applications (:issue:`331`)
        """
        return self._get("audio-features/" + track_id)

    @scopes()
    @chunked("track_ids", 1, 100, join_lists)
    @send_and_process(model_list(AudioFeatures, "audio_features"))
    def tracks_audio_features(self, track_ids: list[str]) -> list[AudioFeatures]:
        """
        Get audio feature information for multiple tracks.

        .. warning::

            This endpoint is unavailable to new third-party applications (:issue:`331`)

        Feature information for a track may be ``None`` if not available.

        Parameters
        ----------
        track_ids
            track IDs, max 100 without chunking
        """
        return self._get("audio-features", ids=",".join(track_ids))
