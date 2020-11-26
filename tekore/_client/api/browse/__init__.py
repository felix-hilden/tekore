from typing import List, Tuple

from .validate import validate_attributes
from ...base import SpotifyBase
from ...decor import send_and_process, maximise_limit, scopes
from ...process import single, top_item, multiple
from tekore.model import (
    SimplePlaylistPaging,
    SimpleAlbumPaging,
    CategoryPaging,
    Category,
    Recommendations
)


class SpotifyBrowse(SpotifyBase):
    """Browse API endpoints."""

    @scopes()
    @send_and_process(multiple(
        top_item('message'),
        single(SimplePlaylistPaging, from_item='playlists')
    ))
    @maximise_limit(50)
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
        Tuple[str, SimplePlaylistPaging]
            message and playlists
        """
        return self._get(
            'browse/featured-playlists',
            locale=locale,
            country=country,
            timestamp=timestamp,
            limit=limit,
            offset=offset
        )

    @scopes()
    @send_and_process(single(SimpleAlbumPaging, from_item='albums'))
    @maximise_limit(50)
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
        """
        return self._get(
            'browse/new-releases',
            country=country,
            limit=limit,
            offset=offset
        )

    @scopes()
    @send_and_process(single(CategoryPaging, from_item='categories'))
    @maximise_limit(50)
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
        """
        return self._get(
            'browse/categories',
            country=country,
            locale=locale,
            limit=limit,
            offset=offset
        )

    @scopes()
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
        """
        return self._get(
            'browse/categories/' + category_id,
            country=country,
            locale=locale
        )

    @scopes()
    @send_and_process(single(SimplePlaylistPaging, from_item='playlists'))
    @maximise_limit(50)
    def category_playlists(
            self,
            category_id: str,
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
        """
        return self._get(
            f'browse/categories/{category_id}/playlists',
            country=country,
            limit=limit,
            offset=offset
        )

    @scopes()
    @send_and_process(single(Recommendations))
    @maximise_limit(100)
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

        .. warning::
            The total number of seeds provided in ``artist_ids``, ``genres``
            and ``track_ids`` must be at least 1 and at most 5.

        Parameters
        ----------
        artist_ids
            list of seed artist IDs
        genres
            list of seed genre names
        track_ids
            list of seed artist IDs
        limit
            the number of items to return (1..100)
        market
            an ISO 3166-1 alpha-2 country code or 'from_token'
        attributes
            min/max/target_<attribute> - For all tuneable track attributes see
            :class:`model.RecommendationAttribute`,
            these values provide filters and targeting on results.

        Raises
        ------
        ValueError
            if any attribute is not allowed
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

    @scopes()
    @send_and_process(top_item('genres'))
    def recommendation_genre_seeds(self) -> List[str]:
        """Get a list of available genre seeds."""
        return self._get('recommendations/available-genre-seeds')
