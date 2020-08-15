"""
Fixtures for tests that require application or user credentials.
"""
import os
import pytest
import tekore as tk

from tests._util import handle_warnings

skip_is_fail = os.getenv('TEKORE_TEST_SKIP_IS_FAIL', None)


def skip_or_fail(ex_type: type, msg: str, ex: Exception = None):
    """
    Skip or fail test execution based on environment.
    """
    if skip_is_fail is not None:
        if ex is None:
            raise ex_type(msg)
        else:
            raise ex_type(msg) from ex
    else:
        pytest.skip(msg)


@pytest.fixture(scope='session')
def app_env():
    """
    Retrieves application credentials from the environment.
    """
    cred = tk.config_from_environment()
    if any(i is None for i in cred):
        skip_or_fail(KeyError, 'No application credentials!')

    return cred


@pytest.fixture(scope='session')
def user_refresh():
    """
    Retrieves user credentials from the environment.
    """
    user_refresh = os.getenv('SPOTIFY_USER_REFRESH', None)
    if user_refresh is None:
        skip_or_fail(KeyError, 'No user credentials!')

    return user_refresh


@pytest.fixture(scope='session')
def app_token(app_env):
    """
    Provides an application token based on the environment.
    """
    cred = tk.Credentials(*app_env)

    try:
        return cred.request_client_token()
    except tk.HTTPError as error:
        skip_or_fail(
            tk.HTTPError,
            'Error in retrieving application token!',
            error
        )


@pytest.fixture(scope='session')
def user_token(app_env, user_refresh):
    """
    Provides a user token based on the environment.
    """
    cred = tk.Credentials(*app_env)

    try:
        return cred.refresh_user_token(user_refresh)
    except tk.HTTPError as error:
        skip_or_fail(
            tk.HTTPError,
            'Error in retrieving user token!',
            error
        )


@pytest.fixture(scope='function')
def app_client(app_token):
    """
    Provides a client with an application token.
    """
    sender = tk.RetryingSender(sender=tk.SyncSender())
    return tk.Spotify(app_token, sender=sender)


@pytest.fixture(scope='function')
def user_client(user_token):
    """
    Provides a client with a user token.
    """
    sender = tk.RetryingSender(sender=tk.SyncSender())
    return tk.Spotify(user_token, sender=sender)


@pytest.fixture(scope='class')
def data_client(user_token):
    """
    Provides a client with a user token.
    """
    sender = tk.RetryingSender(sender=tk.SyncSender())
    return tk.Spotify(user_token, sender=sender)


@pytest.fixture(scope='function')
def app_aclient(app_token):
    """
    Provides an asynchronous client with an application token.
    """
    sender = tk.RetryingSender(sender=tk.AsyncSender())
    return tk.Spotify(app_token, sender=sender)


@pytest.fixture(scope='function')
def user_aclient(user_token):
    """
    Provides an asynchronous client with a user token.
    """
    sender = tk.RetryingSender(sender=tk.AsyncSender())
    return tk.Spotify(user_token, sender=sender)


@pytest.fixture(scope='class')
def current_user_id(data_client):
    """
    Provides the user ID of the current user.
    """
    try:
        return data_client.current_user().id
    except tk.HTTPError as error:
        skip_or_fail(
            tk.HTTPError,
            'ID of current user could not be retrieved!',
            error
        )


@pytest.fixture(scope='class')
def suppress_warnings():
    with handle_warnings():
        yield
