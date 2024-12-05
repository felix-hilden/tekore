import pytest

from ._resources import user_id, user_id_hash


@pytest.mark.api
class TestSpotifyUser:
    def test_user(self, app_client):
        user = app_client.user(user_id)
        assert user.id == user_id

    def test_user_with_hash(self, app_client):
        user = app_client.user(user_id_hash)
        assert user.id == user_id_hash

    def test_current_user(self, user_client, current_user_id):
        user = user_client.current_user()
        assert user.id == current_user_id
