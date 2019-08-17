from spotipy.client.base import SpotifyBase


class SpotifyAlbum(SpotifyBase):
    def album(self, album_id: str, market: str = 'from_token'):
        """
        Get an album.

        Parameters:
            - album_id - album ID
            - market - An ISO 3166-1 alpha-2 country code or 'from_token'
        """
        return self._get('albums/' + album_id, market=market)

    def album_tracks(self, album_id: str, market: str = 'from_token', limit: int = 20, offset: int = 0):
        """
        Get tracks on album.

        Parameters:
            - album_id - album ID
            - market - An ISO 3166-1 alpha-2 country code or 'from_token'
            - limit - the number of items to return (1..50)
            - offset - the index of the first item to return
        """
        return self._get(f'albums/{album_id}/tracks', market=market, limit=limit, offset=offset)

    def albums(self, album_ids: list, market: str = 'from_token'):
        """
        Get multiple albums.

        Parameters:
            - album_ids - list of album IDs (1..20)
            - market - An ISO 3166-1 alpha-2 country code or 'from_token'
        """
        return self._get('albums/?ids=' + ','.join(album_ids), market=market)
