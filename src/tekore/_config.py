from __future__ import annotations

from collections.abc import Iterable
from configparser import ConfigParser
from os import environ
from pathlib import Path
from warnings import warn


class MissingConfigurationWarning(RuntimeWarning):
    """Missing value read from configuration."""


def _read_configuration(conf: dict, *, return_refresh: bool = False) -> tuple:
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
    from tekore import (
        client_id_var,
        client_secret_var,
        redirect_uri_var,
        user_refresh_var,
    )

    variables = [client_id_var, client_secret_var, redirect_uri_var]

    if return_refresh:
        variables.append(user_refresh_var)

    values = tuple(conf.get(var) for var in variables)

    for var, val in zip(variables, values):
        if val is None:
            warn(
                f"`{var}` missing! None returned instead.",
                MissingConfigurationWarning,
                stacklevel=3,
            )

    return values


def config_from_environment(return_refresh: bool = False) -> tuple:
    """
    Read configuration from environment variables.

    Parameters
    ----------
    return_refresh
        return user refresh token

    Returns
    -------
    tuple
        (client ID, client secret, redirect URI), None if not found.
        If return_refresh is True, also return user refresh token.

    Raises
    ------
    MissingConfigurationWarning
        when a missing value is encountered

    Examples
    --------
    .. code:: python

        client_id, client_secret, redirect_uri = tk.config_from_environment()

        conf = tk.config_from_environment(return_refresh=True)
        client_id, client_secret, redirect_uri, user_refresh = conf
    """
    return _read_configuration(environ, return_refresh=return_refresh)


def _read_configfile(file_path: str, *, force: bool = True) -> ConfigParser:
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
        with Path(file_path).open() as f:
            c.read_file(f)
    else:
        c.read(file_path)

    return c


def config_from_file(
    file_path: str, section: str = "DEFAULT", return_refresh: bool = False
) -> tuple:
    """
    Read configuration from a config file.

    The configuration must be in INI format
    as accepted by :class:`configparser.ConfigParser`.

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

    Raises
    ------
    MissingConfigurationWarning
        when a missing value is encountered

    Examples
    --------
    .. code:: python

        client_id, client_secret, redirect_uri = tk.config_from_file(filename)

        conf = tk.config_from_file(filename, return_refresh=True)
        client_id, client_secret, redirect_uri, user_refresh = conf
    """
    c = _read_configfile(file_path)
    return _read_configuration(c[section], return_refresh=return_refresh)


def config_to_file(
    file_path: str, values: Iterable | dict, section: str = "DEFAULT"
) -> None:
    """
    Write configuration to a config file.

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
    Pass in an iterable to use the preset variable names.
    The values should be ordered as returned when reading configuration:
    ``client_id, client_secret, redirect_uri, user_refresh``.

    .. code:: python

        conf = (client_id, client_secret, redirect_uri, user_refresh)
        config_to_file(filename, conf)

    A shorter iterable or one containing ``None`` values may be passed.
    Items missing from the end are ignored and ``None`` values are discarded.

    .. code:: python

        # Write partial information
        config_to_file(filename, (client_id, client_secret))

        # Fill the missing configuration
        conf = (None, None, redirect_uri, user_refresh)
        config_to_file(filename, conf)

    A dictionary is also accepted.
    In this case the keys are used instead of preset variable names.

    .. code:: python

        config_to_file(filename, {'REFRESH_TOKEN': refresh_token})
    """
    if isinstance(values, dict):
        val_dict = values
    else:
        from tekore import (
            client_id_var,
            client_secret_var,
            redirect_uri_var,
            user_refresh_var,
        )

        names = (client_id_var, client_secret_var, redirect_uri_var, user_refresh_var)
        val_dict = {
            name: value for name, value in zip(names, values) if value is not None
        }

    c = _read_configfile(file_path, force=False)

    if section not in c:
        c[section] = {}

    c[section].update(val_dict)

    with Path(file_path).open("w") as f:
        c.write(f)
