from asyncio import run
from unittest import TestCase
from unittest.mock import MagicMock, patch

from requests import Request
from tekore.sender import RetryingSender
from tests._util import AsyncMock


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


def mock_sender(*responses, is_async: bool = False):
    sender = MagicMock()
    sender.is_async = is_async
    if is_async:
        sender.send = AsyncMock(side_effect=responses)
    else:
        sender.send.side_effect = responses
    return sender


class TestRetryingSender(TestCase):
    def test_rate_limited_request_retried_after_set_seconds(self):
        time = MagicMock()
        fail = rate_limit_response()
        success = ok_response()
        sender = mock_sender(fail, success)

        s = RetryingSender(sender=sender)
        with patch('tekore.sender.time', time):
            s.send(Request())
            time.sleep.assert_called_once_with(1 + 1)

    def test_async_rate_limited_request_retried_after_set_seconds(self):
        asyncio = AsyncMock()
        fail = rate_limit_response()
        success = ok_response()
        sender = mock_sender(fail, success, is_async=True)

        s = RetryingSender(sender=sender)
        with patch('tekore.sender.asyncio', asyncio):
            run(s.send(Request()))
            asyncio.sleep.assert_called_once_with(1 + 1)

    def test_default_retry_after_is_one(self):
        time = MagicMock()
        fail = rate_limit_response()
        del fail.headers['Retry-After']
        success = ok_response()
        sender = mock_sender(fail, success)

        s = RetryingSender(sender=sender)
        with patch('tekore.sender.time', time):
            s.send(Request())
            time.sleep.assert_called_once_with(1 + 1)

    def test_async_default_retry_after_is_one(self):
        asyncio = AsyncMock()
        fail = rate_limit_response()
        del fail.headers['Retry-After']
        success = ok_response()
        sender = mock_sender(fail, success, is_async=True)

        s = RetryingSender(sender=sender)
        with patch('tekore.sender.asyncio', asyncio):
            run(s.send(Request()))
            asyncio.sleep.assert_called_once_with(1 + 1)

    def test_failing_request_but_no_retries_returns_failed(self):
        fail = failed_response()
        success = ok_response()
        sender = mock_sender(fail, success)
        s = RetryingSender(sender=sender)
        r = s.send(Request())
        self.assertTrue(r is fail)

    def test_async_failing_request_but_no_retries_returns_failed(self):
        fail = failed_response()
        success = ok_response()
        sender = mock_sender(fail, success, is_async=True)
        s = RetryingSender(sender=sender)
        r = run(s.send(Request()))
        self.assertTrue(r is fail)

    def test_failing_request_retried_max_times(self):
        fail = failed_response()
        success = ok_response()
        sender = mock_sender(fail, fail, fail, success)

        s = RetryingSender(retries=2, sender=sender)
        with patch('tekore.sender.time', MagicMock()):
            s.send(Request())
        self.assertEqual(sender.send.call_count, 3)

    def test_async_failing_request_retried_max_times(self):
        fail = failed_response()
        success = ok_response()
        sender = mock_sender(fail, fail, fail, success, is_async=True)

        s = RetryingSender(retries=2, sender=sender)
        with patch('tekore.sender.asyncio', AsyncMock()):
            run(s.send(Request()))
        self.assertEqual(sender.send.call_count, 3)

    def test_retry_returns_on_first_success(self):
        fail = failed_response()
        success = ok_response()
        sender = mock_sender(fail, fail, success, fail, success)

        s = RetryingSender(retries=5, sender=sender)
        with patch('tekore.sender.time', MagicMock()):
            s.send(Request())
        self.assertEqual(sender.send.call_count, 3)

    def test_async_retry_returns_on_first_success(self):
        fail = failed_response()
        success = ok_response()
        sender = mock_sender(fail, fail, success, fail, is_async=True)

        s = RetryingSender(retries=5, sender=sender)
        with patch('tekore.sender.asyncio', AsyncMock()):
            run(s.send(Request()))
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

    def test_async_rate_limited_retry_doesnt_decrease_retry_count(self):
        fail = failed_response()
        rate = rate_limit_response()
        success = ok_response()
        sender = mock_sender(fail, rate, fail, success, is_async=True)

        s = RetryingSender(retries=2, sender=sender)
        with patch('tekore.sender.asyncio', AsyncMock()):
            run(s.send(Request()))

        self.assertEqual(sender.send.call_count, 4)
