from spotipy.client._base import SpotifyBase


class SpotifyArtist(SpotifyBase):
    def artist(self, artist_id: str):
        return self._get('artists/' + artist_id)

    def artists(self, artist_ids: list):
        return self._get('artists/?ids=' + ','.join(artist_ids))

    def artist_albums(self, artist_id: str, include_groups: list = None,
                      market: str = 'from_token', limit: int = 20, offset: int = 0):
        """
        Get an artist's albums.

        Parameters:
            - artist_id - the artist ID
            - album_type - 'album', 'single', 'appears_on', 'compilation'
            - market - An ISO 3166-1 alpha-2 country code or 'from_token'
            - limit - the number of items to return (1..50)
            - offset - the index of the first item to return
        """
        return self._get('artists/{}/albums'.format(artist_id), include_groups=include_groups,
                         market=market, limit=limit, offset=offset)

    def artist_top_tracks(self, artist_id, market: str = 'from_token'):
        """
        Get an artist's top 10 tracks by country.

        Parameters:
            - artist_id - the artist ID
            - market - An ISO 3166-1 alpha-2 country code or 'from_token'
        """
        return self._get('artists/{}/top-tracks'.format(artist_id), market=market)

    def artist_related_artists(self, artist_id: str):
        """
        Get artists similar to an identified artist.
        Similarity is based on analysis of the Spotify community's listening history.
        """
        return self._get('artists/{}/related-artists'.format(artist_id))
