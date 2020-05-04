from unittest import TestCase
from tekore import (
    TransientSender,
    AsyncTransientSender,
    Client,
    SenderConflictWarning,
)

from tests._util import handle_warnings


class TestClient(TestCase):
    @staticmethod
    def _client(sender_async: bool, asynchronous: bool = None):
        sender = AsyncTransientSender if sender_async else TransientSender
        return Client(sender(), asynchronous=asynchronous)

    def test_is_async_reflects_sync_sender(self):
        c = self._client(sender_async=False)
        self.assertFalse(c.is_async)

    def test_is_async_reflects_async_sender(self):
        c = self._client(sender_async=True)
        self.assertTrue(c.is_async)

    def test_sync_sender_conflict_resolved_to_asynchronous_argument(self):
        with handle_warnings():
            c = self._client(False, True)
        self.assertTrue(c.is_async)

    def test_async_sender_conflict_resolved_to_asynchronous_argument(self):
        with handle_warnings():
            c = self._client(True, False)
        self.assertFalse(c.is_async)

    def test_sender_conflict_issues_warning(self):
        with handle_warnings('error'):
            with self.assertRaises(SenderConflictWarning):
                self._client(True, False)
