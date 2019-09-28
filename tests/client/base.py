import unittest
from unittest.mock import MagicMock, patch
from spotipy.client.base import SpotifyBase


class TestSpotifyBase(unittest.TestCase):
    def setUp(self):
        self.client = SpotifyBase('token')

    def test_token_equals_given_token(self):
        self.assertEqual(self.client.token, 'token')

    def test_token_assignable(self):
        self.client.token = 'new'
        self.assertEqual(self.client.token, 'new')

    def test_token_equals_str_of_given_value(self):
        self.client.token = 1
        self.assertEqual(self.client.token, '1')

    def test_new_token_used_in_context(self):
        with self.client.token_as('new'):
            self.assertEqual(self.client.token, 'new')

    def test_old_token_restored_after_context(self):
        with self.client.token_as('new'):
            pass
        self.assertEqual(self.client.token, 'token')

    def test_next_with_no_next_set_returns_none(self):
        paging = MagicMock()
        paging.next = None

        next_ = self.client.next(paging)
        self.assertIsNone(next_)

    def test_previous_with_no_previous_set_returns_none(self):
        paging = MagicMock()
        paging.previous = None

        previous = self.client.previous(paging)
        self.assertIsNone(previous)

    def test_next_returns_next_set(self):
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {'msg': 'ok'}

        sender = MagicMock()
        sender.send.return_value = response

        paging = MagicMock()
        paging.next = 'http://example.com'

        self.client.sender = sender
        paging_mock = MagicMock()
        type_mock = MagicMock(return_value=paging_mock)
        with patch('spotipy.client.base.type', type_mock):
            self.client.next(paging)

        with self.subTest('Paging type used'):
            type_mock.assert_called_with(paging)

        with self.subTest('Paging model constructed'):
            paging_mock.assert_called_with(msg='ok')

    def test_previous_returns_previous_set(self):
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {'msg': 'ok'}

        sender = MagicMock()
        sender.send.return_value = response

        paging = MagicMock()
        paging.previous = 'http://example.com'

        self.client.sender = sender
        paging_mock = MagicMock()
        type_mock = MagicMock(return_value=paging_mock)
        with patch('spotipy.client.base.type', type_mock):
            self.client.previous(paging)

        with self.subTest('Paging type used'):
            type_mock.assert_called_with(paging)

        with self.subTest('Paging model constructed'):
            paging_mock.assert_called_with(msg='ok')
