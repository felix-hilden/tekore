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


class TestCaseWithAppEnvironment(TestCase):
    """
    Test case that retrieves application credentials from the environment.
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cred = credentials_from_environment()
        if any(i is None for i in cred):
            skip_or_fail(KeyError, 'No application credentials!')

        cls.client_id, cls.client_secret, cls.redirect_uri = cred


class TestCaseWithUserEnvironment(TestCase):
    """
    Test case that retrieves user credentials from the environment.
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user_refresh, = read_environment('SPOTIPY_USER_REFRESH')
        if cls.user_refresh is None:
            skip_or_fail(KeyError, 'No application credentials!')


class TestCaseWithEnvironment(
    TestCaseWithAppEnvironment,
    TestCaseWithUserEnvironment
):
    """
    Test case that retrieves both application and user credentials
    from the environment.
    """


class TestCaseWithCredentials(TestCaseWithAppEnvironment):
    """
    Test case that provides an application token based on the environment.
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.cred = Credentials(
            cls.client_id,
            cls.client_secret,
            cls.redirect_uri
        )

        try:
            cls.app_token = cls.cred.request_client_token()
        except HTTPError as e:
            skip_or_fail(HTTPError, 'Error in retrieving application token!', e)


class TestCaseWithUserCredentials(
    TestCaseWithCredentials,
    TestCaseWithUserEnvironment
):
    """
    Test case that provides both application and user tokens.
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        try:
            cls.user_token = cls.cred.refresh_user_token(cls.user_refresh)
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
