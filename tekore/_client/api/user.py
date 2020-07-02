from ..base import SpotifyBase
from ..decor import send_and_process, scopes
from ..process import single
from tekore._auth import scope
from tekore.model import PublicUser, PrivateUser


class SpotifyUser(SpotifyBase):
    """User API endpoints."""

    @scopes()
    @send_and_process(single(PublicUser))
    def user(self, user_id: str) -> PublicUser:
        """
        Get a user's profile.

        Parameters
        ----------
        user_id
            user ID
        """
        return self._get('users/' + user_id)

    @scopes(optional=[scope.user_read_private, scope.user_read_email])
    @send_and_process(single(PrivateUser))
    def current_user(self) -> PrivateUser:
        """
        Get current user's profile.

        The user-read-private scope allows the user's country and
        product subscription level to be returned.
        """
        return self._get('me/')
