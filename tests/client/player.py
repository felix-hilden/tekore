from time import sleep
from requests import HTTPError

from tests._cred import TestCaseWithUserCredentials, skip_or_fail
from ._resources import track_ids, album_id
from tekore.client.api import SpotifyPlayer
from tekore.client import Spotify
from tekore.convert import to_uri


class TestSpotifyPlayerSequence(TestCaseWithUserCredentials):
    """
    Ordered test set to test player.
    As the Web API does not implement Queue functionality,
    this test set requires the user's queue to be empty.

    Attempts are made to restore playback state after tests.
    Nevertheless, song queues are not preserved.
    Playing saved tracks is not provided as a context,
    so the current song is resumed, but saved tracks won't continue playing.
    Shuffle and repeat states might be affected too.
    """
    def setUp(self):
        self.client = SpotifyPlayer(self.user_token)

        try:
            devices = self.client.playback_devices()
        except HTTPError as e:
            skip_or_fail(HTTPError, 'Playback devices could not be retrieved!', e)

        for device in devices:
            if not device.is_restricted and not device.is_private_session:
                self.device = device
                break
        else:
            skip_or_fail(
                AssertionError,
                'No unrestricted devices with public sessions found!'
            )

        try:
            self.playback = self.client.playback()
        except HTTPError as e:
            skip_or_fail(
                HTTPError,
                'Current playback information could not be retrieved!',
                e
            )

    def currently_playing(self):
        sleep(5)
        return self.client.playback_currently_playing()

    def assertPlaying(self, msg: str, track_id: str):
        playing = self.currently_playing()
        with self.subTest(msg):
            self.assertEqual(playing.item.id, track_id)

    def test_player(self):
        with self.subTest('Set volume'):
            self.client.playback_volume(0, device_id=self.device.id)

        with self.subTest('Transfer playback'):
            self.client.playback_transfer(self.device.id, force_play=True)

        self.client.playback_start_tracks(track_ids, offset=1)
        self.assertPlaying('Playback start with offset index', track_ids[1])

        playing = self.client.playback_currently_playing()
        with self.subTest('Currently playing has item'):
            self.assertIsNotNone(playing.item)

        self.client.playback_start_tracks(track_ids, offset=track_ids[1])
        self.assertPlaying('Playback start with offset uri', track_ids[1])

        self.client.playback_start_tracks(track_ids)
        self.assertPlaying('Playback start', track_ids[0])

        self.client.playback_pause()
        playing = self.currently_playing()
        with self.subTest('Playback pause'):
            self.assertFalse(playing.is_playing)

        with self.subTest('Player error: already paused'):
            with self.assertRaises(HTTPError):
                self.client.playback_pause()

        self.client.playback_resume()
        playing = self.currently_playing()
        with self.subTest('Playback resume'):
            self.assertTrue(playing.is_playing)

        self.client.playback_next()
        self.assertPlaying('Playback next', track_ids[1])

        self.client.playback_previous()
        self.assertPlaying('Playback previous', track_ids[0])

        self.client.playback_seek(30 * 1000)
        playing = self.currently_playing()
        with self.subTest('Playback seek'):
            self.assertGreater(playing.progress_ms, 30 * 1000)

        with self.subTest('Playback repeat'):
            self.client.playback_repeat('off')

        with self.subTest('Playback shuffle'):
            self.client.playback_shuffle(False)

        with self.subTest('Playback start context'):
            self.client.playback_start_context(to_uri('album', album_id))

        self.client.playback_queue_add(to_uri('track', track_ids[0]))
        self.client.playback_next()
        self.assertPlaying('Queue consumed on next', track_ids[0])

    def tearDown(self):
        if self.playback is None:
            self.client.playback_pause()
            self.client.playback_volume(
                self.device.volume_percent,
                self.device.id
            )
            return

        if self.playback.device is not None:
            self.client.playback_transfer(
                self.playback.device.id,
                self.playback.is_playing
            )

        if self.playback.context is None:
            self.client.playback_start_tracks(
                [self.playback.item.id],
                position_ms=self.playback.progress_ms
            )
        else:
            self.client.playback_start_context(
                self.playback.context.uri,
                offset=self.playback.item.id,
                position_ms=self.playback.progress_ms
            )
        if not self.playback.is_playing:
            self.client.playback_pause()

        self.client.playback_shuffle(self.playback.shuffle_state)
        self.client.playback_repeat(self.playback.repeat_state)

        self.client.playback_volume(self.device.volume_percent, self.device.id)


class TestSpotifyPlayer(TestCaseWithUserCredentials):
    def setUp(self):
        self.client = Spotify(self.user_token)

    def test_recently_played(self):
        self.client.playback_recently_played()

    def test_recently_played_before_timestamp_next_is_before_current(self):
        p1 = self.client.playback_recently_played(limit=1)
        p2 = self.client.next(p1)
        self.assertLess(p2.cursors.after, p1.cursors.after)

    def test_recently_played_after_timestamp_next_is_after_current(self):
        p1 = self.client.playback_recently_played(limit=1, after=1569888000)
        p2 = self.client.next(p1)
        self.assertGreater(p2.cursors.after, p1.cursors.after)
