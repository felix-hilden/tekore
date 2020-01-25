"""
Config provides convenient ways of importing application credentials.

.. code:: python

    from tekore.util import config_from_environment, config_from_file

    client_id, client_secret, redirect_uri = config_from_environment()
    client_id, client_secret, redirect_uri = config_from_file(filename)

By default, only client ID, client secret and redirect URI are returned.
To return a user's refresh token as well, set a boolean flag.

.. code:: python

    id_, secret, uri, refresh = config_from_environment(return_refresh=True)

Values are read from preset names, which can be changed.
Note that changing values requires importing the whole config module.

.. code:: python

    from tekore.util import config

    config.client_id_var = 'your_id_name'
    config.client_secret_var = 'your_secret_name'
    config.redirect_uri_var = 'your_uri_name'
    config.user_refresh_var = 'your_refresh_name'

Configuration can be written to file.

.. code:: python

    config_to_file(filename, (id_, secret, uri, refresh))

When reading configuration, if values are missing,
a :class:`MissingConfigurationWarning` is issued.
It can be disabled via the :mod:`warnings` module.

.. code:: python

    from warnings import simplefilter

    simplefilter('ignore', MissingConfigurationWarning)
"""

from os import environ
from typing import Union, Iterable
from warnings import warn
from configparser import ConfigParser

client_id_var: str = 'SPOTIFY_CLIENT_ID'
"""Configuration variable name for a client ID."""

client_secret_var: str = 'SPOTIFY_CLIENT_SECRET'
"""Configuration variable name for a client secret."""

redirect_uri_var: str = 'SPOTIFY_REDIRECT_URI'
"""Configuration variable name for a redirect URI."""

user_refresh_var: str = 'SPOTIFY_USER_REFRESH'
"""Configuration variable name for a user refresh token."""


class MissingConfigurationWarning(RuntimeWarning):
    """Warning issued when a missing value is read from configuration."""


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

    conf = tuple(conf.get(var, None) for var in variables)

    if any(c is None for c in conf):
        warn(
            'A missing value was encountered in configuration!',
            MissingConfigurationWarning,
            stacklevel=3
        )

    return conf


def config_from_environment(return_refresh: bool = False) -> tuple:
    """
    Read application credentials from environment variables.

    Environment variables are read according to
    names set in :mod:`config <tekore.util.config>`.

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
    return _read_configuration(environ, return_refresh)


def _read_configfile(file_path: str, force: bool = True) -> ConfigParser:
    """
    Read configuration from INI file.

    Parameters
    ----------
    file_path
        path of the configuration file
    force
        force reading of the file, fail if not found
    """
    c = ConfigParser()
    c.optionxform = str

    if force:
        with open(file_path, 'r') as f:
            c.read_file(f)
    else:
        c.read(file_path)

    return c


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
    names set in :mod:`config <tekore.util.config>`.

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
    c = _read_configfile(file_path)
    return _read_configuration(c[section], return_refresh)


def config_to_file(
        file_path: str,
        values: Union[Iterable, dict],
        section: str = 'DEFAULT'
) -> None:
    """
    Write application credentials to a config file.

    Existing configuration is preserved if it's not in conflict.

    Parameters
    ----------
    file_path
        path of the configuration file
    values
        configuration values to write, dict or iterable, see below for examples
    section
        name of the section to write to

    Examples
    --------
    Configuration can be written in different ways.
    Pass in an iterable to use variable names that have been set in
    :mod:`config <tekore.util.config>`.
    The values should be ordered as returned when reading configuration:
    ``client_id, client_secret, redirect_uri, user_refresh``.

    .. code:: python

        config_to_file(filename, (client_id, client_secret, redirect_uri))

    A shorter iterable may be passed.
    It may also contain ``None`` values. They are discarded.

    .. code:: python

        # Write partial information
        config_to_file(filename, (client_id, client_secret))

        # Fill the missing configuration
        conf = (None, None, redirect_uri, user_refresh)
        config_to_file(filename, conf)

    A dictionary is also accepted.
    Default variable names are ignored, and the keys used instead.

    .. code:: python

        config_to_file(filename, {'REFRESH_TOKEN': refresh_token})
    """
    if isinstance(values, dict):
        val_dict = values
    else:
        names = (
            client_id_var,
            client_secret_var,
            redirect_uri_var,
            user_refresh_var
        )
        val_dict = {
            name: value
            for name, value in zip(names, values)
            if value is not None
        }

    c = _read_configfile(file_path, force=False)

    if section not in c:
        c[section] = {}

    c[section].update(val_dict)

    with open(file_path, 'w') as f:
        c.write(f)
