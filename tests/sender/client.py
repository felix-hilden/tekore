import pytest
from tekore import (
    TransientSender,
    AsyncTransientSender,
    Client,
    SenderConflictWarning,
)

from tests._util import handle_warnings


class TestClient:
    @staticmethod
    def _client(sender_async: bool, asynchronous: bool = None):
        sender = AsyncTransientSender if sender_async else TransientSender
        return Client(sender(), asynchronous=asynchronous)

    def test_is_async_reflects_sync_sender(self):
        c = self._client(sender_async=False)
        assert c.is_async is False

    def test_is_async_reflects_async_sender(self):
        c = self._client(sender_async=True)
        assert c.is_async is True

    def test_sync_sender_conflict_resolved_to_asynchronous_argument(self):
        with handle_warnings():
            c = self._client(False, True)
        assert c.is_async is True

    def test_async_sender_conflict_resolved_to_asynchronous_argument(self):
        with handle_warnings():
            c = self._client(True, False)
        assert c.is_async is False

    def test_sender_conflict_issues_warning(self):
        with handle_warnings('error'):
            with pytest.raises(SenderConflictWarning):
                self._client(True, False)
