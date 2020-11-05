import pytest

from ._resources import episode_id, episode_ids
from tekore import HTTPError


class TestSpotifyEpisode:
    def test_episode_not_found_without_market(self, app_client):
        """
        Evaluate an episode.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        with pytest.raises(HTTPError):
            app_client.episode(episode_id)

    def test_episode_found_with_market(self, app_client):
        """
        Set an episode for an episode.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        episode = app_client.episode(episode_id, market='FI')
        assert episode.id == episode_id

    def test_resume_point_is_none(self, app_client):
        """
        Return true if the episode.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        episode = app_client.episode(episode_id, market='FI')
        assert episode.resume_point is None

    def test_episodes(self, app_client):
        """
        Test for a list of epochs.

        Args:
            self: (todo): write your description
            app_client: (todo): write your description
        """
        episodes = app_client.episodes(episode_ids, market='FI')
        assert episode_ids == [e.id for e in episodes]

    def test_found_without_market(self, user_client):
        """
        Set the user_id for a particular user.

        Args:
            self: (todo): write your description
            user_client: (todo): write your description
        """
        episode = user_client.episode(episode_id)
        assert episode.id == episode_id

    def test_resume_point_exists(self, user_client):
        """
        Resume a episode point.

        Args:
            self: (todo): write your description
            user_client: (todo): write your description
        """
        episode = user_client.episode(episode_id)
        assert episode.resume_point is not None
