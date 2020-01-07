import os
import configparser


def read_environment(*variables: str) -> tuple:
    """
    Read environment variables.

    Parameters
    ----------
    variables
        environment variable names to read

    Returns
    -------
    tuple
        variable values
    """
    return tuple(os.getenv(var, None) for var in variables)


def credentials_from_environment(
        client_id_var: str = 'SPOTIPY_CLIENT_ID',
        client_secret_var: str = 'SPOTIPY_CLIENT_SECRET',
        redirect_uri_var: str = 'SPOTIPY_REDIRECT_URI'
) -> (str, str, str):
    """
    Read credentials from environment variables.

    Parameters
    ----------
    client_id_var
        name of the variable containing a client ID
    client_secret_var
        name of the variable containing a client secret
    redirect_uri_var
        name of the variable containing a redirect URI

    Returns
    -------
    tuple
        (client ID, client secret, redirect URI), None if not found
    """
    return read_environment(client_id_var, client_secret_var, redirect_uri_var)


def read_configfile(*variables: str, config: dict) -> tuple:
    """
    Read variables from a config dict.

    Parameters
    ----------
    variables
        variable names to read
    config
        parsed config dict

    Returns
    -------
    tuple
        variable values
    """
    return tuple(config.get(var, None) for var in variables)


def credentials_from_configfile(
        file_path: str,
        section: str = 'DEFAULT',
        client_id_var: str = 'SPOTIPY_CLIENT_ID',
        client_secret_var: str = 'SPOTIPY_CLIENT_SECRET',
        redirect_uri_var: str = 'SPOTIPY_REDIRECT_URI'
) -> (str, str, str):
    """
    Read credentials from a config file.

    The configuration must be in INI format
    as accepted by :class:`configparser.ConfigParser`.

    Parameters
    ----------
    file_path
        path of the file containing the credential variables
    section
        name of the section to read variables from
    client_id_var
        name of the variable containing a client ID
    client_secret_var
        name of the variable containing a client secret
    redirect_uri_var
        name of the variable containing a redirect URI

    Returns
    -------
    tuple
        (client ID, client secret, redirect URI), None if not found
    """
    c = configparser.ConfigParser()
    c.optionxform = str
    with open(file_path, 'r') as f:
        c.read_file(f)

    return read_configfile(
        client_id_var,
        client_secret_var,
        redirect_uri_var,
        config=c[section]
    )
