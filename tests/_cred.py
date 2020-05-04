"""
Base classes for tests that require application or user credentials.
"""

import os
import tekore as tk

from unittest import TestCase, SkipTest

skip_is_fail = os.getenv('TEKORE_TEST_SKIP_IS_FAIL', None)


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

        cred = tk.config_from_environment()
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

        cls.user_refresh = os.getenv('SPOTIFY_USER_REFRESH', None)
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

        cls.cred = tk.Credentials(
            cls.client_id,
            cls.client_secret,
            cls.redirect_uri
        )

        try:
            cls.app_token = cls.cred.request_client_token()
        except tk.HTTPError as error:
            skip_or_fail(
                tk.HTTPError,
                'Error in retrieving application token!',
                error
            )

        sender = tk.RetryingSender(sender=tk.PersistentSender())
        cls.client = tk.Spotify(cls.app_token, sender=sender)


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
        except tk.HTTPError as error:
            skip_or_fail(
                tk.HTTPError,
                'Error in retrieving user token!',
                error
            )

        cls.client.token = cls.user_token

        try:
            cls.current_user_id = cls.client.current_user().id
        except tk.HTTPError as error:
            skip_or_fail(
                tk.HTTPError,
                'ID of current user could not be retrieved!',
                error
            )
