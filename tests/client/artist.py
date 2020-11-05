from ._resources import artist_id, artist_ids
from tekore.model import AlbumGroup


class TestSpotifyArtist:
    def test_artist(self, app_client):
        """
        Test if an artist.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        artist = app_client.artist(artist_id)
        assert artist.id == artist_id

    def test_artists(self, app_client):
        """
        Test if a given app s artist.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        artists = app_client.artists(artist_ids)
        assert len(artists) == len(artist_ids)

    def test_artist_albums_with_market(self, app_client):
        """
        Test if the artist s artist.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        albums = app_client.artist_albums(artist_id, market='US')
        assert albums.total > 0

    def test_artist_albums_no_market(self, app_client):
        """
        Test if the artist s artist s artist.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        albums = app_client.artist_albums(artist_id, market=None)
        assert albums.total > 0

    def test_artist_albums_groups(self, app_client):
        """
        Test for artist groups.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        albums = app_client.artist_albums(
            artist_id,
            include_groups=[AlbumGroup.album, AlbumGroup.compilation],
            market=None
        )
        assert albums.total > 0

    def test_artist_albums_no_groups_returns_empty(self, app_client):
        """
        Get an artist s artist s artist groups.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        albums = app_client.artist_albums(
            artist_id,
            include_groups=[],
            market=None
        )
        assert albums.total == 0

    def test_artist_top_tracks_with_country(self, app_client):
        """
        Get a user s tracks.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        tracks = app_client.artist_top_tracks(artist_id, market='US')
        assert len(tracks) > 0

    def test_artist_related_artists(self, app_client):
        """
        Test if an artist s artist has already been created.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        artists = app_client.artist_related_artists(artist_id)
        assert len(artists) > 0

    def test_artist_albums_from_token(self, user_client):
        """
        Get the artist s artist s songs.

        Args:
            self: (todo): write your description
            user_client: (todo): write your description
        """
        albums = user_client.artist_albums(artist_id, market='from_token')
        assert albums.total > 0

    def test_artist_top_tracks_from_token(self, user_client):
        """
        Fetches the most similar tracks.

        Args:
            self: (todo): write your description
            user_client: (todo): write your description
        """
        tracks = user_client.artist_top_tracks(artist_id, market='from_token')
        assert len(tracks) > 0
