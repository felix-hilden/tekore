import pytest

from ._resources import show_id, show_ids
from tekore import HTTPError


class TestSpotifyShow:
    def test_show_not_found_without_market(self, app_client):
        """
        Show the details of a test.

        Args:
            self: (todo): write your description
            app_client: (str): write your description
        """
        with pytest.raises(HTTPError):
            app_client.show(show_id)

    def test_show_found_with_market(self, app_client):
        """
        Test if a test for a given app.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        show = app_client.show(show_id, market='FI')
        assert show.id == show_id

    def test_shows(self, app_client):
        """
        Test if a given app is already in the database.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        shows = app_client.shows(show_ids, market='FI')
        assert show_ids == [s.id for s in shows]

    def test_show_episodes(self, app_client):
        """
        Test for an application.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        episodes = app_client.show_episodes(show_id, market='FI', limit=1)
        assert episodes.items[0] is not None

    def test_show_found_without_market(self, user_client):
        """
        Test if a user s market.

        Args:
            self: (todo): write your description
            user_client: (str): write your description
        """
        show = user_client.show(show_id)
        assert show_id == show.id
