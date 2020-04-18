from tests._cred import TestCaseWithUserCredentials


class TestSpotifyPersonalisation(TestCaseWithUserCredentials):
    def test_cu_top_artists(self):
        self.client.current_user_top_artists()

    def test_cu_top_tracks(self):
        self.client.current_user_top_tracks()
