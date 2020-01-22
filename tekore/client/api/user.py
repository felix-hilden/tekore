from tekore.model import PublicUser, PrivateUser
from tekore.client.process import single
from tekore.client.base import SpotifyBase, send_and_process


class SpotifyUser(SpotifyBase):
    @send_and_process(single(PublicUser))
    def user(self, user_id: str) -> PublicUser:
        """
        Get a user's profile.

        Parameters
        ----------
        user_id
            user ID

        Returns
        -------
        PublicUser
            public user information
        """
        return self._get('users/' + user_id)

    @send_and_process(single(PrivateUser))
    def current_user(self) -> PrivateUser:
        """
        Get current user's profile.

        Requires the user-read-private scope to return
        user's country and product subscription level.
        Requires the user-read-email scope to return user's email.

        Returns
        -------
        PrivateUser
            private user information
        """
        return self._get('me/')
