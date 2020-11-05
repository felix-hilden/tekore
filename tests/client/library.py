import pytest
from ._resources import album_ids, track_ids, show_ids


def revert(ids, current, add, remove):
    """
    Remove duplicates from the list.

    Args:
        ids: (list): write your description
        current: (todo): write your description
        add: (int): write your description
        remove: (bool): write your description
    """
    added = [item for i, item in enumerate(ids) if current[i]]
    if added:
        add(added)

    removed = [item for i, item in enumerate(ids) if not current[i]]
    if removed:
        remove(removed)


@pytest.fixture(scope='class')
def setup(data_client):
    """
    Sets up a track s tracks.

    Args:
        data_client: (todo): write your description
    """
    try:
        current_albums = data_client.saved_albums_contains(album_ids)
        current_tracks = data_client.saved_tracks_contains(track_ids)
        current_shows = data_client.saved_shows_contains(show_ids)
    except Exception:
        pytest.skip('State before tests could not be determined!')
        return

    yield

    revert(
        album_ids,
        current_albums,
        data_client.saved_albums_add,
        data_client.saved_albums_delete
    )

    revert(
        track_ids,
        current_tracks,
        data_client.saved_tracks_add,
        data_client.saved_tracks_delete
    )

    revert(
        show_ids,
        current_shows,
        data_client.saved_shows_add,
        data_client.saved_shows_delete
    )


def call(client, type_: str, ids: list):
    """
    Convenience function for a user

    Args:
        client: (todo): write your description
        type_: (todo): write your description
        ids: (list): write your description
    """
    return {
        'albums': client.saved_albums_contains,
        'shows': client.saved_shows_contains,
        'tracks': client.saved_tracks_contains,
    }[type_](ids)


def assert_contains(client, type_: str, ids: list):
    """
    Asserts that all of the specified ids have a list.

    Args:
        client: (todo): write your description
        type_: (todo): write your description
        ids: (list): write your description
    """
    assert all(call(client, type_, ids))


def assert_not_contains(client, type_: str, ids: list):
    """
    Asserts that all of the specified ids exist.

    Args:
        client: (todo): write your description
        type_: (todo): write your description
        ids: (list): write your description
    """
    assert not any(call(client, type_, ids))


@pytest.mark.usefixtures('setup')
class TestSpotifyFollow:
    """
    If the current user has saved the tested tracks, albums or shows,
    they will be deleted and added again.
    """
    def test_saved_albums(self, user_client):
        """
        Sets user saved api.

        Args:
            self: (todo): write your description
            user_client: (todo): write your description
        """
        user_client.saved_albums_delete(album_ids)

        user_client.saved_albums_add(album_ids)
        assert_contains(user_client, 'albums', album_ids)

        user_client.saved_albums()

        user_client.saved_albums_delete(album_ids)
        assert_not_contains(user_client, 'albums', album_ids)

    def test_saved_tracks(self, user_client):
        """
        Sets the specified tracks for a user.

        Args:
            self: (todo): write your description
            user_client: (todo): write your description
        """
        user_client.saved_tracks_delete(track_ids)

        user_client.saved_tracks_add(track_ids)
        assert_contains(user_client, 'tracks', track_ids)

        user_client.saved_tracks()

        user_client.saved_tracks_delete(track_ids)
        assert_not_contains(user_client, 'tracks', track_ids)

    def test_saved_shows(self, user_client):
        """
        Determine the user s users exist.

        Args:
            self: (todo): write your description
            user_client: (todo): write your description
        """
        user_client.saved_shows_delete(show_ids)

        user_client.saved_shows_add(show_ids)
        assert_contains(user_client, 'shows', show_ids)

        user_client.saved_shows()

        user_client.saved_shows_delete(show_ids)
        assert_not_contains(user_client, 'shows', show_ids)
