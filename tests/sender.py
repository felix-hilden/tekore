import unittest

from unittest.mock import patch, MagicMock
from requests import Request
from spotipy.sender import Sender, TransientSender, SingletonSender, PersistentSender


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
        with patch('spotipy.sender.SingletonSender.session', mock()):
            s = SingletonSender()
            r = Request()
            s.send(r)
            mock.instances[0].prepare_request.assert_called_with(r)

    def test_keywords_passed_to_session(self):
        mock = MockSessionFactory()
        kwargs = dict(k1='k1', k2='k2')
        with patch('spotipy.sender.SingletonSender.session', mock()):
            s = SingletonSender()
            r = Request()
            s.send(r, **kwargs)
            mock.instances[0].send.assert_called_with(
                mock.prepare_return,
                **kwargs
            )


def test_request_prepared(sender_type):
    mock = MockSessionFactory()
    with patch('spotipy.sender.Session', mock):
        s = sender_type()
        r = Request()
        s.send(r)
        mock.instances[0].prepare_request.assert_called_with(r)


def test_keywords_passed_to_session(sender_type):
    mock = MockSessionFactory()
    kwargs = dict(k1='k1', k2='k2')
    with patch('spotipy.sender.Session', mock):
        s = sender_type()
        s.send(Request(), **kwargs)
        mock.instances[0].send.assert_called_with(mock.prepare_return, **kwargs)


class TestPersistentSender(unittest.TestCase):
    @patch('spotipy.sender.Session', MagicMock)
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
        with patch('spotipy.sender.Session', mock):
            s = TransientSender()
            s.send(Request())
            s.send(Request())
            self.assertEqual(len(mock.instances), 2)

    def test_request_prepared(self):
        test_request_prepared(TransientSender)

    def test_keywords_passed_to_session(self):
        test_keywords_passed_to_session(TransientSender)


if __name__ == '__main__':
    unittest.main()
