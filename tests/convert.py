import pytest

from tekore import (
    ConversionError,
    IdentifierType,
    check_id,
    check_type,
    from_uri,
    from_url,
    to_uri,
    to_url,
)


class TestCheckID:
    def test_valid(self):
        check_id("Base62string")

    def test_empty(self):
        with pytest.raises(ConversionError):
            check_id("")

    def test_punctuation(self):
        with pytest.raises(ConversionError):
            check_id(".")

    def test_almost_b62(self):
        with pytest.raises(ConversionError):
            check_id("almost-base62")

    def test_umlaut(self):
        with pytest.raises(ConversionError):
            check_id("withföreignlëtters")


class TestCheckType:
    def test_valid(self):
        for t in ("artist", "album", "episode", "playlist", "show", "track", "user"):
            check_type(t)

    def test_invalid(self):
        with pytest.raises(ConversionError):
            check_type("invalid")

    def test_identifier_type_instance(self):
        check_type(IdentifierType.album)


class TestToURI:
    def test_valid(self):
        assert to_uri("track", "b62") == "spotify:track:b62"

    def test_user_non_b62(self):
        assert to_uri("user", "a#a") == "spotify:user:a#a"


class TestToURL:
    def test_valid(self):
        url = "https://open.spotify.com/track/b62"
        assert to_url("track", "b62") == url

    def test_user_non_b62_hash_replaced(self):
        url = "https://open.spotify.com/user/a%23a"
        assert to_url("user", "a#a") == url


class TestFromURI:
    def test_valid(self):
        t, i = from_uri("spotify:track:b62")
        assert t == "track"
        assert i == "b62"

    def test_invalid_id(self):
        with pytest.raises(ConversionError):
            from_uri("spotify:track:n_b62")

    def test_invalid_type(self):
        with pytest.raises(ConversionError):
            from_uri("spotify:invalid:b62")

    def test_invalid_prefix(self):
        with pytest.raises(ConversionError):
            from_uri("youtube:track:b62")

    def test_totally_invalid(self):
        with pytest.raises(ConversionError):
            from_uri("not-a-valid-uri")

    def test_user_non_b62(self):
        t, i = from_uri("spotify:user:a#a")
        assert t == "user"
        assert i == "a#a"


class TestFromURL:
    @staticmethod
    def _call(url, type_, id_) -> bool:
        t, i = from_url(url)
        return t == type_ and i == id_

    def test_valid(self):
        url = "https://open.spotify.com/track/b62"
        assert self._call(url, "track", "b62")

    def test_user_non_b62(self):
        url = "https://open.spotify.com/user/a%23a"
        assert self._call(url, "user", "a%23a")

    def test_short_prefix(self):
        url = "open.spotify.com/track/b62"
        assert self._call(url, "track", "b62")

    def test_not_secure_prefix(self):
        url = "http://open.spotify.com/track/b62"
        assert self._call(url, "track", "b62")

    def test_invalid_id(self):
        with pytest.raises(ConversionError):
            from_url("http://open.spotify.com/track/n_b62")

    def test_invalid_type(self):
        with pytest.raises(ConversionError):
            from_url("http://open.spotify.com/invalid/b62")

    def test_invalid_prefix(self):
        with pytest.raises(ConversionError):
            from_url("a.suspicious.site/track/b62")

    def test_totally_invalid(self):
        with pytest.raises(ConversionError):
            from_url("not-a-valid-url")

    def test_params_ignored(self):
        url = "https://open.spotify.com/track/b62?si=a101"
        assert self._call(url, "track", "b62")
