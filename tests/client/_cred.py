import os

from unittest import TestCase, SkipTest
from requests.exceptions import HTTPError

from spotipy.auth import Credentials
from spotipy.util import read_environment
from spotipy.client import Spotify


class TestCaseWithCredentials(TestCase):
    @classmethod
    def setUpClass(cls):
        id_, secret, redirect = read_environment()
        if any(i is None for i in (id_, secret, redirect)):
            raise SkipTest('No application credentials!')

        cls.client_id = id_
        cls.client_secret = secret
        cls.redirect_uri = redirect

        cls.cred = Credentials(id_, secret, redirect)

        try:
            cls.app_token = cls.cred.request_client_token()
        except HTTPError as e:
            raise SkipTest('Error in retrieving application token!') from e


class TestCaseWithUserCredentials(TestCaseWithCredentials):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        refresh = os.getenv('SPOTIPY_USER_REFRESH', None)
        if refresh is None:
            raise SkipTest('No user credentials!')

        try:
            cls.user_token = cls.cred.request_refreshed_token(refresh)
        except HTTPError as e:
            raise SkipTest('Error in retrieving user token!') from e

        client = Spotify(cls.user_token)

        try:
            cls.current_user_id = client.current_user().id
        except Exception as e:
            print(e)
            raise SkipTest('ID of current user could not be retrieved!') from e
