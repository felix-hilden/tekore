import pytest

from ._resources import audiobook_id, audiobook_ids
from tekore import InternalServerError, NotFound, from_uri


class TestSpotifyAudiobook:
    def test_audiobook_without_market_raises(self, app_client):
        with pytest.raises(InternalServerError):
            app_client.audiobook(audiobook_id)

    def test_audiobook_with_US_market(self, app_client):
        book = app_client.audiobook(audiobook_id, market='US')
        assert book.id == audiobook_id
        assert book.type == 'audiobook'
        assert from_uri(book.uri)[0] == 'show'

    def test_audiobook_with_non_US_market(self, app_client):
        with pytest.raises(InternalServerError):
            app_client.audiobook(audiobook_id, market='FI')

    def test_audiobooks_no_market_not_found(self, app_client):
        with pytest.raises(NotFound):
            app_client.audiobooks(audiobook_ids)

    def test_audiobooks_with_US_market(self, app_client):
        with pytest.raises(NotFound):
            app_client.audiobooks(audiobook_ids, market='US')

    def test_audiobook_chapters_no_market_not_found(self, app_client):
        with pytest.raises(InternalServerError):
            app_client.audiobook_chapters(audiobook_id, limit=1)

    def test_audiobook_chapters_US_market(self, app_client):
        chapters = app_client.audiobook_chapters(audiobook_id, market='US', limit=1)
        assert chapters.items[0] is not None

    def test_audiobook_chapters_non_US_market(self, app_client):
        with pytest.raises(InternalServerError):
            app_client.audiobook_chapters(audiobook_id, market='FI', limit=1)
