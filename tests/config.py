import pytest
from pathlib import Path

from tekore import (
    config_from_environment,
    config_from_file,
    config_to_file,
    MissingConfigurationWarning,
)

from tests._util import handle_warnings


def config_names_set(id_, secret, uri, refresh):
    """
    Set a set of config variables.

    Args:
        id_: (str): write your description
        secret: (str): write your description
        uri: (str): write your description
        refresh: (todo): write your description
    """
    import tekore as tk
    tk.client_id_var = id_
    tk.client_secret_var = secret
    tk.redirect_uri_var = uri
    tk.user_refresh_var = refresh


@pytest.fixture()
def conf_vars():
    """
    A context manager that provides a context manager.

    Args:
    """
    import tekore as tk
    client_id_var = tk.client_id_var
    client_secret_var = tk.client_secret_var
    redirect_uri_var = tk.redirect_uri_var
    user_refresh_var = tk.user_refresh_var
    yield
    config_names_set(
        client_id_var,
        client_secret_var,
        redirect_uri_var,
        user_refresh_var
    )


@pytest.fixture(scope='class')
def conf_path():
    """
    Return the path to the conf file.

    Args:
    """
    return 'test_config.ini'


@pytest.fixture(scope='function')
def write_conf(conf_path):
    """
    Write config file.

    Args:
        conf_path: (str): write your description
    """
    test_config = """
[DEFAULT]
SPOTIFY_CLIENT_ID = df_id
SPOTIFY_CLIENT_SECRET = df_secret
SPOTIFY_REDIRECT_URI = df_uri
SPOTIFY_USER_REFRESH = df_refresh

[ANOTHER]
CLIENT_ID = an_id
CLIENT_SECRET = an_secret
REDIRECT_URI = an_uri

[MISSING]
WHATEVER = something
"""
    with open(conf_path, 'w') as f:
        f.write(test_config)

    yield

    import os
    os.remove(conf_path)


@pytest.mark.usefixtures('conf_vars', 'write_conf')
class TestReadConfig:
    def test_environment_user_refresh_returned(self):
        """
        Return the environment environment environment.

        Args:
            self: (todo): write your description
        """
        _, _, _, _ = config_from_environment(return_refresh=True)

    def test_environment_read_modified_names(self):
        """
        Read environment variables.

        Args:
            self: (todo): write your description
        """
        import os
        import tekore as tk

        tk.client_id_var = 'client_id'
        tk.client_secret_var = 'client_secret'
        tk.redirect_uri_var = 'redirect_uri'
        os.environ[tk.client_id_var] = 'id'
        os.environ[tk.client_secret_var] = 'secret'
        os.environ[tk.redirect_uri_var] = 'uri'

        conf = config_from_environment()
        assert conf == ('id', 'secret', 'uri')

    def test_file_default_section(self, conf_path):
        """
        Read the default config file.

        Args:
            self: (todo): write your description
            conf_path: (str): write your description
        """
        conf = config_from_file(conf_path)
        assert conf == ('df_id', 'df_secret', 'df_uri')

    def test_file_refresh_returned(self, conf_path):
        """
        Return true if the test file exists.

        Args:
            self: (todo): write your description
            conf_path: (str): write your description
        """
        conf = config_from_file(conf_path, return_refresh=True)
        assert conf == ('df_id', 'df_secret', 'df_uri', 'df_refresh')

    def test_file_another_section(self, conf_path):
        """
        Test if the configuration file exists.

        Args:
            self: (todo): write your description
            conf_path: (str): write your description
        """
        config_names_set(
            'CLIENT_ID',
            'CLIENT_SECRET',
            'REDIRECT_URI',
            '_'
        )

        conf = config_from_file(conf_path, 'ANOTHER')
        assert conf == ('an_id', 'an_secret', 'an_uri')

    def test_file_missing_variables_returns_none(self, conf_path):
        """
        Return a set of missing test variables.

        Args:
            self: (todo): write your description
            conf_path: (str): write your description
        """
        config_names_set(
            'CLIENT_ID',
            'CLIENT_SECRET',
            'REDIRECT_URI',
            '_'
        )
        with handle_warnings('ignore'):
            conf = config_from_file(conf_path, 'MISSING')
        assert conf == (None, None, None)

    def test_file_another_section_is_case_sensitive(self, conf_path):
        """
        Returns true if the test case of test case.

        Args:
            self: (todo): write your description
            conf_path: (str): write your description
        """
        config_names_set(
            'client_id',
            'client_secret',
            'redirect_uri',
            '_'
        )
        with handle_warnings('ignore'):
            conf = config_from_file(conf_path)
        assert conf == (None, None, None)

    def test_file_nonexistent_file_raises(self):
        """
        Test if the test file is none.

        Args:
            self: (todo): write your description
        """
        with pytest.raises(FileNotFoundError):
            config_from_file('not_file.ini')

    def test_file_nonexistent_section_raises(self, conf_path):
        """
        Check if the test section is not none.

        Args:
            self: (todo): write your description
            conf_path: (str): write your description
        """
        with pytest.raises(KeyError):
            config_from_file(conf_path, 'NOTSECTION')

    def test_file_pathlib_path_accepted(self, conf_path):
        """
        Test if the given test_path.

        Args:
            self: (todo): write your description
            conf_path: (str): write your description
        """
        from pathlib import Path
        path = Path(conf_path)
        conf = config_from_file(path)
        assert conf == ('df_id', 'df_secret', 'df_uri')

    def test_missing_variables_warned(self, conf_path):
        """
        .. version of missing variables.

        Args:
            self: (todo): write your description
            conf_path: (str): write your description
        """
        config_names_set(
            'CLIENT_ID',
            'CLIENT_SECRET',
            'REDIRECT_URI',
            '_'
        )
        with handle_warnings('error'):
            with pytest.raises(MissingConfigurationWarning):
                config_from_file(conf_path, 'MISSING')


