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
        """
        Checks if the test is valid.

        Args:
            self: (todo): write your description
        """
        check_id('Base62string')

    def test_empty(self):
        """
        Check if the test is empty.

        Args:
            self: (todo): write your description
        """
        with pytest.raises(ConversionError):
            check_id('')

    def test_punctuation(self):
        """
        Check if all punctuation is allowed.

        Args:
            self: (todo): write your description
        """
        with pytest.raises(ConversionError):
            check_id('.')

    def test_almost_b62(self):
        """
        Test if the test b62 version of the b62.

        Args:
            self: (todo): write your description
        """
        with pytest.raises(ConversionError):
            check_id('almost-base62')

    def test_umlaut(self):
        """
        Check if the test is enabled.

        Args:
            self: (todo): write your description
        """
        with pytest.raises(ConversionError):
            check_id('withföreignlëtters')


class TestCheckType:
    def test_valid(self):
        """
        Check that the test types.

        Args:
            self: (todo): write your description
        """
        for t in ('artist', 'album', 'playlist', 'track'):
            check_type(t)

    def test_invalid(self):
        """
        Check if the test is in the test.

        Args:
            self: (todo): write your description
        """
        with pytest.raises(ConversionError):
            check_type('invalid')

    def test_identifier_type_instance(self):
        """
        The identifier of the identifier is_type of the identifier.

        Args:
            self: (todo): write your description
        """
        check_type(IdentifierType.album)


class TestToURI:
    def test_valid(self):
        """
        È¿ķåľŀè¿ĳ»åĭ¨

        Args:
            self: (todo): write your description
        """
        assert to_uri('track', 'b62') == 'spotify:track:b62'


class TestToURL:
    def test_valid(self):
        """
        Checks that the test.

        Args:
            self: (todo): write your description
        """
        url = 'https://open.spotify.com/track/b62'
        assert to_url('track', 'b62') == url


class TestFromURI:
    @staticmethod
    def _call(uri, type_, id_) -> bool:
        """
        Call the given uri.

        Args:
            uri: (str): write your description
            type_: (todo): write your description
            id_: (str): write your description
        """
        t, i = from_uri(uri)
        return t == type_ and i == id_

    def test_valid(self):
        """
        Perform test test test.

        Args:
            self: (todo): write your description
        """
        assert self._call('spotify:track:b62', 'track', 'b62') is True

    def test_invalid_id(self):
        """
        Check if the test id is valid.

        Args:
            self: (todo): write your description
        """
        with pytest.raises(ConversionError):
            self._call('spotify:track:n_b62', 'track', 'n_b62')

    def test_invalid_type(self):
        """
        Test if the test type of test. pytest.

        Args:
            self: (todo): write your description
        """
        with pytest.raises(ConversionError):
            self._call('spotify:invalid:b62', 'invalid', 'b62')

    def test_invalid_prefix(self):
        """
        Check that the test prefix exists.

        Args:
            self: (todo): write your description
        """
        with pytest.raises(ConversionError):
            self._call('youtube:track:b62', 'track', 'b62')


class TestFromURL:
    @staticmethod
    def _call(url, type_, id_) -> bool:
        """
        Returns a url and return the result.

        Args:
            url: (str): write your description
            type_: (todo): write your description
            id_: (str): write your description
        """
        t, i = from_url(url)
        return t == type_ and i == id_

    def test_valid(self):
        """
        Validate test test test is valid

        Args:
            self: (todo): write your description
        """
        url = 'https://open.spotify.com/track/b62'
        assert self._call(url, 'track', 'b62') is True

    def test_short_prefix(self):
        """
        Get short short prefix.

        Args:
            self: (todo): write your description
        """
        url = 'open.spotify.com/track/b62'
        assert self._call(url, 'track', 'b62') is True

    def test_not_secure_prefix(self):
        """
        Test if the url prefix.

        Args:
            self: (todo): write your description
        """
        url = 'http://open.spotify.com/track/b62'
        assert self._call(url, 'track', 'b62') is True

    def test_invalid_id(self):
        """
        Check if the test id is valid.

        Args:
            self: (todo): write your description
        """
        url = 'http://open.spotify.com/track/n_b62'
        with pytest.raises(ConversionError):
            self._call(url, 'track', 'n_b62')

    def test_invalid_type(self):
        """
        Validate that the test type is valid.

        Args:
            self: (todo): write your description
        """
        url = 'http://open.spotify.com/invalid/b62'
        with pytest.raises(ConversionError):
            self._call(url, 'invalid', 'b62')

    def test_invalid_prefix(self):
        """
        Check for test test prefix.

        Args:
            self: (todo): write your description
        """
        url = 'a.suspicious.site/track/b62'
        with pytest.raises(ConversionError):
            self._call(url, 'track', 'b62')
