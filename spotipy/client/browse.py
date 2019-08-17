from spotipy.client.base import SpotifyBase


class SpotifyBrowse(SpotifyBase):
    def featured_playlists(self, country: str = None, locale: str = None,
                           timestamp: str = None, limit: int = 20,
                           offset: int = 0):
        """
        Get a list of Spotify featured playlists.

        Parameters:
            - country - ISO 3166-1 alpha-2 country code
            - locale - desired language, consisting of a lowercase ISO 639
            language code and an uppercase ISO 3166-1 alpha-2 country code,
            joined by an underscore.
            - timestamp - timestamp in ISO 8601 format: yyyy-MM-ddTHH:mm:ss.
            Used to specify the user's local time to get results tailored for
            that specific date and time in the day.
            - limit - the number of items to return (1..50)
            - offset - the index of the first item to return
        """
        return self._get('browse/featured-playlists', locale=locale,
                         country=country, timestamp=timestamp, limit=limit,
                         offset=offset)

    def new_releases(self, country: str = None, limit: int = 20,
                     offset: int = 0):
        """
        Get a list of new album releases featured in Spotify.

        Parameters:
            - country - An ISO 3166-1 alpha-2 country code.
            - limit  - the number of items to return (1..50)
            - offset - the index of the first item to return
        """
        return self._get('browse/new-releases', country=country, limit=limit,
                         offset=offset)

    def categories(self, country: str = None, locale: str = None,
                   limit: int = 20, offset: int = 0):
        """
        Get a list of categories used to tag items in Spotify.

        Parameters:
            - country - An ISO 3166-1 alpha-2 country code.
            - locale - The desired language, consisting of an ISO 639 language
            code and an ISO 3166-1 alpha-2 country code, joined by
            an underscore.
            - limit - the number of items to return (1..50)
            - offset - the index of the first item to return
        """
        return self._get('browse/categories', country=country, locale=locale,
                         limit=limit, offset=offset)

    def category(self, category_id: str, country: str = None,
                 locale: str = None):
        """
        Get a single category used to tag items in Spotify.

        Parameters:
            - category_id - category ID
            - country - An ISO 3166-1 alpha-2 country code.
            - locale - The desired language, consisting of an ISO 639 language
            code and an ISO 3166-1 alpha-2 country code, joined by
            an underscore.
        """
        return self._get('browse/categories/' + category_id, country=country,
                         locale=locale)

    def category_playlists(self, category_id: str = None, country: str = None,
                           limit: int = 20, offset: int = 0):
        """
        Get a list of Spotify playlists tagged with a particular category.

        Parameters:
            - category_id - The Spotify category ID for the category.
            - country - An ISO 3166-1 alpha-2 country code.
            - limit - the number of items to return (1..50)
            - offset - the index of the first item to return
        """
        return self._get(f'browse/categories/{category_id}/playlists',
                         country=country, limit=limit, offset=offset)

    def recommendations(self, artist_ids: list = None, genres: list = None,
                        track_ids: list = None, limit: int = 20,
                        market: str = 'from_token', **kwargs):
        """
        Get a list of recommended tracks for seeds.

        Parameters:
            - seed_artists - list of artist IDs, URIs or URLs
            - seed_genres - list of genre names
            - seed_tracks - list of artist IDs, URIs or URLs
            - limit - the number of items to return (1..100)
            - market - ISO 3166-1 alpha-2 country code or 'from_token'
            - kwargs - min/max/target_<attribute> - For the tuneable track
            attributes listed in the documentation, these values
            provide filters and targeting on results.
        """
        params = dict(limit=limit)
        if artist_ids:
            params['seed_artists'] = ','.join(artist_ids)
        if genres:
            params['seed_genres'] = ','.join(genres)
        if track_ids:
            params['seed_tracks'] = ','.join(track_ids)
        if market:
            params['market'] = market

        for attribute in ['acousticness', 'danceability', 'duration_ms',
                          'energy', 'instrumentalness', 'key', 'liveness',
                          'loudness', 'mode', 'popularity', 'speechiness',
                          'tempo', 'time_signature', 'valence']:
            for prefix in ['min_', 'max_', 'target_']:
                param = prefix + attribute
                if param in kwargs:
                    params[param] = kwargs[param]
        return self._get('recommendations', **params)

    def recommendation_genre_seeds(self):
        return self._get('recommendations/available-genre-seeds')
