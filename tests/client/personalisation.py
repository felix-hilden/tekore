import pytest


@pytest.mark.api
class TestSpotifyPersonalisation:
    def test_cu_top_artists(self, user_client):
        user_client.current_user_top_artists()

    def test_cu_top_tracks(self, user_client):
        user_client.current_user_top_tracks()
