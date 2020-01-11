from ._cred import TestCaseWithUserCredentials
from spotipy.client.api import SpotifyPersonalisation


class TestSpotifyPersonalisation(TestCaseWithUserCredentials):
    def setUp(self):
        self.client = SpotifyPersonalisation(self.user_token)

    def test_cu_top_artists(self):
        self.client.current_user_top_artists()

    def test_cu_top_tracks(self):
        self.client.current_user_top_tracks()
