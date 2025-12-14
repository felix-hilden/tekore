import pytest

import tekore as tk

from ._resources import artist_ids, category_id, genres, track_id


@pytest.mark.api
class TestSpotifyBrowse:
    def test_featured_playlists_with_country(self, app_client):
        _, playlists = app_client.featured_playlists(country="US")
        assert playlists.total > 0

    def test_featured_playlists_no_country(self, app_client):
        _, playlists = app_client.featured_playlists()
        assert playlists.total > 0

    def test_new_releases_with_country(self, app_client):
        albums = app_client.new_releases(country="US")
        assert albums.total > 0

    def test_new_releases_no_country(self, app_client):
        albums = app_client.new_releases()
        assert albums.total > 0

    def test_categories_with_country(self, app_client):
        cat = app_client.categories(country="US")
        assert cat.total > 0

    def test_categories_no_country(self, app_client):
        cat = app_client.categories()
        assert cat.total > 0

    def test_category_with_country(self, app_client):
        cat = app_client.category(category_id, country="US")
        assert cat.id == category_id

    def test_category_no_country(self, app_client):
        cat = app_client.category(category_id)
        assert cat.id == category_id

    def test_category_playlists_with_country(self, app_client):
        playlists = app_client.category_playlists(category_id, country="US")
        assert playlists.total > 0

    def test_category_playlists_no_country(self, app_client):
        playlists = app_client.category_playlists(category_id)
        assert playlists.total > 0

    def test_recommendations_with_market(self, app_client):
        rec = app_client.recommendations(artist_ids=artist_ids, market="US")
        assert len(rec.tracks) > 0

    def test_recommendations_no_market(self, app_client):
        rec = app_client.recommendations(artist_ids=artist_ids, market=None)
        assert len(rec.tracks) > 0

    def test_recommendations_all_arguments(self, app_client):
        rec = app_client.recommendations(
            artist_ids=artist_ids, genres=genres, track_ids=[track_id], market=None
        )
        assert len(rec.tracks) > 0

    def test_recommendations_no_seeds(self, app_client):
        with pytest.raises(tk.BadRequest):
            app_client.recommendations()

    def test_recommendations_target_attribute(self, app_client):
        rec = app_client.recommendations(
            artist_ids=artist_ids, market="US", target_valence=50
        )
        assert len(rec.tracks) > 0

    def test_recommendations_invalid_attribute_raises(self, app_client):
        with pytest.raises(ValueError, match="Invalid attribute"):
            app_client.recommendations(artist_ids=artist_ids, market="US", maxbogus=50)

    def test_recommendations_invalid_attribute_name_raises(self, app_client):
        with pytest.raises(ValueError, match="Invalid attribute"):
            app_client.recommendations(artist_ids=artist_ids, market="US", max_bogus=50)

    def test_recommendations_invalid_attribute_prefix_raises(self, app_client):
        with pytest.raises(ValueError, match="Invalid attribute"):
            app_client.recommendations(
                artist_ids=artist_ids, market="US", bogus_valence=50
            )

    def test_recommendation_genre_seeds(self, app_client):
        seeds = app_client.recommendation_genre_seeds()
        assert len(seeds) > 0
