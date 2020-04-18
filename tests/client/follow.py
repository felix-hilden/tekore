from unittest import SkipTest
from tests._cred import TestCaseWithUserCredentials
from ._resources import playlist_id, artist_ids, user_ids


class TestSpotifyFollow(TestCaseWithUserCredentials):
    """
    If current user follows the tested playlist, it is set as a private follow.
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        try:
            cls.current_playlist_follow = cls.client.playlist_is_following(
                playlist_id,
                [cls.current_user_id]
            )[0]
            cls.current_artist_follows = cls.client.artists_is_following(
                artist_ids
            )
            cls.current_user_follows = cls.client.users_is_following(
                user_ids
            )
        except Exception as e:
            raise SkipTest('State before tests could not be determined!') from e

    def test_playlist_follow(self):
        self.client.playlist_follow(playlist_id)

    def test_playlist_unfollow(self):
        self.client.playlist_unfollow(playlist_id)

    def test_followed_artists(self):
        self.client.followed_artists()

    def test_artists_follow(self):
        self.client.artists_follow(artist_ids)

    def test_artists_unfollow(self):
        self.client.artists_unfollow(artist_ids)

    def test_users_follow(self):
        self.client.users_follow(user_ids)

    def test_users_unfollow(self):
        self.client.users_unfollow(user_ids)

    @classmethod
    def tearDownClass(cls):
        if cls.current_playlist_follow:
            cls.client.playlist_follow(playlist_id, public=False)
        else:
            cls.client.playlist_unfollow(playlist_id)

        artist_follows = [
            a for i, a in enumerate(artist_ids)
            if cls.current_artist_follows[i]
        ]
        if artist_follows:
            cls.client.artists_follow(artist_follows)

        artist_unfollows = [
            a for i, a in enumerate(artist_ids)
            if not cls.current_artist_follows[i]
        ]
        if artist_unfollows:
            cls.client.artists_unfollow(artist_unfollows)

        user_follows = [
            u for i, u in enumerate(user_ids)
            if cls.current_user_follows[i]
        ]
        if user_follows:
            cls.client.users_follow(user_follows)

        user_unfollows = [
            u for i, u in enumerate(user_ids)
            if not cls.current_user_follows[i]
        ]
        if user_unfollows:
            cls.client.users_unfollow(user_unfollows)
