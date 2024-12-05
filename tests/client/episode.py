import pytest

from tekore import HTTPError

from ._resources import episode_id, episode_ids


@pytest.mark.api
class TestSpotifyEpisode:
    @pytest.mark.xfail(reason="API inconsistencies.")
    def test_episode_not_found_without_market(self, app_client):
        with pytest.raises(HTTPError):
            app_client.episode(episode_id)

    def test_episode_found_with_market(self, app_client):
        episode = app_client.episode(episode_id, market="FI")
        assert episode.id == episode_id

    def test_resume_point_is_none(self, app_client):
        episode = app_client.episode(episode_id, market="FI")
        assert episode.resume_point is None

    def test_episodes(self, app_client):
        episodes = app_client.episodes(episode_ids, market="FI")
        assert episode_ids == [e.id for e in episodes]

    def test_found_without_market(self, user_client):
        episode = user_client.episode(episode_id)
        assert episode.id == episode_id

    def test_resume_point_exists(self, user_client):
        episode = user_client.episode(episode_id)
        assert episode.resume_point is not None
