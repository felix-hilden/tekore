import pytest

from tekore import HTTPError

from ._resources import artist_ids, playlist_id, user_ids


@pytest.fixture(scope="class")
def setup(data_client, current_user_id):
    try:
        current_playlist_follow = data_client.playlist_is_following(
            playlist_id, [current_user_id]
        )[0]
        current_artist_follows = data_client.artists_is_following(artist_ids)
        current_user_follows = data_client.users_is_following(user_ids)
    except HTTPError:
        pytest.skip("State before tests could not be determined!")

    yield

    if current_playlist_follow:
        data_client.playlist_follow(playlist_id, public=False)
    else:
        data_client.playlist_unfollow(playlist_id)

    artist_follows = [a for i, a in enumerate(artist_ids) if current_artist_follows[i]]
    if artist_follows:
        data_client.artists_follow(artist_follows)

    artist_unfollows = [
        a for i, a in enumerate(artist_ids) if not current_artist_follows[i]
    ]
    if artist_unfollows:
        data_client.artists_unfollow(artist_unfollows)

    user_follows = [u for i, u in enumerate(user_ids) if current_user_follows[i]]
    if user_follows:
        data_client.users_follow(user_follows)

    user_unfollows = [u for i, u in enumerate(user_ids) if not current_user_follows[i]]
    if user_unfollows:
        data_client.users_unfollow(user_unfollows)


@pytest.mark.api
@pytest.mark.usefixtures("setup")
class TestSpotifyFollow:
    """
    If current user follows the tested playlist, it is set as a private follow.
    """

    def test_playlist_follow(self, user_client):
        user_client.playlist_follow(playlist_id)

    def test_playlist_unfollow(self, user_client):
        user_client.playlist_unfollow(playlist_id)

    def test_followed_artists(self, user_client):
        user_client.followed_artists()

    def test_artists_follow(self, user_client):
        user_client.artists_follow(artist_ids)

    def test_artists_unfollow(self, user_client):
        user_client.artists_unfollow(artist_ids)

    def test_users_follow(self, user_client):
        user_client.users_follow(user_ids)

    def test_users_unfollow(self, user_client):
        user_client.users_unfollow(user_ids)
