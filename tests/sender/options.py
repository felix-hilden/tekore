from unittest import TestCase
from unittest.mock import MagicMock

import tekore as tk


class TestSenderDefaults(TestCase):
    def setUp(self):
        self.old_default_type = tk.default_sender_type
        self.old_default_instance = tk.default_sender_instance
        self.old_default_kwargs = tk.default_requests_kwargs

    def test_modify_default_sender_type(self):
        instance = MagicMock()
        type_mock = MagicMock(return_value=instance)
        tk.default_sender_type = type_mock

        s = tk.Spotify()
        self.assertIs(s.sender, instance)

    def test_modify_default_sender_instance(self):
        instance = MagicMock()
        tk.default_sender_instance = instance

        s = tk.Spotify()
        self.assertIs(s.sender, instance)

    def test_instance_has_precedence_over_type(self):
        instance = MagicMock()
        type_mock = MagicMock(return_value=MagicMock())
        tk.default_sender_type = type_mock
        tk.default_sender_instance = instance

        s = tk.Spotify()
        self.assertIs(s.sender, instance)

    def test_retrying_sender_as_default_type_recurses(self):
        tk.default_sender_type = tk.RetryingSender

        with self.assertRaises(RecursionError):
            tk.RetryingSender()

    def test_default_kwargs_used_if_none_specified(self):
        kwargs = {'arg': 'val'}

        tk.default_requests_kwargs = kwargs
        s = tk.TransientSender()
        self.assertDictEqual(s.requests_kwargs, kwargs)

    def test_default_kwargs_ignored_if_kwargs_specified(self):
        kwargs = {'arg': 'val'}

        tk.default_requests_kwargs = kwargs
        s = tk.TransientSender(kw='value')
        self.assertNotIn('arg', s.requests_kwargs)

    def tearDown(self):
        tk.default_sender_type = self.old_default_type
        tk.default_sender_instance = self.old_default_instance
        tk.default_requests_kwargs = self.old_default_kwargs
