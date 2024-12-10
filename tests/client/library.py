import pytest

from tekore import HTTPError

from ._resources import album_ids, episode_ids, show_ids, track_ids


def revert(ids, current, add, remove):
    added = [item for i, item in enumerate(ids) if current[i]]
    if added:
        add(added)

    removed = [item for i, item in enumerate(ids) if not current[i]]
    if removed:
        remove(removed)


@pytest.fixture(scope="class")
def setup(data_client):
    try:
        current_albums = data_client.saved_albums_contains(album_ids)
        current_episodes = data_client.saved_episodes_contains(episode_ids)
        current_tracks = data_client.saved_tracks_contains(track_ids)
        current_shows = data_client.saved_shows_contains(show_ids)
    except HTTPError:
        pytest.skip("State before tests could not be determined!")

    yield

    revert(
        album_ids,
        current_albums,
        data_client.saved_albums_add,
        data_client.saved_albums_delete,
    )

    revert(
        episode_ids,
        current_episodes,
        data_client.saved_episodes_add,
        data_client.saved_episodes_delete,
    )

    revert(
        track_ids,
        current_tracks,
        data_client.saved_tracks_add,
        data_client.saved_tracks_delete,
    )

    revert(
        show_ids,
        current_shows,
        data_client.saved_shows_add,
        data_client.saved_shows_delete,
    )


def call(client, type_: str, ids: list):
    return {
        "albums": client.saved_albums_contains,
        "episodes": client.saved_episodes_contains,
        "shows": client.saved_shows_contains,
        "tracks": client.saved_tracks_contains,
    }[type_](ids)


def assert_contains(client, type_: str, ids: list):
    assert all(call(client, type_, ids))


def assert_not_contains(client, type_: str, ids: list):
    assert not any(call(client, type_, ids))


@pytest.mark.api
@pytest.mark.usefixtures("setup")
class TestSpotifyFollow:
    """
    If the current user has saved the tested tracks, albums, episodes or shows,
    they will be deleted and added again.
    """

    def test_saved_albums(self, user_client):
        user_client.saved_albums_delete(album_ids)

        user_client.saved_albums_add(album_ids)
        assert_contains(user_client, "albums", album_ids)

        user_client.saved_albums()

        user_client.saved_albums_delete(album_ids)
        assert_not_contains(user_client, "albums", album_ids)

    def test_saved_episodes(self, user_client):
        user_client.saved_episodes_delete(episode_ids)

        user_client.saved_episodes_add(episode_ids)
        assert_contains(user_client, "episodes", episode_ids)

        user_client.saved_episodes()

        user_client.saved_episodes_delete(episode_ids)
        assert_not_contains(user_client, "episodes", episode_ids)

    def test_saved_tracks(self, user_client):
        user_client.saved_tracks_delete(track_ids)

        user_client.saved_tracks_add(track_ids)
        assert_contains(user_client, "tracks", track_ids)

        user_client.saved_tracks()

        user_client.saved_tracks_delete(track_ids)
        assert_not_contains(user_client, "tracks", track_ids)

    def test_saved_shows(self, user_client):
        user_client.saved_shows_delete(show_ids)

        user_client.saved_shows_add(show_ids)
        assert_contains(user_client, "shows", show_ids)

        user_client.saved_shows()

        user_client.saved_shows_delete(show_ids)
        assert_not_contains(user_client, "shows", show_ids)
