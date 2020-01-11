from spotipy.model import PublicUser, PrivateUser
from spotipy.client.base import SpotifyBase


class SpotifyUser(SpotifyBase):
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
        json = self._get('users/' + user_id)
        return PublicUser(**json)

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
        json = self._get('me/')
        return PrivateUser(**json)
