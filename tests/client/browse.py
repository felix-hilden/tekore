from ._cred import TestCaseWithCredentials
from ._resources import artist_ids, category_id, genres, track_id

from tekore.client.api import SpotifyBrowse


class TestSpotifyArtist(TestCaseWithCredentials):
    def setUp(self):
        self.client = SpotifyBrowse(self.app_token)

    def test_featured_playlists_with_country(self):
        msg, playlists = self.client.featured_playlists(country='US')
        self.assertGreater(playlists.total, 0)

    def test_featured_playlists_no_country(self):
        msg, playlists = self.client.featured_playlists()
        self.assertGreater(playlists.total, 0)

    def test_new_releases_with_country(self):
        albums = self.client.new_releases(country='US')
        self.assertGreater(albums.total, 0)

    def test_new_releases_no_country(self):
        albums = self.client.new_releases()
        self.assertGreater(albums.total, 0)

    def test_categories_with_country(self):
        cat = self.client.categories(country='US')
        self.assertGreater(cat.total, 0)

    def test_categories_no_country(self):
        cat = self.client.categories()
        self.assertGreater(cat.total, 0)

    def test_category_with_country(self):
        cat = self.client.category(category_id, country='US')
        self.assertEqual(cat.id, category_id)

    def test_category_no_country(self):
        cat = self.client.category(category_id)
        self.assertEqual(cat.id, category_id)

    def test_category_playlists_with_country(self):
        playlists = self.client.category_playlists(category_id, country='US')
        self.assertGreater(playlists.total, 0)

    def test_category_playlists_no_country(self):
        playlists = self.client.category_playlists(category_id)
        self.assertGreater(playlists.total, 0)

    def test_recommendations_with_market(self):
        rec = self.client.recommendations(
            artist_ids=artist_ids,
            market='US'
        )
        self.assertGreater(len(rec.tracks), 0)

    def test_recommendations_no_market(self):
        rec = self.client.recommendations(
            artist_ids=artist_ids,
            market=None
        )
        self.assertGreater(len(rec.tracks), 0)

    def test_recommendations_all_arguments(self):
        rec = self.client.recommendations(
            artist_ids=artist_ids,
            genres=genres,
            track_ids=[track_id],
            market=None
        )
        self.assertGreater(len(rec.tracks), 0)

    def test_recommendations_target_attribute(self):
        rec = self.client.recommendations(
            artist_ids=artist_ids,
            market='US',
            target_valence=50
        )
        self.assertGreater(len(rec.tracks), 0)

    def test_recommendations_invalid_attribute_raises(self):
        with self.assertRaises(ValueError):
            self.client.recommendations(
                artist_ids=artist_ids,
                market='US',
                maxbogus=50
            )

    def test_recommendations_invalid_attribute_name_raises(self):
        with self.assertRaises(ValueError):
            self.client.recommendations(
                artist_ids=artist_ids,
                market='US',
                max_bogus=50
            )

    def test_recommendations_invalid_attribute_prefix_raises(self):
        with self.assertRaises(ValueError):
            self.client.recommendations(
                artist_ids=artist_ids,
                market='US',
                bogus_valence=50
            )

    def test_recommendation_genre_seeds(self):
        seeds = self.client.recommendation_genre_seeds()
        self.assertGreater(len(seeds), 0)
