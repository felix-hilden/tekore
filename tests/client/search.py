import pytest

from tekore import HTTPError


@pytest.mark.api
class TestSpotifySearch:
    def test_search(self, app_client):
        (tracks,) = app_client.search("sheeran")
        assert tracks.total > 0

    def test_search_below_limit_succeeds(self, app_client):
        app_client.search("piano", types=("playlist",), limit=1, offset=999)

    def test_search_beyond_limit_raises(self, app_client):
        with pytest.raises(HTTPError):
            app_client.search("piano", types=("playlist",), limit=1, offset=1000)

    def test_search_shows(self, app_client):
        (shows,) = app_client.search("sleep", types=("show",), market="US", limit=1)
        assert shows.total > 0

    def test_search_episodes(self, app_client):
        (episodes,) = app_client.search(
            "piano", types=("episode",), market="US", limit=1
        )
        assert episodes.total > 0

    def test_search_audiobooks(self, app_client):
        (audiobooks,) = app_client.search(
            "book", types=("audiobook",), market="US", limit=1
        )
        assert audiobooks.total > 0
