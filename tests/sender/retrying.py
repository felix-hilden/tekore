from unittest.mock import MagicMock, patch

import pytest

from tekore import Request, RetryingSender
from tests._util import AsyncMock


def mock_request():
    return Request("GET", "url.com")


def ok_response() -> MagicMock:
    response = MagicMock()
    response.status_code = 200
    return response


def rate_limit_response(retry_after: int = 1) -> MagicMock:
    response = MagicMock()
    response.status_code = 429
    response.headers = {"Retry-After": retry_after}
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


module = "tekore._sender.extending"


class TestRetryingSender:
    def test_repr(self):
        s = RetryingSender()
        assert repr(s).startswith("RetryingSender(")

    def test_rate_limited_request_retried_after_set_seconds(self):
        time = MagicMock()
        fail = rate_limit_response()
        success = ok_response()
        sender = mock_sender(fail, success)

        s = RetryingSender(sender=sender)
        with patch(module + ".time", time):
            s.send(mock_request())
            time.sleep.assert_called_once_with(1 + 1)

    @pytest.mark.asyncio
    async def test_async_rate_limited_request_retried_after_set_seconds(self):
        asyncio = AsyncMock()
        fail = rate_limit_response()
        success = ok_response()
        sender = mock_sender(fail, success, is_async=True)

        s = RetryingSender(sender=sender)
        with patch(module + ".asyncio", asyncio):
            await s.send(mock_request())
            asyncio.sleep.assert_called_once_with(1 + 1)

    def test_default_retry_after_is_one(self):
        time = MagicMock()
        fail = rate_limit_response()
        del fail.headers["Retry-After"]
        success = ok_response()
        sender = mock_sender(fail, success)

        s = RetryingSender(sender=sender)
        with patch(module + ".time", time):
            s.send(mock_request())
            time.sleep.assert_called_once_with(1 + 1)

    @pytest.mark.asyncio
    async def test_async_default_retry_after_is_one(self):
        asyncio = AsyncMock()
        fail = rate_limit_response()
        del fail.headers["Retry-After"]
        success = ok_response()
        sender = mock_sender(fail, success, is_async=True)

        s = RetryingSender(sender=sender)
        with patch(module + ".asyncio", asyncio):
            await s.send(mock_request())
            asyncio.sleep.assert_called_once_with(1 + 1)

    def test_failing_request_but_no_retries_returns_failed(self):
        fail = failed_response()
        success = ok_response()
        sender = mock_sender(fail, success)
        s = RetryingSender(sender=sender)
        r = s.send(mock_request())
        assert r is fail

    @pytest.mark.asyncio
    async def test_async_failing_request_but_no_retries_returns_failed(self):
        fail = failed_response()
        success = ok_response()
        sender = mock_sender(fail, success, is_async=True)
        s = RetryingSender(sender=sender)
        r = await s.send(mock_request())
        assert r is fail

    def test_failing_request_retried_max_times(self):
        fail = failed_response()
        success = ok_response()
        sender = mock_sender(fail, fail, fail, success)

        s = RetryingSender(retries=2, sender=sender)
        with patch(module + ".time", MagicMock()):
            s.send(mock_request())
        assert sender.send.call_count == 3

    @pytest.mark.asyncio
    async def test_async_failing_request_retried_max_times(self):
        fail = failed_response()
        success = ok_response()
        sender = mock_sender(fail, fail, fail, success, is_async=True)

        s = RetryingSender(retries=2, sender=sender)
        with patch(module + ".asyncio", AsyncMock()):
            await s.send(mock_request())
        assert sender.send.call_count == 3

    def test_retry_returns_on_first_success(self):
        fail = failed_response()
        success = ok_response()
        sender = mock_sender(fail, fail, success, fail, success)

        s = RetryingSender(retries=5, sender=sender)
        with patch(module + ".time", MagicMock()):
            s.send(mock_request())
        assert sender.send.call_count == 3

    @pytest.mark.asyncio
    async def test_async_retry_returns_on_first_success(self):
        fail = failed_response()
        success = ok_response()
        sender = mock_sender(fail, fail, success, fail, is_async=True)

        s = RetryingSender(retries=5, sender=sender)
        with patch(module + ".asyncio", AsyncMock()):
            await s.send(mock_request())
        assert sender.send.call_count == 3

    def test_rate_limited_retry_doesnt_decrease_retry_count(self):
        fail = failed_response()
        rate = rate_limit_response()
        success = ok_response()
        sender = mock_sender(fail, rate, fail, success)

        s = RetryingSender(retries=2, sender=sender)
        with patch(module + ".time", MagicMock()):
            s.send(mock_request())

        assert sender.send.call_count == 4

    @pytest.mark.asyncio
    async def test_async_rate_limited_retry_doesnt_decrease_retry_count(self):
        fail = failed_response()
        rate = rate_limit_response()
        success = ok_response()
        sender = mock_sender(fail, rate, fail, success, is_async=True)

        s = RetryingSender(retries=2, sender=sender)
        with patch(module + ".asyncio", AsyncMock()):
            await s.send(mock_request())

        assert sender.send.call_count == 4
