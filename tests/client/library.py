from unittest import SkipTest
from ._cred import TestCaseWithUserCredentials
from ._resources import album_ids, track_ids

from spotipy.client import SpotifyLibrary


class TestSpotifyFollow(TestCaseWithUserCredentials):
    """
    If current user has saved the tested tracks,
    they will be deleted and added again.
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        client = SpotifyLibrary(cls.user_token)

        try:
            cls.current_albums = client.current_user_albums_contains(
                album_ids
            )
            cls.current_tracks = client.current_user_tracks_contains(
                track_ids
            )
        except Exception as e:
            raise SkipTest('State before tests could not be determined!') from e

    def setUp(self):
        self.client = SpotifyLibrary(self.user_token)

    def test_cu_albums(self):
        self.client.current_user_albums()

    def test_cu_albums_add(self):
        self.client.current_user_albums_add(album_ids)

    def test_cu_albums_delete(self):
        self.client.current_user_albums_delete(album_ids)

    def test_cu_tracks(self):
        self.client.current_user_tracks()

    def test_cu_tracks_add(self):
        self.client.current_user_tracks_add(track_ids)

    def test_cu_tracks_delete(self):
        self.client.current_user_tracks_delete(track_ids)

    @classmethod
    def tearDownClass(cls):
        client = SpotifyLibrary(cls.user_token)

        album_adds = [
            a for i, a in enumerate(album_ids)
            if cls.current_albums[i]
        ]
        if album_adds:
            client.current_user_albums_add(album_adds)

        album_dels = [
            a for i, a in enumerate(album_ids)
            if not cls.current_albums[i]
        ]
        if album_dels:
            client.current_user_albums_delete(album_dels)

        track_adds = [
            t for i, t in enumerate(track_ids)
            if cls.current_tracks[i]
        ]
        if track_adds:
            client.current_user_tracks_add(track_adds)

        track_dels = [
            t for i, t in enumerate(track_ids)
            if not cls.current_tracks[i]
        ]
        if track_dels:
            client.current_user_tracks_delete(track_dels)
