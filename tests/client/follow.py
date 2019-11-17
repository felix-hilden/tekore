from unittest import SkipTest
from ._cred import TestCaseWithUserCredentials
from ._resources import playlist_id, artist_ids, user_ids

from spotipy.client import SpotifyFollow


class TestSpotifyFollow(TestCaseWithUserCredentials):
    """
    If current user follows the tested playlist, it is set as a private follow.
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        client = SpotifyFollow(cls.user_token)
        try:
            cls.current_playlist_follow = client.playlist_is_following(
                playlist_id,
                [cls.current_user_id]
            )[0]
            cls.current_artist_follows = client.current_user_artists_is_following(
                artist_ids
            )
            cls.current_user_follows = client.current_user_users_is_following(
                user_ids
            )
        except Exception as e:
            raise SkipTest('State before tests could not be determined!') from e

    def setUp(self):
        self.client = SpotifyFollow(self.user_token)

    def test_cu_playlist_follow(self):
        self.client.current_user_playlist_follow(playlist_id)

    def test_cu_playlist_unfollow(self):
        self.client.current_user_playlist_unfollow(playlist_id)

    def test_cu_followed_artists(self):
        self.client.current_user_followed_artists()

    def test_cu_artists_follow(self):
        self.client.current_user_artists_follow(artist_ids)

    def test_cu_artists_unfollow(self):
        self.client.current_user_artists_unfollow(artist_ids)

    def test_cu_users_follow(self):
        self.client.current_user_users_follow(user_ids)

    def test_cu_users_unfollow(self):
        self.client.current_user_users_unfollow(user_ids)

    @classmethod
    def tearDownClass(cls):
        client = SpotifyFollow(cls.user_token)

        if cls.current_playlist_follow:
            client.current_user_playlist_follow(playlist_id, public=False)
        else:
            client.current_user_playlist_unfollow(playlist_id)

        artist_follows = [
            a for i, a in enumerate(artist_ids)
            if cls.current_artist_follows[i]
        ]
        if artist_follows:
            client.current_user_artists_follow(artist_follows)

        artist_unfollows = [
            a for i, a in enumerate(artist_ids)
            if not cls.current_artist_follows[i]
        ]
        if artist_unfollows:
            client.current_user_artists_unfollow(artist_unfollows)

        user_follows = [
            u for i, u in enumerate(user_ids)
            if cls.current_user_follows[i]
        ]
        if user_follows:
            client.current_user_users_follow(user_follows)

        user_unfollows = [
            u for i, u in enumerate(user_ids)
            if not cls.current_user_follows[i]
        ]
        if user_unfollows:
            client.current_user_users_unfollow(user_unfollows)
