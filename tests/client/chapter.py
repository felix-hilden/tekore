import pytest

from tekore import NotFound, from_uri

from ._resources import chapter_id, chapter_ids


@pytest.mark.api
class TestSpotifyChapter:
    @pytest.mark.xfail(reason="API inconsistencies.")
    def test_chapter_no_market_not_found(self, app_client):
        with pytest.raises(NotFound):
            app_client.chapter(chapter_id)

    def test_chapter_with_us_market_found(self, app_client):
        chapter = app_client.chapter(chapter_id, market="US")
        assert chapter.id == chapter_id
        assert from_uri(chapter.uri)[0] == "episode"

    def test_chapter_with_non_us_market_found(self, app_client):
        chapter = app_client.chapter(chapter_id, market="FI")
        assert chapter.id == chapter_id
        assert from_uri(chapter.uri)[0] == "episode"

    @pytest.mark.xfail(reason="API inconsistencies.")
    def test_chapters_no_market_returns_none(self, app_client):
        chapters = app_client.chapters(chapter_ids)
        assert all(c is None for c in chapters)

    def test_chapters_us_market_found(self, app_client):
        chapters = app_client.chapters(chapter_ids, market="US")
        assert chapter_ids == [c.id for c in chapters]

    def test_chapters_non_us_market_returns_results(self, app_client):
        chapters = app_client.chapters(chapter_ids, market="FI")
        assert chapter_ids == [c.id for c in chapters]
