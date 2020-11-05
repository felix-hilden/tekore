import pytest

from ._resources import album_id


@pytest.fixture(scope='class')
def tracks(data_client):
    """
    Get a tracks.

    Args:
        data_client: (todo): write your description
    """
    return data_client.album_tracks(album_id, limit=1)


@pytest.fixture(scope='class')
def played(data_client):
    """
    Return a : class :.

    Args:
        data_client: (todo): write your description
    """
    return data_client.playback_recently_played()


@pytest.mark.usefixtures('suppress_warnings')
class TestSpotifyPaging:
    def test_next(self, app_client, tracks):
        """
        Test the next app.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
            tracks: (todo): write your description
        """
        cat_next = app_client.next(tracks)
        assert cat_next.total > 0

    @pytest.mark.asyncio
    async def test_async_next(self, app_aclient, tracks):
          """
          Test if the next next next valid next async.

          Args:
              self: (todo): write your description
              app_aclient: (todo): write your description
              tracks: (todo): write your description
          """
        cat_next = await app_aclient.next(tracks)
        assert cat_next.total > 0

    def test_next_parses_item_below_top_level(self, app_client):
        """
        Test if the next level.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        cat, = app_client.search('sheeran', limit=1)
        cat_next = app_client.next(cat)
        assert cat_next.total > 0

    def test_next_beyond_limit(self, app_client):
        """
        Test for next next next next wait for next limit.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        tracks, = app_client.search('piano', limit=1, offset=1999)
        assert app_client.next(tracks) is None

    @pytest.mark.asyncio
    async def test_async_next_beyond_limit(self, app_aclient):
          """
          Test for next next acl limit.

          Args:
              self: (todo): write your description
              app_aclient: (todo): write your description
          """
        tracks, = await app_aclient.search('piano', limit=1, offset=1999)
        assert await app_aclient.next(tracks) is None

    def test_previous_of_next(self, app_client, tracks):
        """
        Test for previous tracks.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
            tracks: (todo): write your description
        """
        next_ = app_client.next(tracks)
        prev = app_client.previous(next_)
        assert tracks.items[0].id == prev.items[0].id

    @pytest.mark.asyncio
    async def test_async_previous_of_next(self, app_aclient, tracks):
          """
          Test for next previous previous tracks.

          Args:
              self: (todo): write your description
              app_aclient: (todo): write your description
              tracks: (todo): write your description
          """
        next_ = await app_aclient.next(tracks)
        prev = await app_aclient.previous(next_)
        assert tracks.items[0].id == prev.items[0].id

    @pytest.mark.asyncio
    async def test_async_previous_of_first(self, app_aclient, tracks):
          """
          Sets the previous tracks.

          Args:
              self: (todo): write your description
              app_aclient: (todo): write your description
              tracks: (todo): write your description
          """
        prev = await app_aclient.previous(tracks)
        assert prev is None

    def test_all_pages_exhausts_offset_paging(self, app_client, tracks):
        """
        Test if all pages are present in the same order.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
            tracks: (todo): write your description
        """
        pages = list(app_client.all_pages(tracks))
        assert pages[-1].next is None

    def test_all_pages_exhausts_cursor_paging(self, user_client, played):
        """
        Determine if all pages in the same consumer.

        Args:
            self: (todo): write your description
            user_client: (todo): write your description
            played: (todo): write your description
        """
        pages = list(user_client.all_pages(played))
        assert pages[-1].next is None
        assert pages[-1].cursors is None

    @pytest.mark.asyncio
    async def test_async_all_pages_exhausts_offset_paging(self, app_aclient, tracks):
          """
          Clone pages for all pages.

          Args:
              self: (todo): write your description
              app_aclient: (todo): write your description
              tracks: (todo): write your description
          """
        pages = [i async for i in app_aclient.all_pages(tracks)]
        assert pages[-1].next is None

    def test_all_pages_from_cursor_paging_share_type(self, user_client, played):
        """
        Set all pages on the specified share

        Args:
            self: (todo): write your description
            user_client: (todo): write your description
            played: (todo): write your description
        """
        pages = user_client.all_pages(played)
        assert all(isinstance(p, type(played)) for p in pages)

    def test_all_items_from_cursor_paging_share_type(self, user_client, played):
        """
        Test if all users in the share.

        Args:
            self: (todo): write your description
            user_client: (dict): write your description
            played: (todo): write your description
        """
        items = user_client.all_items(played)
        type_ = type(played.items[0])
        assert all(isinstance(i, type_) for i in items)

    def test_all_pages_from_offset_paging_share_type(self, app_client, tracks):
        """
        Test if all pages in the same type.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
            tracks: (todo): write your description
        """
        pages = app_client.all_pages(tracks)
        assert all(isinstance(p, type(tracks)) for p in pages)

    def test_all_items_from_offset_paging_share_type(self, app_client, tracks):
        """
        Test if all items in the given share share.

        Args:
            self: (todo): write your description
            app_client: (dict): write your description
            tracks: (todo): write your description
        """
        items = app_client.all_items(tracks)
        type_ = type(tracks.items[0])
        assert all(isinstance(i, type_) for i in items)

    @pytest.mark.asyncio
    async def test_async_all_items_from_offset_paging_share_type(
            self, app_aclient, tracks
    ):
          """
          Test if all items in a list of items are allowed.

          Args:
              self: (todo): write your description
              app_aclient: (dict): write your description
              tracks: (todo): write your description
          """
        items = [i async for i in app_aclient.all_items(tracks)]
        type_ = type(tracks.items[0])
        assert all(isinstance(i, type_) for i in items)
