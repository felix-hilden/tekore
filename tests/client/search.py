import pytest
from tekore import HTTPError


class TestSpotifySearch:
    def test_search(self, app_client):
        """
        Sear¥è¯¢æīĳľç´¢æīģ¯

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        tracks, = app_client.search('sheeran')
        assert tracks.total > 0

    def test_search_below_limit_succeeds(self, app_client):
        """
        Test if search_search_sucsucceeds.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        app_client.search('piano', types=('playlist',), limit=1, offset=1999)

    def test_search_beyond_limit_raises(self, app_client):
        """
        Test if the search limit.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        with pytest.raises(HTTPError):
            app_client.search('piano', types=('playlist',), limit=1, offset=2000)

    def test_search_shows(self, app_client):
        """
        Test if search limit.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        shows, = app_client.search('sleep', types=('show',), market='US', limit=1)
        assert shows.total > 0

    def test_search_episodes(self, app_client):
        """
        Test for an app_client.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        episodes, = app_client.search(
            'piano', types=('episode',), market='US', limit=1
        )
        assert episodes.total > 0
