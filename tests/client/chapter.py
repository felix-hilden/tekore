import pytest

from ._resources import chapter_id, chapter_ids
from tekore import NotFound, from_uri


class TestSpotifyChapter:
    def test_chapter_no_market_not_found(self, app_client):
        with pytest.raises(NotFound):
            app_client.chapter(chapter_id)

    def test_chapter_with_US_market_found(self, app_client):
        chapter = app_client.chapter(chapter_id, market='US')
        assert chapter.id == chapter_id
        assert from_uri(chapter.uri)[0] == 'episode'

    def test_chapter_with_non_US_market_found(self, app_client):
        with pytest.raises(NotFound):
            app_client.chapter(chapter_id, market='FI')

    def test_chapters_no_market_returns_empty(self, app_client):
        chapters = app_client.chapters(chapter_ids)
        assert not chapters

    def test_chapters_US_market_found(self, app_client):
        chapters = app_client.chapters(chapter_ids, market='US')
        assert chapter_ids == [c.id for c in chapters]

    def test_chapters_non_US_market_returns_empty(self, app_client):
        chapters = app_client.chapters(chapter_ids, market='FI')
        assert not chapters
