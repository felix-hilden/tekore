import pytest
from ._resources import artist_ids, category_id, genres, track_id


class TestSpotifyArtist:
    def test_featured_playlists_with_country(self, app_client):
        """
        Test whether the user playlists.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        msg, playlists = app_client.featured_playlists(country='US')
        assert playlists.total > 0

    def test_featured_playlists_no_country(self, app_client):
        """
        Test if the user s playlists.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        msg, playlists = app_client.featured_playlists()
        assert playlists.total > 0

    def test_new_releases_with_country(self, app_client):
        """
        Create new api keys.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        albums = app_client.new_releases(country='US')
        assert albums.total > 0

    def test_new_releases_no_country(self, app_client):
        """
        Create a new application.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        albums = app_client.new_releases()
        assert albums.total > 0

    def test_categories_with_country(self, app_client):
        """
        Test for the app_client for the given app.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        cat = app_client.categories(country='US')
        assert cat.total > 0

    def test_categories_no_country(self, app_client):
        """
        Sets the category category for the given app.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        cat = app_client.categories()
        assert cat.total > 0

    def test_category_with_country(self, app_client):
        """
        Sets the category for the given app.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        cat = app_client.category(category_id, country='US')
        assert cat.id == category_id

    def test_category_no_country(self, app_client):
        """
        Test if app_category_category

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        cat = app_client.category(category_id)
        assert cat.id == category_id

    def test_category_playlists_with_country(self, app_client):
        """
        Test if there s a playlists.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        playlists = app_client.category_playlists(category_id, country='US')
        assert playlists.total > 0

    def test_category_playlists_no_country(self, app_client):
        """
        : return : attr : playlists.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        playlists = app_client.category_playlists(category_id)
        assert playlists.total > 0

    def test_recommendations_with_market(self, app_client):
        """
        Test if a list of cookies.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        rec = app_client.recommendations(
            artist_ids=artist_ids,
            market='US'
        )
        assert len(rec.tracks) > 0

    def test_recommendations_no_market(self, app_client):
        """
        Test if a list of cookies *

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        rec = app_client.recommendations(
            artist_ids=artist_ids,
            market=None
        )
        assert len(rec.tracks) > 0

    def test_recommendations_all_arguments(self, app_client):
        """
        Test if there s a list of a given artist.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        rec = app_client.recommendations(
            artist_ids=artist_ids,
            genres=genres,
            track_ids=[track_id],
            market=None
        )
        assert len(rec.tracks) > 0

    def test_recommendations_target_attribute(self, app_client):
        """
        Test whether the specified artist attribute.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        rec = app_client.recommendations(
            artist_ids=artist_ids,
            market='US',
            target_valence=50
        )
        assert len(rec.tracks) > 0

    def test_recommendations_invalid_attribute_raises(self, app_client):
        """
        Test for a list of a list of tracks. tracks.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        with pytest.raises(ValueError):
            app_client.recommendations(
                artist_ids=artist_ids,
                market='US',
                maxbogus=50
            )

    def test_recommendations_invalid_attribute_name_raises(self, app_client):
        """
        Test if you want to see if there are valid.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        with pytest.raises(ValueError):
            app_client.recommendations(
                artist_ids=artist_ids,
                market='US',
                max_bogus=50
            )

    def test_recommendations_invalid_attribute_prefix_raises(self, app_client):
        """
        Test for an artist prefixes an artist.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        with pytest.raises(ValueError):
            app_client.recommendations(
                artist_ids=artist_ids,
                market='US',
                bogus_valence=50
            )

    def test_recommendation_genre_seeds(self, app_client):
        """
        Test if the seeds of - specific.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        seeds = app_client.recommendation_genre_seeds()
        assert len(seeds) > 0
