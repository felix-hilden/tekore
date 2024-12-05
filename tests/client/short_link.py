import pytest

from tekore import from_url, is_short_link

from ._resources import short_link, track_id


class TestSpotifyShortLink:
    def test_random_string_is_not_short_link(self):
        assert not is_short_link("asdf")

    def test_random_url_is_not_short_link(self):
        assert not is_short_link("https://spotify.org/resource")

    def test_valid_short_link(self):
        assert is_short_link("https://spotify.link/resource")

    def test_short_link_does_not_need_https(self):
        assert is_short_link("spotify.link/resource")


@pytest.mark.api
class TestSpotifyShortLinkOnline:
    def test_follow_short_link(self, app_client):
        resolved = app_client.follow_short_link(short_link)
        assert short_link != resolved
        from_url(resolved)

    @pytest.mark.asyncio
    async def test_async_follow_short_link(self, app_aclient):
        resolved = await app_aclient.follow_short_link(short_link)
        assert short_link != resolved
        from_url(resolved)

    def test_follow_short_link_already_resolved(self, app_client):
        link = "https://open.spotify.com/track/" + track_id
        resolved = app_client.follow_short_link(link)
        assert link == resolved
        from_url(resolved)

    def test_follow_short_link_does_not_authorise(self, app_client, httpx_mock):
        httpx_mock.add_response(200)
        app_client.follow_short_link(short_link)
        (request,) = httpx_mock.get_requests()
        assert "authorization" not in request.headers