@pytest.fixture(scope='function')
def remove_conf(conf_path):
    """
    Remove conf file.

    Args:
        conf_path: (str): write your description
    """
    yield
    path = Path(conf_path)
    if path.exists():
        path.unlink()


@pytest.mark.usefixtures('remove_conf')
class TestConfigToFile:
    def test_pathlib_path_accepted(self, conf_path):
        """
        Test if the test path to the test_pathlib.

        Args:
            self: (todo): write your description
            conf_path: (str): write your description
        """
        path = Path(conf_path)
        config_to_file(path, ('a', 'b', 'c'))

    def test_config_written_with_tuple(self, conf_path):
        """
        Test if a config file exists. conf_path.

        Args:
            self: (todo): write your description
            conf_path: (str): write your description
        """
        written = ('id', 'secret', 'uri')
        config_to_file(conf_path, written)
        loaded = config_from_file(conf_path)
        assert written == loaded

    def test_config_written_with_dict(self, conf_path):
        """
        Test if a secure configuration file exists.

        Args:
            self: (todo): write your description
            conf_path: (str): write your description
        """
        import tekore as tk
        written = {tk.client_secret_var: 'secret'}

        config_to_file(conf_path, written)
        with handle_warnings('ignore'):
            loaded = config_from_file(conf_path)
        assert (None, 'secret', None) == loaded

    def test_config_write_to_section(self, conf_path):
        """
        Write config to a file.

        Args:
            self: (todo): write your description
            conf_path: (str): write your description
        """
        written = ('id', 'secret', 'uri')
        config_to_file(conf_path, written, section='SEC')
        loaded = config_from_file(conf_path, section='SEC')
        assert written == loaded

    def test_config_written_with_tuple_refresh_token(self, conf_path):
        """
        Test if a config file exists in the config file.

        Args:
            self: (todo): write your description
            conf_path: (str): write your description
        """
        written = ('id', 'secret', 'uri', 'refresh')
        config_to_file(conf_path, written)
        loaded = config_from_file(conf_path, return_refresh=True)
        assert written == loaded

    def test_config_tuple_nones_not_written(self, conf_path):
        """
        Test if nones are nones.

        Args:
            self: (todo): write your description
            conf_path: (str): write your description
        """
        original = ('id', 'secret', 'uri')
        config_to_file(conf_path, original)

        written = (None, 'another', None)
        config_to_file(conf_path, written)

        loaded = config_from_file(conf_path)
        assert ('id', 'another', 'uri') == loaded

    def test_existing_configuration_preserved(self, conf_path):
        """
        Test that the configuration file.

        Args:
            self: (todo): write your description
            conf_path: (str): write your description
        """
        test_config = """
[DEFAULT]
SOMETHING = whatever
SPOTIFY_CLIENT_ID = df_id
SPOTIFY_CLIENT_SECRET = df_secret
SPOTIFY_REDIRECT_URI = df_uri
SPOTIFY_USER_REFRESH = df_refresh

[SECTION]
WHATEVER = something
"""
        path = Path(conf_path)
        path.write_text(test_config)
        config_to_file(path, ('a', 'b', 'c'))
        text = path.read_text()
        conf = tuple(i in text for i in ('SOMETHING', 'WHATEVER', 'SECTION'))
        assert (True, True, True) == conf
