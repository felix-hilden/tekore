"""
util
====

Utility module for your convenience <3

The main motivation for this module is to make authorisation effortless.
That goal is achieved by three mechanisms:
reading configuration, an automatically refreshing access token and
functions that implement everything needed to retrieve tokens.
The effect is easy configuration, user authorisation and
a strong independent token.

.. code:: python

    from spotipy import util

    conf = util.config_from_environment()
    app_token = util.request_client_token(*conf[:2])
    user_token = util.prompt_for_user_token(*conf)

    # Save the refresh token to avoid authenticating again
    refresh_token = ...     # Load refresh token
    user_token = util.refresh_user_token(*conf[:2], refresh_token)

If you authenticate with a server but would still like to use
:class:`RefreshingToken`, you can use the :class:`RefreshingCredentials`
manager that is used by the functions above to create refreshing tokens.

.. code:: python

    cred = util.RefreshingCredentials(*conf)

    # Client credentials flow
    app_token = cred.request_client_token()

    # Authorisation code flow
    url = cred.user_authorisation_url()
    code = ...  # Redirect user to login and retrieve code
    user_token = cred.request_user_token(code)

    # Reload a token
    user_token = cred.refresh_user_token(refresh_token)

Reading configuration from INI files is also possible.

.. code:: python

    util.config_from_file(filename)

This module exists solely to make developing applications easier.
Some applications might have different needs,
so please do create your own versions of these routines.
Particularly, ``prompt_for_user_token`` opens up a web browser
for the user to log in with, doesn't expose all parameters that are available
when using lower-level functions, and forces the login dialog to be shown.
"""

from spotipy.util.config import (
    config_from_environment,
    config_from_file,
)
from spotipy.util.credentials import (
    parse_code_from_url,
    prompt_for_user_token,
    RefreshingCredentials,
    RefreshingToken,
    refresh_user_token,
    request_client_token,
)
