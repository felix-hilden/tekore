from typing import List, Tuple

from tekore.client.api.browse.validate import validate_attributes
from tekore.client.process import single, top_item, multiple
from tekore.client.base import SpotifyBase, send_and_process
from tekore.model import (
    SimplePlaylistPaging,
    SimpleAlbumPaging,
    CategoryPaging,
    Category,
    Recommendations
)


class SpotifyBrowse(SpotifyBase):
    @send_and_process(multiple(
        top_item('message'),
        single(SimplePlaylistPaging, from_item='playlists')
    ))
    def featured_playlists(
            self,
            country: str = None,
            locale: str = None,
            timestamp: str = None,
            limit: int = 20,
            offset: int = 0
    ) -> Tuple[str, SimplePlaylistPaging]:
        """
        Get a list of Spotify featured playlists.

        Parameters
        ----------
        country
            an ISO 3166-1 alpha-2 country code
        locale
            the desired language, consisting of a lowercase ISO 639 language code
            and an uppercase ISO 3166-1 alpha-2 country code joined by an underscore
        timestamp
            Timestamp in ISO 8601 format: yyyy-MM-ddTHH:mm:ss.
            Used to specify the user's local time to get results tailored for
            that specific date and time in the day.
        limit
            the number of items to return (1..50)
        offset
            the index of the first item to return

        Returns
        -------
        tuple
            (str, SimplePlaylistPaging): message for the playlists and a list of
            simplified playlist objects wrapped in a paging object
        """
        return self._get(
            'browse/featured-playlists',
            locale=locale,
            country=country,
            timestamp=timestamp,
            limit=limit,
            offset=offset
        )

    @send_and_process(single(SimpleAlbumPaging, from_item='albums'))
    def new_releases(
            self,
            country: str = None,
            limit: int = 20,
            offset: int = 0
    ) -> SimpleAlbumPaging:
        """
        Get a list of new album releases featured in Spotify.

        Parameters
        ----------
        country
            an ISO 3166-1 alpha-2 country code
        limit
            the number of items to return (1..50)
        offset
            the index of the first item to return

        Returns
        -------
        SimpleAlbumPaging
            paging containing simplified album objects
        """
        return self._get(
            'browse/new-releases',
            country=country,
            limit=limit,
            offset=offset
        )

    @send_and_process(single(CategoryPaging, from_item='categories'))
    def categories(
            self,
            country: str = None,
            locale: str = None,
            limit: int = 20,
            offset: int = 0
    ) -> CategoryPaging:
        """
        Get a list of categories used to tag items in Spotify.

        Parameters
        ----------
        country
            an ISO 3166-1 alpha-2 country code
        locale
            the desired language, consisting of a lowercase ISO 639 language code
            and an uppercase ISO 3166-1 alpha-2 country code joined by an underscore
        limit
            the number of items to return (1..50)
        offset
            the index of the first item to return

        Returns
        -------
        CategoryPaging
            paging object containing a list of categories
        """
        return self._get(
            'browse/categories',
            country=country,
            locale=locale,
            limit=limit,
            offset=offset
        )

    @send_and_process(single(Category))
    def category(
            self,
            category_id: str,
            country: str = None,
            locale: str = None
    ) -> Category:
        """
        Get a single category used to tag items in Spotify.

        Parameters
        ----------
        category_id
            category ID
        country
            an ISO 3166-1 alpha-2 country code
        locale
            the desired language, consisting of a lowercase ISO 639 language code
            and an uppercase ISO 3166-1 alpha-2 country code joined by an underscore

        Returns
        -------
        Category
            category object
        """
        return self._get(
            'browse/categories/' + category_id,
            country=country,
            locale=locale
        )

    @send_and_process(single(SimplePlaylistPaging, from_item='playlists'))
    def category_playlists(
            self,
            category_id: str = None,
            country: str = None,
            limit: int = 20,
            offset: int = 0
    ) -> SimplePlaylistPaging:
        """
        Get a list of Spotify playlists tagged with a particular category.

        Parameters
        ----------
        category_id
            category ID
        country
            an ISO 3166-1 alpha-2 country code
        limit
            the number of items to return (1..50)
        offset
            the index of the first item to return

        Returns
        -------
        SimplePlaylistPaging
            paging object containing a list of simplified playlist objects
        """
        return self._get(
            f'browse/categories/{category_id}/playlists',
            country=country,
            limit=limit,
            offset=offset
        )

    @send_and_process(single(Recommendations))
    def recommendations(
            self,
            artist_ids: list = None,
            genres: list = None,
            track_ids: list = None,
            limit: int = 20,
            market: str = None,
            **attributes
    ) -> Recommendations:
        """
        Get a list of recommended tracks for seeds.

        Up to 5 seed values may be provided as artists, genres and tracks.

        Parameters
        ----------
        artist_ids
            list of artist IDs, URIs or URLs
        genres
            list of genre names
        track_ids
            list of artist IDs, URIs or URLs
        limit
            the number of items to return (1..100)
        market
            an ISO 3166-1 alpha-2 country code or 'from_token'
        attributes
            min/max/target_<attribute> - For all tuneable track attributes see
            :class:`tekore.model.recommendations.RecommendationAttribute`,
            these values provide filters and targeting on results.

        Returns
        -------
        Recommendations
            recommendations object containing track recommendations and seeds
        """
        params = dict(limit=limit)
        if artist_ids is not None:
            params['seed_artists'] = ','.join(artist_ids)
        if genres is not None:
            params['seed_genres'] = ','.join(genres)
        if track_ids is not None:
            params['seed_tracks'] = ','.join(track_ids)
        if market is not None:
            params['market'] = market

        validate_attributes(attributes)
        params.update(attributes)

        return self._get('recommendations', **params)

    @send_and_process(top_item('genres'))
    def recommendation_genre_seeds(self) -> List[str]:
        """
        Get a list of available genre seeds.

        Returns
        -------
        list
            list of genres to use as seeds
        """
        return self._get('recommendations/available-genre-seeds')
