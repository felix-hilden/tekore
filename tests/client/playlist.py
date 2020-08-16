import pytest

from tekore import to_uri
from ._resources import (
    user_id,
    playlist_id,
    playlist_local,
    playlist_special,
    track_ids,
    image,
)


class TestSpotifyPlaylistView:
    def test_playlists(self, app_client):
        app_client.playlists(user_id)

    def test_playlist(self, app_client):
        playlist = app_client.playlist(playlist_id)
        assert playlist.id == playlist_id

    def test_playlist_track_attributes(self, app_client):
        track = app_client.playlist_items(playlist_id, limit=1).items[0].track
        assert track.track is True
        assert track.episode is False
        assert track.is_local is False

    def test_playlist_episode_attributes(self, app_client):
        items = app_client.playlist_items(playlist_special, limit=1, market='FI')
        episode = items.items[0].track
        assert episode.track is False
        assert episode.episode is True
        assert hasattr(episode, 'is_local') is False

    def test_playlist_local_track_attributes(self, app_client):
        track = app_client.playlist_items(playlist_local).items[0].track
        assert track.track is True
        assert track.episode is False
        assert track.is_local is True

    def test_playlist_owner_attributes(self, app_client):
        owner = app_client.playlist(playlist_id).owner
        nones = [i is None for i in (owner.followers, owner.images)]
        assert all(nones)

    def test_playlist_cover_image(self, app_client):
        app_client.playlist_cover_image(playlist_id)

    def test_playlist_items(self, app_client):
        items = app_client.playlist_items(playlist_id)
        assert items.total > 0

    @pytest.mark.asyncio
    async def test_async_playlist_items(self, app_aclient):
        items = await app_aclient.playlist_items(playlist_id)
        assert items.total > 0

    def test_playlist_with_fields_returns_object(self, app_client):
        playlist = app_client.playlist(playlist_id, fields='uri')
        assert isinstance(playlist, dict)

    @pytest.mark.asyncio
    async def test_async_playlist_with_fields_returns_object(self, app_aclient):
        playlist = await app_aclient.playlist(playlist_id, fields='uri')
        assert isinstance(playlist, dict)

    def test_playlist_items_with_fields_returns_object(self, app_client):
        items = app_client.playlist_items(playlist_id, fields='total')
        assert isinstance(items, dict)

    @pytest.mark.asyncio
    async def test_async_playlist_items_fields_returns_object(self, app_aclient):
        items = await app_aclient.playlist_items(playlist_id, fields='uri')
        assert isinstance(items, dict)

    def test_playlist_podcast_no_market_returns_none(self, app_client):
        playlist = app_client.playlist(playlist_special)
        assert playlist.tracks.items[0].track is None

    def test_playlist_podcast_with_market_returned(self, app_client):
        playlist = app_client.playlist(playlist_special, market='FI')
        assert playlist.tracks.items[0].track.episode is True

    def test_playlist_with_podcast_as_tracks_no_market_returns_object(
            self, app_client
    ):
        playlist = app_client.playlist(playlist_special, as_tracks=True)
        assert playlist['tracks']['items'][0]['track'] is None

    def test_playlist_with_podcast_as_tracks_with_market_returns_object(
            self, app_client
    ):
        playlist = app_client.playlist(
            playlist_special,
            market='FI',
            as_tracks=True
        )
        assert playlist['tracks']['items'][0]['track']['track'] is True

    def test_playlist_as_tracks_takes_iterable(self, app_client):
        playlist = app_client.playlist(
            playlist_special,
            market='FI',
            as_tracks=['episode']
        )
        assert playlist['tracks']['items'][0]['track']['track'] is True

    def test_playlist_items_podcast_no_market_returns_none(self, app_client):
        items = app_client.playlist_items(playlist_special)
        assert items.items[0].track is None

    def test_playlist_items_podcast_with_market_returned(self, app_client):
        items = app_client.playlist_items(playlist_special, market='FI')
        assert items.items[0].track.episode is True

    def test_playlist_items_with_podcast_as_tracks_no_market_returns_object(
            self, app_client
    ):
        items = app_client.playlist_items(
            playlist_special,
            as_tracks=True
        )
        assert items['items'][0]['track'] is None

    def test_playlist_items_with_podcast_as_tracks_with_market_returns_object(
            self, app_client
    ):
        items = app_client.playlist_items(
            playlist_special,
            market='FI',
            as_tracks=True
        )
        assert items['items'][0]['track']['track'] is True

    def test_followed_playlists(self, user_client):
        user_client.followed_playlists()

    def test_playlist_with_podcast(self, user_client):
        playlist = user_client.playlist(playlist_special)
        assert playlist.id == playlist_special


def assert_items_equal(client, playlist: str, items: list):
    observed = client.playlist_items(playlist)
    assert [t.track.uri for t in observed.items] == items


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
        track_uris = [to_uri('track', id_) for id_ in track_ids]

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
            user_client.playlist_add(playlist.id, track_uris[::-1])
            assert_items_equal(user_client, playlist.id, track_uris[::-1])

            # Tracks replaced
            user_client.playlist_replace(playlist.id, track_uris)
            assert_items_equal(user_client, playlist.id, track_uris)

            # Note: reordering tracks can sometimes result in another version of
            # the track to be added to the playlist instead. This occurred with
            # a 'single' being converted to the album version.
            snapshot = user_client.playlist_reorder(
                playlist.id,
                range_start=1,
                insert_before=0
            )
            # Tracks reordered
            assert_items_equal(
                user_client,
                playlist.id,
                [track_uris[1], track_uris[0]] + track_uris[2:]
            )

            user_client.playlist_reorder(
                playlist.id,
                range_start=1,
                insert_before=0,
                snapshot_id=snapshot
            )
            # Tracks reordered with snapshot
            assert_items_equal(user_client, playlist.id, track_uris)

            # Tracks removed
            user_client.playlist_remove(playlist.id, track_uris)
            items = user_client.playlist_items(playlist.id)
            assert items.total == 0

            # Add tracks back with duplicates and test removing occurrences
            new_tracks = track_uris + track_uris[::-1]
            user_client.playlist_replace(playlist.id, new_tracks)
            user_client.playlist_remove_occurrences(
                playlist.id,
                [(uri, ix) for ix, uri in enumerate(track_uris)]
            )
            # Occurrences removed
            assert_items_equal(user_client, playlist.id, track_uris[::-1])

            # Add tracks back with duplicates and test removing indices
            new_tracks = track_uris + track_uris[::-1]
            user_client.playlist_replace(playlist.id, new_tracks)
            playlist = user_client.playlist(playlist.id)
            user_client.playlist_remove_indices(
                playlist.id,
                list(range(len(track_uris))),
                playlist.snapshot_id
            )
            # Indices removed
            assert_items_equal(user_client, playlist.id, track_uris[::-1])

            # Tracks cleared
            user_client.playlist_clear(playlist.id)
            assert_items_equal(user_client, playlist.id, [])

            # Assert cover was uploaded
            cover = user_client.playlist_cover_image(playlist.id)
            assert len(cover) > 0
        except Exception:
            raise
        finally:
            # Unfollow (delete) playlist to tear down
            user_client.playlist_unfollow(playlist.id)
