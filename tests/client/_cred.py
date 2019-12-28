from unittest import TestCase, SkipTest
from requests.exceptions import HTTPError

from spotipy.auth import Credentials
from spotipy.util import credentials_from_environment, read_environment
from spotipy.client import Spotify

skip_is_fail, = read_environment('SPOTIPY_TEST_SKIP_IS_FAIL')


def skip_or_fail(ex_type: type, msg: str, ex: Exception = None):
    """
    Skip or fail test execution based on environment.
    """
    err = ex_type if skip_is_fail else SkipTest
    if ex is None:
        raise err(msg)
    else:
        raise err(msg) from ex


class TestCaseWithCredentials(TestCase):
    @classmethod
    def setUpClass(cls):
        id_, secret, redirect = credentials_from_environment()
        if any(i is None for i in (id_, secret, redirect)):
            skip_or_fail(KeyError, 'No application credentials!')

        cls.client_id = id_
        cls.client_secret = secret
        cls.redirect_uri = redirect

        cls.cred = Credentials(id_, secret, redirect)

        try:
            cls.app_token = cls.cred.request_client_token()
        except HTTPError as e:
            skip_or_fail(HTTPError, 'Error in retrieving application token!', e)


class TestCaseWithUserCredentials(TestCaseWithCredentials):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        refresh = read_environment('SPOTIPY_USER_REFRESH')
        if refresh is None:
            skip_or_fail(KeyError, 'No application credentials!')

        try:
            cls.user_token = cls.cred.request_refreshed_token(refresh)
        except HTTPError as e:
            skip_or_fail(HTTPError, 'Error in retrieving user token!', e)

        client = Spotify(cls.user_token)

        try:
            cls.current_user_id = client.current_user().id
        except HTTPError as e:
            skip_or_fail(
                HTTPError,
                'ID of current user could not be retrieved!',
                e
            )
