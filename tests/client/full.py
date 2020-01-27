from asyncio import run
from unittest import TestCase
from unittest.mock import MagicMock

from tekore.client import Spotify
from tests._util import handle_warnings
from tests._cred import TestCaseWithUserCredentials
from ._resources import album_id


class TestSpotifyBaseUnits(TestCase):
    def setUp(self):
        self.client = Spotify('token')

    def test_new_token_used_in_context(self):
        with self.client.token_as('new'):
            self.assertEqual(self.client.token, 'new')

    def test_old_token_restored_after_context(self):
        with self.client.token_as('new'):
            pass
        self.assertEqual(self.client.token, 'token')

    def test_next_with_no_next_set_returns_none(self):
        paging = MagicMock()
        paging.next = None

        next_ = self.client.next(paging)
        self.assertIsNone(next_)

    def test_previous_with_no_previous_set_returns_none(self):
        paging = MagicMock()
        paging.previous = None

        previous = self.client.previous(paging)
        self.assertIsNone(previous)


class TestSpotifyPaging(TestCaseWithUserCredentials):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Spotify(cls.user_token)
        cls.aclient = Spotify(cls.user_token, asynchronous=True)

        cls.tracks = cls.client.album_tracks(album_id, limit=1)
        cls.played = cls.client.playback_recently_played()

        cls.handle = handle_warnings()
        cls.handle.__enter__()

    @classmethod
    def tearDownClass(cls):
        cls.handle.__exit__(None, None, None)

    def test_paging_next(self):
        cat_next = self.client.next(self.tracks)
        self.assertGreater(cat_next.total, 0)

    def test_async_paging_next(self):
        cat_next = run(self.aclient.next(self.tracks))
        self.assertGreater(cat_next.total, 0)

    def test_paging_previous_of_next_is_identical(self):
        cat_next = self.client.next(self.tracks)
        cat_prev = self.client.previous(cat_next)
        self.assertEqual(self.tracks.items[0].id, cat_prev.items[0].id)

    def test_async_paging_previous_of_next_is_identical(self):
        async def f():
            cat_next = await self.aclient.next(self.tracks)
            return await self.aclient.previous(cat_next)

        cat_prev = run(f())
        self.assertEqual(self.tracks.items[0].id, cat_prev.items[0].id)

    def test_all_pages_exhausts_offset_paging(self):
        pages = list(self.client.all_pages(self.tracks))
        self.assertIsNone(pages[-1].next)

    def test_all_pages_exhausts_cursor_paging(self):
        pages = list(self.client.all_pages(self.played))

        with self.subTest('Next is None'):
            self.assertIsNone(pages[-1].next)
        with self.subTest('Cursors is None'):
            self.assertIsNone(pages[-1].cursors)

    def test_async_all_pages_exhausts_offset_paging(self):
        async def f():
            return [i async for i in self.aclient.all_pages(self.tracks)]

        pages = run(f())
        self.assertIsNone(pages[-1].next)

    def test_all_pages_from_cursor_paging_share_type(self):
        pages = self.client.all_pages(self.played)
        self.assertTrue(all(isinstance(p, type(self.played)) for p in pages))

    def test_all_items_from_cursor_paging_share_type(self):
        items = self.client.all_items(self.played)
        type_ = type(self.played.items[0])
        self.assertTrue(all(isinstance(i, type_) for i in items))

    def test_all_pages_from_offset_paging_share_type(self):
        pages = self.client.all_pages(self.tracks)
        self.assertTrue(all(isinstance(p, type(self.tracks)) for p in pages))

    def test_all_items_from_offset_paging_share_type(self):
        items = self.client.all_items(self.tracks)
        type_ = type(self.tracks.items[0])
        self.assertTrue(all(isinstance(i, type_) for i in items))

    def test_async_all_items_from_offset_paging_share_type(self):
        async def f():
            return [i async for i in self.aclient.all_items(self.tracks)]

        items = run(f())
        type_ = type(self.tracks.items[0])
        self.assertTrue(all(isinstance(i, type_) for i in items))
