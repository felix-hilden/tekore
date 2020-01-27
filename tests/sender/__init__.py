from unittest import TestCase
from unittest.mock import MagicMock
from tekore.sender import (
    Sender,
    TransientSender,
    AsyncTransientSender,
    RetryingSender,
    Client,
    SenderConflictWarning,
)

from tests._util import handle_warnings


class TestSender(TestCase):
    def test_sender_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            Sender()


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


class TestSenderDefaults(TestCase):
    def setUp(self):
        from tekore import sender
        self.old_default_type = sender.default_sender_type
        self.old_default_instance = sender.default_sender_instance
        self.old_default_kwargs = sender.default_requests_kwargs

    def test_modify_default_sender_type(self):
        instance = MagicMock()
        type_mock = MagicMock(return_value=instance)

        from tekore import sender, Spotify
        sender.default_sender_type = type_mock

        s = Spotify()
        self.assertIs(s.sender, instance)

    def test_modify_default_sender_instance(self):
        instance = MagicMock()

        from tekore import sender, Spotify
        sender.default_sender_instance = instance

        s = Spotify()
        self.assertIs(s.sender, instance)

    def test_instance_has_precedence_over_type(self):
        instance = MagicMock()
        type_mock = MagicMock(return_value=MagicMock())

        from tekore import sender, Spotify
        sender.default_sender_type = type_mock
        sender.default_sender_instance = instance

        s = Spotify()
        self.assertIs(s.sender, instance)

    def test_retrying_sender_as_default_type_recurses(self):
        from tekore import sender
        sender.default_sender_type = sender.RetryingSender

        with self.assertRaises(RecursionError):
            RetryingSender()

    def test_default_kwargs_used_if_none_specified(self):
        kwargs = {'arg': 'val'}

        from tekore import sender
        sender.default_requests_kwargs = kwargs
        s = sender.TransientSender()
        self.assertDictEqual(s.requests_kwargs, kwargs)

    def test_default_kwargs_ignored_if_kwargs_specified(self):
        kwargs = {'arg': 'val'}

        from tekore import sender
        sender.default_requests_kwargs = kwargs
        s = sender.TransientSender(kw='value')
        self.assertNotIn('arg', s.requests_kwargs)

    def tearDown(self):
        from tekore import sender
        sender.default_sender_type = self.old_default_type
        sender.default_sender_instance = self.old_default_instance
        sender.default_requests_kwargs = self.old_default_kwargs
