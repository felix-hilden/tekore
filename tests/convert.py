import pytest
from tekore import (
    check_id,
    check_type,
    ConversionError,
    to_url,
    to_uri,
    from_url,
    from_uri,
    IdentifierType,
)


class TestCheckID:
    def test_valid(self):
        check_id('Base62string')

    def test_empty(self):
        with pytest.raises(ConversionError):
            check_id('')

    def test_punctuation(self):
        with pytest.raises(ConversionError):
            check_id('.')

    def test_almost_b62(self):
        with pytest.raises(ConversionError):
            check_id('almost-base62')

    def test_umlaut(self):
        with pytest.raises(ConversionError):
            check_id('withföreignlëtters')


class TestCheckType:
    def test_valid(self):
        for t in ('artist', 'album', 'playlist', 'track'):
            check_type(t)

    def test_invalid(self):
        with pytest.raises(ConversionError):
            check_type('invalid')

    def test_identifier_type_instance(self):
        check_type(IdentifierType.album)


class TestToURI:
    def test_valid(self):
        assert to_uri('track', 'b62') == 'spotify:track:b62'


class TestToURL:
    def test_valid(self):
        url = 'https://open.spotify.com/track/b62'
        assert to_url('track', 'b62') == url


class TestFromURI:
    @staticmethod
    def _call(uri, type_, id_) -> bool:
        t, i = from_uri(uri)
        return t == type_ and i == id_

    def test_valid(self):
        assert self._call('spotify:track:b62', 'track', 'b62') is True

    def test_invalid_id(self):
        with pytest.raises(ConversionError):
            self._call('spotify:track:n_b62', 'track', 'n_b62')

    def test_invalid_type(self):
        with pytest.raises(ConversionError):
            self._call('spotify:invalid:b62', 'invalid', 'b62')

    def test_invalid_prefix(self):
        with pytest.raises(ConversionError):
            self._call('youtube:track:b62', 'track', 'b62')


class TestFromURL:
    @staticmethod
    def _call(url, type_, id_) -> bool:
        t, i = from_url(url)
        return t == type_ and i == id_

    def test_valid(self):
        url = 'https://open.spotify.com/track/b62'
        assert self._call(url, 'track', 'b62') is True

    def test_short_prefix(self):
        url = 'open.spotify.com/track/b62'
        assert self._call(url, 'track', 'b62') is True

    def test_not_secure_prefix(self):
        url = 'http://open.spotify.com/track/b62'
        assert self._call(url, 'track', 'b62') is True

    def test_invalid_id(self):
        url = 'http://open.spotify.com/track/n_b62'
        with pytest.raises(ConversionError):
            self._call(url, 'track', 'n_b62')

    def test_invalid_type(self):
        url = 'http://open.spotify.com/invalid/b62'
        with pytest.raises(ConversionError):
            self._call(url, 'invalid', 'b62')

    def test_invalid_prefix(self):
        url = 'a.suspicious.site/track/b62'
        with pytest.raises(ConversionError):
            self._call(url, 'track', 'b62')
