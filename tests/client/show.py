import pytest

from ._resources import show_id, show_ids
from tekore import HTTPError


class TestSpotifyShow:
    def test_show_not_found_without_market(self, app_client):
        with pytest.raises(HTTPError):
            app_client.show(show_id)

    def test_show_found_with_market(self, app_client):
        show = app_client.show(show_id, market='FI')
        assert show.id == show_id

    def test_shows(self, app_client):
        shows = app_client.shows(show_ids, market='FI')
        assert show_ids == [s.id for s in shows]

    def test_show_episodes(self, app_client):
        episodes = app_client.show_episodes(show_id, market='FI', limit=1)
        assert episodes.items[0] is not None

    def test_show_found_without_market(self, user_client):
        show = user_client.show(show_id)
        assert show_id == show.id
