import pytest
from unittest.mock import MagicMock, patch

from httpx import AsyncClient
from requests import Request
from tekore._sender import (
    TransientSender,
    AsyncTransientSender,
    PersistentSender,
    AsyncPersistentSender,
    SingletonSender,
    AsyncSingletonSender,
)

from tests._util import AsyncMock


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


module = 'tekore._sender.concrete'


class TestSingletonSender:
    def test_instances_share_session(self):
        s1 = SingletonSender()
        s2 = SingletonSender()
        assert s1.session is s2.session

    def test_async_instances_share_client(self):
        s1 = AsyncSingletonSender()
        s2 = AsyncSingletonSender()
        assert s1.client is s2.client

    def test_request_prepared(self):
        mock = MockSessionFactory()
        with patch(module + '.SingletonSender.session', mock()):
            s = SingletonSender()
            r = Request()
            s.send(r)
            mock.instances[0].prepare_request.assert_called_with(r)

    def test_keywords_passed_to_session(self):
        mock = MockSessionFactory()
        kwargs = dict(k1='k1', k2='k2')
        with patch(module + '.SingletonSender.session', mock()):
            s = SingletonSender(**kwargs)
            r = Request()
            s.send(r)
            mock.instances[0].send.assert_called_with(
                mock.prepare_return,
                **kwargs
            )

    @pytest.mark.asyncio
    async def test_async_keywords_passed_to_client(self):
        # Test via raising from incorrect arguments
        s = AsyncSingletonSender(not_an_argument='raises')
        with pytest.raises(TypeError):
            await s.send(Request())


def _test_request_prepared(sender_type):
    mock = MockSessionFactory()
    with patch(module + '.Session', mock):
        s = sender_type()
        r = Request()
        s.send(r)
        mock.instances[0].prepare_request.assert_called_with(r)


def _test_keywords_passed_to_session(sender_type):
    mock = MockSessionFactory()
    kwargs = dict(k1='k1', k2='k2')
    with patch(module + '.Session', mock):
        s = sender_type(**kwargs)
        s.send(Request())
        mock.instances[0].send.assert_called_with(mock.prepare_return, **kwargs)


class TestPersistentSender:
    @patch(module + '.Session', MagicMock)
    def test_session_is_reused(self):
        s = PersistentSender()
        sess1 = s.session
        s.send(Request())
        s.send(Request())
        sess2 = s.session
        assert sess1 is sess2

    @pytest.mark.asyncio
    async def test_async_client_is_reused(self):
        mock = AsyncMock()

        with patch(module + '.AsyncClient.request', mock):
            s = AsyncPersistentSender()
            c1 = s.client
            await s.send(Request())
            await s.send(Request())
            c2 = s.client
            assert c1 is c2

    def test_instances_dont_share_session(self):
        s1 = PersistentSender()
        s2 = PersistentSender()
        assert s1.session is not s2.session

    def test_async_instances_dont_share_client(self):
        s1 = AsyncPersistentSender()
        s2 = AsyncPersistentSender()
        assert s1.client is not s2.client

    def test_request_prepared(self):
        _test_request_prepared(PersistentSender)

    def test_keywords_passed_to_session(self):
        _test_keywords_passed_to_session(PersistentSender)

    @pytest.mark.asyncio
    async def test_async_keywords_passed_to_client(self):
        # Test via raising from incorrect arguments
        s = AsyncPersistentSender(not_an_argument='raises')
        with pytest.raises(TypeError):
            await s.send(Request())


class TestTransientSender:
    def test_session_is_not_reused(self):
        mock = MockSessionFactory()
        with patch(module + '.Session', mock):
            s = TransientSender()
            s.send(Request())
            s.send(Request())
            assert len(mock.instances) == 2

    @pytest.mark.asyncio
    async def test_async_client_is_not_reused(self):
        client = AsyncClient()
        client.request = AsyncMock()
        mock = MagicMock(return_value=client)
        with patch(module + '.AsyncClient', mock):
            s = AsyncTransientSender()
            await s.send(Request())
            await s.send(Request())
            assert mock.call_count == 2

    def test_request_prepared(self):
        _test_request_prepared(TransientSender)

    def test_keywords_passed_to_session(self):
        _test_keywords_passed_to_session(TransientSender)

    @pytest.mark.asyncio
    async def test_async_keywords_passed_to_client(self):
        s = AsyncTransientSender(not_an_argument='raises')
        with pytest.raises(TypeError):
            await s.send(Request())
