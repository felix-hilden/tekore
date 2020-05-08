import pytest
from ._resources import (
    user_id,
    playlist_id,
    playlist_local,
    playlist_podcast,
    track_ids,
    image,
)
from tekore import Spotify


class TestSpotifyPlaylistView:
    def test_playlists(self, app_client):
        app_client.playlists(user_id)

    def test_playlist(self, app_client):
        playlist = app_client.playlist(playlist_id)
        assert playlist.id == playlist_id

    def test_playlist_track_has_episode_and_track(self, app_client):
        track = app_client.playlist(playlist_id).tracks.items[0].track
        assert all(i is not None for i in (track.episode, track.track))

    def test_playlist_owner_attributes(self, app_client):
        owner = app_client.playlist(playlist_id).owner
        nones = [i is None for i in (owner.followers, owner.images)]
        assert all(nones)

    def test_playlist_with_local_track(self, app_client):
        playlist = app_client.playlist(playlist_local)
        assert playlist.tracks.items[0].is_local is True

    def test_playlist_cover_image(self, app_client):
        app_client.playlist_cover_image(playlist_id)

    def test_playlist_tracks(self, app_client):
        tracks = app_client.playlist_tracks(playlist_id)
        assert tracks.total > 0

    @pytest.mark.asyncio
    async def test_async_playlist_tracks(self, app_aclient):
        tracks = await app_aclient.playlist_tracks(playlist_id)
        assert tracks.total > 0

    def test_playlist_with_fields_returns_object(self, app_client):
        playlist = app_client.playlist(playlist_id, fields='uri')
        assert isinstance(playlist, dict)

    @pytest.mark.asyncio
    async def test_async_playlist_with_fields_returns_object(self, app_aclient):
        playlist = await app_aclient.playlist(playlist_id, fields='uri')
        assert isinstance(playlist, dict)

    def test_playlist_tracks_with_fields_returns_object(self, app_client):
        tracks = app_client.playlist_tracks(playlist_id, fields='total')
        assert isinstance(tracks, dict)

    @pytest.mark.asyncio
    async def test_async_playlist_tracks_fields_returns_object(self, app_aclient):
        tracks = await app_aclient.playlist_tracks(playlist_id, fields='uri')
        assert isinstance(tracks, dict)

    def test_playlist_podcast_no_market_returns_none(self, app_client):
        playlist = app_client.playlist(playlist_podcast)
        assert playlist.tracks.items[0].track is None

    def test_playlist_podcast_with_market_returned(self, app_client):
        playlist = app_client.playlist(playlist_podcast, market='FI')
        assert playlist.tracks.items[0].track.episode is True

    def test_playlist_with_podcast_as_tracks_no_market_returns_object(
            self, app_client
    ):
        playlist = app_client.playlist(playlist_podcast, episodes_as_tracks=True)
        assert playlist['tracks']['items'][0]['track'] is None

    def test_playlist_with_podcast_as_tracks_with_market_returns_object(
            self, app_client
    ):
        playlist = app_client.playlist(
            playlist_podcast,
            market='FI',
            episodes_as_tracks=True
        )
        assert playlist['tracks']['items'][0]['track']['track'] is True

    def test_playlist_tracks_podcast_no_market_returns_none(self, app_client):
        tracks = app_client.playlist_tracks(playlist_podcast)
        assert tracks.items[0].track is None

    def test_playlist_tracks_podcast_with_market_returned(self, app_client):
        tracks = app_client.playlist_tracks(playlist_podcast, market='FI')
        assert tracks.items[0].track.episode is True

    def test_playlist_tracks_with_podcast_as_tracks_no_market_returns_object(
            self, app_client
    ):
        tracks = app_client.playlist_tracks(
            playlist_podcast,
            episodes_as_tracks=True
        )
        assert tracks['items'][0]['track'] is None

    def test_playlist_tracks_with_podcast_as_tracks_with_market_returns_object(
            self, app_client
    ):
        tracks = app_client.playlist_tracks(
            playlist_podcast,
            market='FI',
            episodes_as_tracks=True
        )
        assert tracks['items'][0]['track']['track'] is True

    def test_followed_playlists(self, user_client):
        user_client.followed_playlists()

    def test_playlist_with_podcast(self, user_client):
        playlist = user_client.playlist(playlist_podcast)
        assert playlist.id == playlist_podcast

    def test_playlist_tracks_with_podcast(self, user_client):
        playlist = user_client.playlist(playlist_podcast)
        assert playlist.id == playlist_podcast


