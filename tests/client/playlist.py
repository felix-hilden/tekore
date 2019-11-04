from ._cred import TestCaseWithUserCredentials
from ._resources import user_id, playlist_id, playlist_local, track_ids, image

from spotipy.client import SpotifyPlaylist, SpotifyFollow


class TestSpotifyPlaylistView(TestCaseWithUserCredentials):
    def setUp(self):
        self.client = SpotifyPlaylist(self.user_token)

    def test_cu_playlists(self):
        self.client.current_user_playlists()

    def test_playlists(self):
        self.client.playlists(user_id)

    def test_playlist(self):
        self.client.playlist(playlist_id)

    def test_playlist_with_local_track(self):
        self.client.playlist(playlist_local)

    def test_playlist_cover_image(self):
        self.client.playlist_cover_image(playlist_id)

    def test_playlist_tracks(self):
        self.client.playlist_tracks(playlist_id)

    def test_playlist_tracks_with_fields_returns_object(self):
        tracks = self.client.playlist_tracks(playlist_id, fields='total')
        self.assertIsInstance(tracks, dict)


class TestSpotifyPlaylistModify(TestCaseWithUserCredentials):
    """
    Ordered test set to test playlist creation and modification.
    """
    def setUp(self):
        self.client = SpotifyPlaylist(self.user_token)

    def assertTracksEqual(self, sub_test_msg: str, playlist: str, tracks: list):
        observed = self.client.playlist_tracks(playlist)
        with self.subTest(sub_test_msg):
            self.assertListEqual(
                [t.track.id for t in observed.items],
                tracks
            )

    def test_playlist_modifications(self):
        playlist = self.client.playlist_create(
            self.current_user_id,
            'spotipy-test',
            public=False,
            description='Temporary test playlist for Spotipy'
        )
        with self.subTest('Playlist created'):
            self.assertIsNotNone(playlist)

        try:
            # Upload new cover, assert last to wait for server
            self.client.playlist_cover_image_upload(playlist.id, image)

            new_name = 'spotipy-test-modified'
            self.client.playlist_change_details(
                playlist.id,
                name=new_name,
                description='Temporary test playlist for Spotipy (modified)'
            )
            playlist = self.client.playlist(playlist.id)
            with self.subTest('Details changed'):
                self.assertEqual(playlist.name, new_name)

            self.client.playlist_tracks_add(playlist.id, track_ids[::-1])
            self.assertTracksEqual('Tracks added', playlist.id, track_ids[::-1])

            self.client.playlist_tracks_replace(playlist.id, track_ids)
            self.assertTracksEqual('Tracks replaced', playlist.id, track_ids)

            # Note: reordering tracks can sometimes result in another version of
            # the track to be added to the playlist instead. This occurred with
            # a 'single' being converted to the album version.
            snapshot = self.client.playlist_tracks_reorder(
                playlist.id,
                range_start=1,
                insert_before=0
            )
            self.assertTracksEqual(
                'Tracks reordered',
                playlist.id,
                [track_ids[1], track_ids[0]] + track_ids[2:]
            )

            self.client.playlist_tracks_reorder(
                playlist.id,
                range_start=1,
                insert_before=0,
                snapshot_id=snapshot
            )
            self.assertTracksEqual(
                'Tracks reordered with snapshot',
                playlist.id,
                track_ids
            )

            self.client.playlist_tracks_remove(playlist.id, track_ids)
            tracks = self.client.playlist_tracks(playlist.id)
            with self.subTest('Tracks removed'):
                self.assertEqual(tracks.total, 0)

            # Add tracks back with duplicates and test removing occurrences
            new_tracks = track_ids + track_ids[::-1]
            self.client.playlist_tracks_replace(playlist.id, new_tracks)
            self.client.playlist_tracks_remove_occurrences(
                playlist.id,
                [(id_, ix) for ix, id_ in enumerate(track_ids)]
            )
            self.assertTracksEqual(
                'Occurrences removed',
                playlist.id,
                track_ids[::-1]
            )

            # Add tracks back with duplicates and test removing indices
            new_tracks = track_ids + track_ids[::-1]
            self.client.playlist_tracks_replace(playlist.id, new_tracks)
            playlist = self.client.playlist(playlist.id)
            self.client.playlist_tracks_remove_indices(
                playlist.id,
                list(range(len(track_ids))),
                playlist.snapshot_id
            )
            self.assertTracksEqual('Indices removed', playlist.id, track_ids[::-1])

            # Assert cover was uploaded
            cover = self.client.playlist_cover_image(playlist.id)
            with self.subTest('Cover uploaded'):
                self.assertGreater(len(cover), 0)
        except Exception:
            raise
        finally:
            # Unfollow (delete) playlist to tear down
            follow = SpotifyFollow(self.user_token)
            follow.current_user_playlist_unfollow(playlist.id)
