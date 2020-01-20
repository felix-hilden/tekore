import unittest
import warnings

from unittest.mock import patch, MagicMock
from contextlib import contextmanager
from requests import Request

from tekore.sender import (
    Sender,
    TransientSender,
    SingletonSender,
    PersistentSender,
    RetryingSender,
    AsyncTransientSender,
    SenderConflictWarning,
    Client,
)


class TestSender(unittest.TestCase):
    def test_sender_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            Sender()


class MockSessionFactory:
    prepare_return = 'prepared'

    def __init__(self):
        self.instances = []

    def __call__(self, *args, **kwargs):
        mock = MagicMock()
        mock.__enter__ = MagicMock(return_value=mock)
        mock.prepare_request = MagicMock(return_value=self.prepare_return)

        self.instances.append(mock)
        return mock


class TestSingletonSender(unittest.TestCase):
    def test_instances_share_session(self):
        s1 = SingletonSender()
        s2 = SingletonSender()
        self.assertTrue(s1.session is s2.session)

    def test_request_prepared(self):
        mock = MockSessionFactory()
        with patch('tekore.sender.SingletonSender.session', mock()):
            s = SingletonSender()
            r = Request()
            s.send(r)
            mock.instances[0].prepare_request.assert_called_with(r)

    def test_keywords_passed_to_session(self):
        mock = MockSessionFactory()
        kwargs = dict(k1='k1', k2='k2')
        with patch('tekore.sender.SingletonSender.session', mock()):
            s = SingletonSender(**kwargs)
            r = Request()
            s.send(r)
            mock.instances[0].send.assert_called_with(
                mock.prepare_return,
                **kwargs
            )


def test_request_prepared(sender_type):
    mock = MockSessionFactory()
    with patch('tekore.sender.Session', mock):
        s = sender_type()
        r = Request()
        s.send(r)
        mock.instances[0].prepare_request.assert_called_with(r)


def test_keywords_passed_to_session(sender_type):
    mock = MockSessionFactory()
    kwargs = dict(k1='k1', k2='k2')
    with patch('tekore.sender.Session', mock):
        s = sender_type(**kwargs)
        s.send(Request())
        mock.instances[0].send.assert_called_with(mock.prepare_return, **kwargs)


class TestPersistentSender(unittest.TestCase):
    @patch('tekore.sender.Session', MagicMock)
    def test_session_is_reused(self):
        s = PersistentSender()
        sess1 = s.session
        s.send(Request())
        s.send(Request())
        sess2 = s.session
        self.assertTrue(sess1 is sess2)

    def test_instances_dont_share_session(self):
        s1 = PersistentSender()
        s2 = PersistentSender()
        self.assertTrue(s1.session is not s2.session)

    def test_request_prepared(self):
        test_request_prepared(PersistentSender)

    def test_keywords_passed_to_session(self):
        test_keywords_passed_to_session(PersistentSender)


class TestTransientSender(unittest.TestCase):
    def test_session_is_not_reused(self):
        mock = MockSessionFactory()
        with patch('tekore.sender.Session', mock):
            s = TransientSender()
            s.send(Request())
            s.send(Request())
            self.assertEqual(len(mock.instances), 2)

    def test_request_prepared(self):
        test_request_prepared(TransientSender)

    def test_keywords_passed_to_session(self):
        test_keywords_passed_to_session(TransientSender)


def ok_response() -> MagicMock:
    response = MagicMock()
    response.status_code = 200
    return response


def rate_limit_response(retry_after: int = 1) -> MagicMock:
    response = MagicMock()
    response.status_code = 429
    response.headers = {'Retry-After': retry_after}
    return response


def failed_response() -> MagicMock:
    response = MagicMock()
    response.status_code = 500
    return response


def mock_sender(*responses):
    sender = MagicMock()
    sender.is_async = False
    sender.send.side_effect = responses
    return sender


class TestRetryingSender(unittest.TestCase):
    def test_rate_limited_request_retried_after_set_seconds(self):
        time = MagicMock()
        fail = rate_limit_response()
        success = ok_response()
        sender = mock_sender(fail, success)

        s = RetryingSender(sender=sender)
        with patch('tekore.sender.time', time):
            s.send(Request())
            time.sleep.assert_called_once_with(1)

    def test_failing_request_but_no_retries_returns_failed(self):
        fail = failed_response()
        success = ok_response()
        sender = mock_sender(fail, success)
        s = RetryingSender(sender=sender)
        r = s.send(Request())
        self.assertTrue(r is fail)

    def test_failing_request_retried_max_times(self):
        fail = failed_response()
        success = ok_response()
        sender = mock_sender(fail, fail, fail, success)

        s = RetryingSender(retries=2, sender=sender)
        with patch('tekore.sender.time', MagicMock()):
            s.send(Request())
        self.assertEqual(sender.send.call_count, 3)

    def test_retry_returns_on_first_success(self):
        fail = failed_response()
        success = ok_response()
        sender = mock_sender(fail, fail, success, fail, success)

        s = RetryingSender(retries=5, sender=sender)
        with patch('tekore.sender.time', MagicMock()):
            s.send(Request())
        self.assertEqual(sender.send.call_count, 3)

    def test_rate_limited_retry_doesnt_decrease_retry_count(self):
        fail = failed_response()
        rate = rate_limit_response()
        success = ok_response()
        sender = mock_sender(fail, rate, fail, success)

        s = RetryingSender(retries=2, sender=sender)
        with patch('tekore.sender.time', MagicMock()):
            s.send(Request())

        self.assertEqual(sender.send.call_count, 4)


class TestSenderDefaults(unittest.TestCase):
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


@contextmanager
def handle_warnings(filt: str = 'ignore'):
    warnings.simplefilter(filt)
    yield
    warnings.resetwarnings()


class TestClient(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
