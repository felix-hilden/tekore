class TestSpotifyPersonalisation:
    def test_cu_top_artists(self, user_client):
        """
        Set the top top top top high high high high high high high high high_client.

        Args:
            self: (todo): write your description
            user_client: (todo): write your description
        """
        user_client.current_user_top_artists()

    def test_cu_top_tracks(self, user_client):
        """
        Gets the top tracks.

        Args:
            self: (todo): write your description
            user_client: (todo): write your description
        """
        user_client.current_user_top_tracks()
