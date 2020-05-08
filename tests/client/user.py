from ._resources import user_id


class TestSpotifyUser:
    def test_user(self, app_client):
        user = app_client.user(user_id)
        assert user.id == user_id

    def test_current_user(self, user_client, current_user_id):
        user = user_client.current_user()
        assert user.id == current_user_id
