import unittest

from spotipy.convert import (
    check_id, check_type, ConversionError,
    to_url, to_uri, from_url, from_uri
)


class TestCheckID(unittest.TestCase):
    def test_valid(self):
        check_id('Base62string')

    def test_empty(self):
        with self.assertRaises(ConversionError):
            check_id('')

    def test_punctuation(self):
        with self.assertRaises(ConversionError):
            check_id('.')

    def test_almost_b62(self):
        with self.assertRaises(ConversionError):
            check_id('almost-base62')

    def test_umlaut(self):
        with self.assertRaises(ConversionError):
            check_id('withföreignlëtters')


class TestCheckType(unittest.TestCase):
    def test_valid(self):
        for t in ('artist', 'album', 'track'):
            with self.subTest(f'Type: {t}'):
                check_type(t)

    def test_invalid(self):
        with self.assertRaises(ConversionError):
            check_type('invalid')


class TestToURI(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(to_uri('track', 'b62'), 'spotify:track:b62')


class TestToURL(unittest.TestCase):
    def test_valid(self):
        url = 'http://open.spotify.com/track/b62'
        self.assertEqual(to_url('track', 'b62'), url)


class TestFromURI(unittest.TestCase):
    @staticmethod
    def _call(uri, type_, id_) -> bool:
        t, i = from_uri(uri)
        return t == type_ and i == id_

    def test_valid(self):
        self.assertTrue(self._call('spotify:track:b62', 'track', 'b62'))

    def test_invalid_id(self):
        with self.assertRaises(ConversionError):
            self._call('spotify:track:n_b62', 'track', 'n_b62')

    def test_invalid_type(self):
        with self.assertRaises(ConversionError):
            self._call('spotify:invalid:b62', 'invalid', 'b62')

    def test_invalid_prefix(self):
        with self.assertRaises(ConversionError):
            self._call('youtube:track:b62', 'track', 'b62')


class TestFromURL(unittest.TestCase):
    @staticmethod
    def _call(url, type_, id_) -> bool:
        t, i = from_url(url)
        return t == type_ and i == id_

    def test_valid(self):
        url = 'http://open.spotify.com/track/b62'
        self.assertTrue(self._call(url, 'track', 'b62'))

    def test_short_prefix(self):
        url = 'open.spotify.com/track/b62'
        self.assertTrue(self._call(url, 'track', 'b62'))

    def test_invalid_id(self):
        url = 'http://open.spotify.com/track/n_b62'
        with self.assertRaises(ConversionError):
            self._call(url, 'track', 'n_b62')

    def test_invalid_type(self):
        url = 'http://open.spotify.com/invalid/b62'
        with self.assertRaises(ConversionError):
            self._call(url, 'invalid', 'b62')

    def test_invalid_prefix(self):
        url = 'a.suspicious.site/track/b62'
        with self.assertRaises(ConversionError):
            self._call(url, 'track', 'b62')


if __name__ == '__main__':
    unittest.main()
