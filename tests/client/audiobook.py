import pytest

from tekore import NotFound, from_uri

from ._resources import audiobook_id, audiobook_ids


@pytest.mark.api
class TestSpotifyAudiobook:
    @pytest.mark.xfail(reason="API inconsistencies.")
    def test_audiobook_without_market_raises(self, app_client):
        app_client.audiobook(audiobook_id)

    def test_audiobook_with_us_market(self, app_client):
        book = app_client.audiobook(audiobook_id, market="US")
        assert book.id == audiobook_id
        assert book.type == "audiobook"
        assert from_uri(book.uri)[0] == "show"

    @pytest.mark.xfail(reason="API inconsistencies.")
    def test_audiobook_with_non_us_market(self, app_client):
        app_client.audiobook(audiobook_id, market="FI")

    def test_audiobooks_no_market_not_found(self, app_client):
        with pytest.raises(NotFound):
            app_client.audiobooks(audiobook_ids)

    def test_audiobooks_with_us_market(self, app_client):
        with pytest.raises(NotFound):
            app_client.audiobooks(audiobook_ids, market="US")

    @pytest.mark.xfail(reason="API inconsistencies.")
    def test_audiobook_chapters_no_market_not_found(self, app_client):
        app_client.audiobook_chapters(audiobook_id, limit=1)

    def test_audiobook_chapters_us_market(self, app_client):
        chapters = app_client.audiobook_chapters(audiobook_id, market="US", limit=1)
        assert chapters.items[0] is not None

    @pytest.mark.xfail(reason="API inconsistencies.")
    def test_audiobook_chapters_non_us_market(self, app_client):
        app_client.audiobook_chapters(audiobook_id, market="FI", limit=1)
