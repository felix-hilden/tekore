import pytest

from ._resources import album_id


@pytest.fixture(scope="class")
def tracks(data_client):
    return data_client.album_tracks(album_id, limit=1)


@pytest.fixture(scope="class")
def played(data_client):
    return data_client.playback_recently_played()


@pytest.mark.api
@pytest.mark.usefixtures("suppress_warnings")
class TestSpotifyPaging:
    def test_next(self, app_client, tracks):
        cat_next = app_client.next(tracks)
        assert cat_next.total > 0

    @pytest.mark.asyncio
    async def test_async_next(self, app_aclient, tracks):
        cat_next = await app_aclient.next(tracks)
        assert cat_next.total > 0

    def test_next_parses_item_below_top_level(self, app_client):
        (cat,) = app_client.search("sheeran", limit=1)
        cat_next = app_client.next(cat)
        assert cat_next.total > 0

    def test_next_beyond_limit(self, app_client):
        (tracks,) = app_client.search("piano", limit=1, offset=999)
        assert app_client.next(tracks) is None

    @pytest.mark.asyncio
    async def test_async_next_beyond_limit(self, app_aclient):
        (tracks,) = await app_aclient.search("piano", limit=1, offset=999)
        assert await app_aclient.next(tracks) is None

    def test_previous_of_next(self, app_client, tracks):
        next_ = app_client.next(tracks)
        prev = app_client.previous(next_)
        assert tracks.items[0].id == prev.items[0].id

    @pytest.mark.asyncio
    async def test_async_previous_of_next(self, app_aclient, tracks):
        next_ = await app_aclient.next(tracks)
        prev = await app_aclient.previous(next_)
        assert tracks.items[0].id == prev.items[0].id

    @pytest.mark.asyncio
    async def test_async_previous_of_first(self, app_aclient, tracks):
        prev = await app_aclient.previous(tracks)
        assert prev is None

    def test_all_pages_exhausts_offset_paging(self, app_client, tracks):
        pages = list(app_client.all_pages(tracks))
        assert pages[-1].next is None

    def test_all_pages_exhausts_cursor_paging(self, user_client, played):
        pages = list(user_client.all_pages(played))
        assert pages[-1].next is None
        assert pages[-1].cursors is None

    @pytest.mark.asyncio
    async def test_async_all_pages_exhausts_offset_paging(self, app_aclient, tracks):
        pages = [i async for i in app_aclient.all_pages(tracks)]
        assert pages[-1].next is None

    def test_all_pages_from_cursor_paging_share_type(self, user_client, played):
        pages = user_client.all_pages(played)
        assert all(isinstance(p, type(played)) for p in pages)

    def test_all_items_from_cursor_paging_share_type(self, user_client, played):
        items = user_client.all_items(played)
        type_ = type(played.items[0])
        assert all(isinstance(i, type_) for i in items)

    def test_all_pages_from_offset_paging_share_type(self, app_client, tracks):
        pages = app_client.all_pages(tracks)
        assert all(isinstance(p, type(tracks)) for p in pages)

    def test_all_items_from_offset_paging_share_type(self, app_client, tracks):
        items = app_client.all_items(tracks)
        type_ = type(tracks.items[0])
        assert all(isinstance(i, type_) for i in items)

    @pytest.mark.asyncio
    async def test_async_all_items_from_offset_paging_share_type(
        self, app_aclient, tracks
    ):
        items = [i async for i in app_aclient.all_items(tracks)]
        type_ = type(tracks.items[0])
        assert all(isinstance(i, type_) for i in items)
