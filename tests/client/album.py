from ._resources import album_id, album_ids, album_relinked, album_restricted


class TestSpotifyAlbum:
    def test_album_with_market(self, app_client):
        """
        Test if an album hashed album.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        album = app_client.album(album_id, market='US')
        assert album.id == album_id

    def test_album_no_market(self, app_client):
        """
        Test if an album is in an album.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        album = app_client.album(album_id, market=None)
        assert album.available_markets is not None

    def test_album_tracks_with_market(self, app_client):
        """
        Test if an album is in ack.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        tracks = app_client.album_tracks(album_id, market='US')
        assert tracks.total > 0

    def test_album_tracks_no_market(self, app_client):
        """
        Test if an artist s tracks.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        tracks = app_client.album_tracks(album_id, market=None)
        assert tracks.total > 0

    def test_album_tracks_relinking(self, app_client):
        """
        Test if the album s tracks are tracks.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        tracks = app_client.album_tracks(album_relinked, market='US', limit=1)
        track = tracks.items[0]
        assert track.is_playable is True

    def test_album_tracks_restricted(self, app_client):
        """
        Test if an artist s tracks.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        tracks = app_client.album_tracks(album_restricted, market='SE', limit=1)
        track = tracks.items[0]

        assert track.is_playable is False
        assert track.restrictions.reason == 'market'

    def test_albums_with_market(self, app_client):
        """
        Test if a list of albums.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        albums = app_client.albums(album_ids, market='US')
        assert len(albums) == len(album_ids)

    def test_albums_no_market(self, app_client):
        """
        Test if an iotile.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        albums = app_client.albums(album_ids, market=None)
        assert len(albums) == len(album_ids)

    def test_album_from_token(self, user_client):
        """
        Test if a user s album.

        Args:
            self: (todo): write your description
            user_client: (todo): write your description
        """
        album = user_client.album(album_id, market='from_token')
        assert album.id == album_id

    def test_album_tracks_from_token(self, user_client):
        """
        Get the album s album s tracks.

        Args:
            self: (todo): write your description
            user_client: (todo): write your description
        """
        tracks = user_client.album_tracks(album_id, market='from_token')
        assert tracks.total > 0

    def test_albums_from_token(self, user_client):
        """
        Test for many albums of a user.

        Args:
            self: (todo): write your description
            user_client: (todo): write your description
        """
        albums = user_client.albums(album_ids, market='from_token')
        assert len(albums) == len(album_ids)
