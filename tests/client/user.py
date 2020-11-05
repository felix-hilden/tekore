from ._resources import user_id


class TestSpotifyUser:
    def test_user(self, app_client):
        """
        Test if app_client exists in user.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        user = app_client.user(user_id)
        assert user.id == user_id

    def test_current_user(self, user_client, current_user_id):
        """
        Set the current user.

        Args:
            self: (todo): write your description
            user_client: (todo): write your description
            current_user_id: (str): write your description
        """
        user = user_client.current_user()
        assert user.id == current_user_id
