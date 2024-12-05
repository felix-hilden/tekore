from time import sleep

import pytest

from tekore import HTTPError, to_uri
from tests.conftest import skip_or_fail

from ._resources import album_id, episode_id, track_ids


@pytest.fixture
def setup(user_client):
    try:
        devices = user_client.playback_devices()
    except HTTPError as e:
        skip_or_fail(HTTPError, "Playback devices could not be retrieved!", e)

    for device in devices:
        if not device.is_restricted and not device.is_private_session:
            break
    else:
        skip_or_fail(
            AssertionError, "No unrestricted devices with public sessions found!"
        )

    try:
        playback = user_client.playback()
    except HTTPError as e:
        skip_or_fail(
            HTTPError, "Current playback information could not be retrieved!", e
        )

    yield device.id

    if playback is None:
        user_client.playback_pause()
        user_client.playback_volume(device.volume_percent, device.id)
        return

    if playback.device is not None:
        user_client.playback_transfer(playback.device.id, playback.is_playing)

    if playback.context is None:
        user_client.playback_start_tracks(
            [playback.item.id], position_ms=playback.progress_ms
        )
    else:
        user_client.playback_start_context(
            playback.context.uri,
            offset=playback.item.id,
            position_ms=playback.progress_ms,
        )
    if not playback.is_playing:
        user_client.playback_pause()

    user_client.playback_shuffle(playback.shuffle_state)
    user_client.playback_repeat(playback.repeat_state)

    user_client.playback_volume(device.volume_percent, device.id)


SLEEP_SECS = 5


def currently_playing(client):
    sleep(SLEEP_SECS)
    return client.playback_currently_playing()


def assert_playing(client, track_id: str):
    playing = currently_playing(client)
    assert playing.item.id == track_id


@pytest.mark.api
@pytest.mark.usefixtures("setup")
class TestSpotifyPlayerSequence:
    """
    Ordered test set to test player.

    This test set requires an active device and an empty song queue.
    Restoring playback is not possible when listening to artists.

    Attempts are made to restore playback state after tests.
    Playing saved tracks is not provided as a context,
    so the current song is resumed, but saved tracks won't continue playing.
    Shuffle and repeat states might be affected too.
    """

    def test_player(self, user_client, setup):
        device_id = setup

        # Set volume
        user_client.playback_volume(0, device_id=device_id)

        # Transfer playback
        user_client.playback_transfer(device_id, force_play=True)

        # Playback start with offset index
        user_client.playback_start_tracks(track_ids, offset=1)
        assert_playing(user_client, track_ids[1])

        # Currently playing has an item
        playing = user_client.playback_currently_playing()
        assert playing.item is not None

        # Playback start with offset uri
        user_client.playback_start_tracks(track_ids, offset=track_ids[1])
        assert_playing(user_client, track_ids[1])

        # Playback start
        user_client.playback_start_tracks(track_ids[:2])
        assert_playing(user_client, track_ids[0])

        # Playback pause
        user_client.playback_pause()
        playing = currently_playing(user_client)
        assert playing.is_playing is False

        # Already paused
        with pytest.raises(HTTPError):
            user_client.playback_pause()

        # Playback resume
        user_client.playback_resume()
        playing = currently_playing(user_client)
        assert playing.is_playing is True

        # Playback next
        user_client.playback_next()
        assert_playing(user_client, track_ids[1])

        # Playback previous
        user_client.playback_previous()
        assert_playing(user_client, track_ids[0])

        # Playback seek
        user_client.playback_seek(30 * 1000)
        playing = currently_playing(user_client)
        assert playing.progress_ms > 30 * 1000

        # Playback repeat / shuffle
        user_client.playback_repeat("off")
        user_client.playback_shuffle(state=False)

        # Playback start context
        user_client.playback_start_context(to_uri("album", album_id))

        # Queue consumed on next
        user_client.playback_queue_add(to_uri("track", track_ids[0]))
        sleep(SLEEP_SECS)
        assert len(user_client.playback_queue().queue) > 0
        user_client.playback_next()
        assert_playing(user_client, track_ids[0])

        # Add episode to queue
        user_client.playback_queue_add(to_uri("episode", episode_id))

        # Currently playing episode returned by default
        user_client.playback_next()
        playing = currently_playing(user_client)
        assert playing.item.id == episode_id
        # Episode.show has total_episodes
        assert playing.item.show.total_episodes is not None

        # Currently playing item is none if only tracks
        playing = user_client.playback_currently_playing(tracks_only=True)
        assert playing.item is None

        # Playback episode returned by default
        playing = user_client.playback()
        assert playing.item.id == episode_id

        # Playback item is none if only tracks
        playing = user_client.playback(tracks_only=True)
        assert playing.item is None


@pytest.mark.api
class TestSpotifyPlayer:
    def test_recently_played(self, user_client):
        user_client.playback_recently_played()

    def test_recently_played_before_next_is_before_current(self, user_client):
        p1 = user_client.playback_recently_played(limit=1)
        p2 = user_client.next(p1)
        assert p2.cursors.after < p1.cursors.after

    def test_recently_played_after_next_is_after_current(self, user_client):
        p1 = user_client.playback_recently_played(limit=1, after=1569888000)
        p2 = user_client.next(p1)
        assert p2.cursors.after > p1.cursors.after
