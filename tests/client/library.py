from unittest import SkipTest
from tests._cred import TestCaseWithUserCredentials
from ._resources import album_ids, track_ids, show_ids

from tekore.client.api import SpotifyLibrary


class TestSpotifyFollow(TestCaseWithUserCredentials):
    """
    If the current user has saved the tested tracks, albums or shows,
    they will be deleted and added again.
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = SpotifyLibrary(cls.user_token)

        try:
            cls.current_albums = cls.client.saved_albums_contains(album_ids)
            cls.current_tracks = cls.client.saved_tracks_contains(track_ids)
            cls.current_shows = cls.client.saved_shows_contains(show_ids)
        except Exception as e:
            raise SkipTest('State before tests could not be determined!') from e

        cls.call = {
            'albums': cls.client.saved_albums_contains,
            'shows': cls.client.saved_shows_contains,
            'tracks': cls.client.saved_tracks_contains,
        }

    def assert_contains(self, type_: str, ids: list):
        self.assertTrue(all(self.call[type_](ids)))

    def assert_not_contains(self, type_: str, ids: list):
        self.assertFalse(any(self.call[type_](ids)))

    def test_saved_albums(self):
        self.client.saved_albums_delete(album_ids)

        self.client.saved_albums_add(album_ids)
        with self.subTest('Albums added'):
            self.assert_contains('albums', album_ids)

        self.client.saved_albums()

        self.client.saved_albums_delete(album_ids)
        with self.subTest('Albums deleted'):
            self.assert_not_contains('albums', album_ids)

    def test_saved_tracks(self):
        self.client.saved_tracks_delete(track_ids)

        self.client.saved_tracks_add(track_ids)
        with self.subTest('Tracks added'):
            self.assert_contains('tracks', track_ids)

        self.client.saved_tracks()

        self.client.saved_tracks_delete(track_ids)
        with self.subTest('Tracks deleted'):
            self.assert_not_contains('tracks', track_ids)

    def test_saved_shows(self):
        self.client.saved_shows_delete(show_ids)

        self.client.saved_shows_add(show_ids)
        with self.subTest('Shows added'):
            self.assert_contains('shows', show_ids)

        self.client.saved_shows()

        self.client.saved_shows_delete(show_ids)
        with self.subTest('Shows deleted'):
            self.assert_not_contains('shows', show_ids)

    @staticmethod
    def _revert(ids, current, add, remove):
        added = [item for i, item in enumerate(ids) if current[i]]
        if added:
            add(added)

        removed = [item for i, item in enumerate(ids) if not current[i]]
        if removed:
            remove(removed)

    @classmethod
    def tearDownClass(cls):
        cls._revert(
            album_ids,
            cls.current_albums,
            cls.client.saved_albums_add,
            cls.client.saved_albums_delete
        )

        cls._revert(
            track_ids,
            cls.current_tracks,
            cls.client.saved_tracks_add,
            cls.client.saved_tracks_delete
        )

        cls._revert(
            show_ids,
            cls.current_shows,
            cls.client.saved_shows_add,
            cls.client.saved_shows_delete
        )