def assert_tracks_equal(client, playlist: str, tracks: list):
    observed = client.playlist_tracks(playlist)
    assert [t.track.id for t in observed.items] == tracks


class TestSpotifyPlaylistModify:
    """
    Ordered test set to test playlist creation and modification.
    """
    def test_playlist_modifications(self, user_client, current_user_id):
        playlist = user_client.playlist_create(
            current_user_id,
            'tekore-test',
            public=False,
            description='Temporary test playlist for Tekore'
        )
        # Playlist created
        assert playlist is not None

        try:
            # Upload new cover, assert last to wait for server
            user_client.playlist_cover_image_upload(playlist.id, image)

            new_name = 'tekore-test-modified'
            user_client.playlist_change_details(
                playlist.id,
                name=new_name,
                description='Temporary test playlist for Tekore (modified)'
            )
            playlist = user_client.playlist(playlist.id)
            # Details changed
            assert playlist.name == new_name

            # Tracks added
            user_client.playlist_tracks_add(playlist.id, track_ids[::-1])
            assert_tracks_equal(user_client, playlist.id, track_ids[::-1])

            # Tracks replaced
            user_client.playlist_tracks_replace(playlist.id, track_ids)
            assert_tracks_equal(user_client, playlist.id, track_ids)

            # Note: reordering tracks can sometimes result in another version of
            # the track to be added to the playlist instead. This occurred with
            # a 'single' being converted to the album version.
            snapshot = user_client.playlist_tracks_reorder(
                playlist.id,
                range_start=1,
                insert_before=0
            )
            # Tracks reordered
            assert_tracks_equal(
                user_client,
                playlist.id,
                [track_ids[1], track_ids[0]] + track_ids[2:]
            )

            user_client.playlist_tracks_reorder(
                playlist.id,
                range_start=1,
                insert_before=0,
                snapshot_id=snapshot
            )
            # Tracks reordered with snapshot
            assert_tracks_equal(user_client, playlist.id, track_ids)

            # Tracks removed
            user_client.playlist_tracks_remove(playlist.id, track_ids)
            tracks = user_client.playlist_tracks(playlist.id)
            assert tracks.total == 0

            # Add tracks back with duplicates and test removing occurrences
            new_tracks = track_ids + track_ids[::-1]
            user_client.playlist_tracks_replace(playlist.id, new_tracks)
            user_client.playlist_tracks_remove_occurrences(
                playlist.id,
                [(id_, ix) for ix, id_ in enumerate(track_ids)]
            )
            # Occurrences removed
            assert_tracks_equal(user_client, playlist.id, track_ids[::-1])

            # Add tracks back with duplicates and test removing indices
            new_tracks = track_ids + track_ids[::-1]
            user_client.playlist_tracks_replace(playlist.id, new_tracks)
            playlist = user_client.playlist(playlist.id)
            user_client.playlist_tracks_remove_indices(
                playlist.id,
                list(range(len(track_ids))),
                playlist.snapshot_id
            )
            # Indices removed
            assert_tracks_equal(user_client, playlist.id, track_ids[::-1])

            # Tracks cleared
            user_client.playlist_tracks_clear(playlist.id)
            assert_tracks_equal(user_client, playlist.id, [])

            # Assert cover was uploaded
            cover = user_client.playlist_cover_image(playlist.id)
            assert len(cover) > 0
        except Exception:
            raise
        finally:
            # Unfollow (delete) playlist to tear down
            user_client.playlist_unfollow(playlist.id)
