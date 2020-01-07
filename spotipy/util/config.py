"""
Config provides convenient ways of importing application credentials.

.. code:: python

    from spotipy.util import config_from_environment, config_from_file

    client_id, client_secret, redirect_uri = config_from_environment()
    client_id, client_secret, redirect_uri = config_from_file(filename)

By default, only client ID, client secret and redirect URI is returned.
To return a user's refresh token as well, set a boolean flag.

.. code:: python

    id_, secret, uri, refresh = config_from_environment(return_refresh=True)

Values are read from preset names, which can be changed.
Note that changing values requires importing the whole config module.

.. code:: python

    from spotipy.util import config

    config.client_id_var = 'your_id_name'
    config.client_secret_var = 'your_secret_name'
    config.redirect_uri_var = 'your_uri_name'
    config.user_refresh_var = 'your_refresh_name'
"""

import os
import configparser

client_id_var: str = 'SPOTIPY_CLIENT_ID'
"""Configuration variable name for a client ID."""

client_secret_var: str = 'SPOTIPY_CLIENT_SECRET'
"""Configuration variable name for a client secret."""

redirect_uri_var: str = 'SPOTIPY_REDIRECT_URI'
"""Configuration variable name for a redirect URI."""

user_refresh_var: str = 'SPOTIPY_USER_REFRESH'
"""Configuration variable name for a user refresh token."""


def _read_configuration(conf: dict, return_refresh: bool = False) -> tuple:
    """
    Read variables from dictionary.

    Parameters
    ----------
    conf
        dictionary to read from
    return_refresh
        return user refresh token

    Returns
    -------
    tuple
        (client ID, client secret, redirect URI), None if not found.
        If return_refresh is True, also return user refresh token.
    """
    variables = (client_id_var, client_secret_var, redirect_uri_var)

    if return_refresh:
        variables += (user_refresh_var,)

    return tuple(conf.get(var, None) for var in variables)


def config_from_environment(return_refresh: bool = False) -> tuple:
    """
    Read application credentials from environment variables.

    Environment variables are read according to
    names set in :class:`spotipy.util.config`.

    Parameters
    ----------
    return_refresh
        return user refresh token

    Returns
    -------
    tuple
        (client ID, client secret, redirect URI), None if not found.
        If return_refresh is True, also return user refresh token.
    """
    return _read_configuration(os.environ, return_refresh)


def config_from_file(
        file_path: str,
        section: str = 'DEFAULT',
        return_refresh: bool = False
) -> tuple:
    """
    Read application credentials from a config file.

    The configuration must be in INI format
    as accepted by :class:`configparser.ConfigParser`.
    Configuration variables are read according to
    names set in :class:`spotipy.util.config`.

    Parameters
    ----------
    file_path
        path of the file containing the credential variables
    section
        name of the section to read variables from
    return_refresh
        return user refresh token

    Returns
    -------
    tuple
        (client ID, client secret, redirect URI), None if not found.
        If return_refresh is True, also return user refresh token.
    """
    c = configparser.ConfigParser()
    c.optionxform = str
    with open(file_path, 'r') as f:
        c.read_file(f)

    return _read_configuration(c[section], return_refresh)
