import unittest

from pathlib import Path
from unittest.mock import MagicMock, patch

from tekore.auth.refreshing import RefreshingToken
from tekore.util.config import MissingConfigurationWarning
from tekore.util import (
    parse_code_from_url,
    prompt_for_user_token,
    config_from_environment,
    refresh_user_token,
    request_client_token,
    config_from_file,
    config_to_file,
)

from tests._util import handle_warnings
from tests._cred import TestCaseWithUserCredentials


class TestParseCodeFromURL(unittest.TestCase):
    def test_empty_url_raises(self):
        with self.assertRaises(KeyError):
            parse_code_from_url('')

    def test_no_code_raises(self):
        with self.assertRaises(KeyError):
            parse_code_from_url('http://example.com')

    def test_multiple_codes_raises(self):
        with self.assertRaises(KeyError):
            parse_code_from_url('http://example.com?code=1&code=2')

    def test_single_code_returned(self):
        r = parse_code_from_url('http://example.com?code=1')
        self.assertEqual(r, '1')


class TestTokenUtilityFunctions(TestCaseWithUserCredentials):
    def test_prompt_for_user_token(self):
        cred = MagicMock()
        cred.authorisation_url.return_value = 'http://example.com'
        cred.request_access_token.return_value = MagicMock()
        input_ = MagicMock(return_value='http://example.com?code=1')
        with patch('tekore.auth.refreshing.Credentials', cred),\
                patch('tekore.util.credentials.webbrowser', MagicMock()),\
                patch('tekore.util.credentials.input', input_),\
                patch('tekore.util.credentials.print', MagicMock()):
            token = prompt_for_user_token('', '', '')

        with self.subTest('Input prompted'):
            input_.assert_called_once()

        with self.subTest('Refreshing token returned'):
            self.assertIsInstance(token, RefreshingToken)

    def test_request_refreshed_token_returns_refreshing_token(self):
        token = refresh_user_token(
            self.client_id,
            self.client_secret,
            self.user_token.refresh_token
        )
        self.assertIsInstance(token, RefreshingToken)

    def test_expiring_user_token_refreshed(self):
        token = refresh_user_token(
            self.client_id,
            self.client_secret,
            self.user_token.refresh_token
        )
        old_token = str(token)
        token._token._expires_at -= token._token.expires_in - 30
        self.assertNotEqual(old_token, str(token))

    def test_request_client_token_returns_refreshing_token(self):
        token = request_client_token(
            self.client_id,
            self.client_secret
        )
        self.assertIsInstance(token, RefreshingToken)

    def test_expiring_client_token_refreshed(self):
        token = request_client_token(
            self.client_id,
            self.client_secret
        )
        old_token = str(token)
        token._token._expires_at -= token._token.expires_in - 30
        self.assertNotEqual(old_token, str(token))


class TestReadConfig(unittest.TestCase):
    test_config_path = 'test_config.ini'
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

    @classmethod
    def setUpClass(cls):
        with open(cls.test_config_path, 'w') as f:
            f.write(cls.test_config)

        from tekore.util import config
        cls.client_id_var = config.client_id_var
        cls.client_secret_var = config.client_secret_var
        cls.redirect_uri_var = config.redirect_uri_var
        cls.user_refresh_var = config.user_refresh_var

    @staticmethod
    def _config_names_set(id_, secret, uri, refresh):
        from tekore.util import config
        config.client_id_var = id_
        config.client_secret_var = secret
        config.redirect_uri_var = uri
        config.user_refresh_var = refresh

    def tearDown(self):
        self._config_names_set(
            self.client_id_var,
            self.client_secret_var,
            self.redirect_uri_var,
            self.user_refresh_var
        )

    @classmethod
    def tearDownClass(cls):
        import os
        os.remove(cls.test_config_path)

    def test_environment_user_refresh_returned(self):
        _, _, _, _ = config_from_environment(return_refresh=True)

    def test_environment_read_modified_names(self):
        import os
        from tekore.util import config

        config.client_id_var = 'client_id'
        config.client_secret_var = 'client_secret'
        config.redirect_uri_var = 'redirect_uri'
        os.environ[config.client_id_var] = 'id'
        os.environ[config.client_secret_var] = 'secret'
        os.environ[config.redirect_uri_var] = 'uri'

        conf = config_from_environment()
        self.assertTupleEqual(conf, ('id', 'secret', 'uri'))

    def test_file_default_section(self):
        conf = config_from_file(self.test_config_path)
        self.assertTupleEqual(conf, ('df_id', 'df_secret', 'df_uri'))

    def test_file_refresh_returned(self):
        conf = config_from_file(self.test_config_path, return_refresh=True)
        self.assertTupleEqual(conf, ('df_id', 'df_secret', 'df_uri', 'df_refresh'))

    def test_file_another_section(self):
        self._config_names_set(
            'CLIENT_ID',
            'CLIENT_SECRET',
            'REDIRECT_URI',
            '_'
        )

        conf = config_from_file(self.test_config_path, 'ANOTHER')
        self.assertTupleEqual(conf, ('an_id', 'an_secret', 'an_uri'))

    def test_file_missing_variables_returns_none(self):
        self._config_names_set(
            'CLIENT_ID',
            'CLIENT_SECRET',
            'REDIRECT_URI',
            '_'
        )
        with handle_warnings('ignore'):
            conf = config_from_file(self.test_config_path, 'MISSING')
        self.assertTupleEqual(conf, (None, None, None))

    def test_file_another_section_is_case_sensitive(self):
        self._config_names_set(
            'client_id',
            'client_secret',
            'redirect_uri',
            '_'
        )
        with handle_warnings('ignore'):
            conf = config_from_file(self.test_config_path)
        self.assertTupleEqual(conf, (None, None, None))

    def test_file_nonexistent_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            config_from_file('not_file.ini')

    def test_file_nonexistent_section_raises(self):
        with self.assertRaises(KeyError):
            config_from_file(self.test_config_path, 'NOTSECTION')

    def test_file_pathlib_path_accepted(self):
        from pathlib import Path
        path = Path(self.test_config_path)
        conf = config_from_file(path)
        self.assertTupleEqual(conf, ('df_id', 'df_secret', 'df_uri'))

    def test_missing_variables_warned(self):
        self._config_names_set(
            'CLIENT_ID',
            'CLIENT_SECRET',
            'REDIRECT_URI',
            '_'
        )
        with handle_warnings('error'):
            with self.assertRaises(MissingConfigurationWarning):
                config_from_file(self.test_config_path, 'MISSING')


class TestConfigToFile(unittest.TestCase):
    test_config_path = Path('test_config.ini')
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

    def tearDown(self):
        if self.test_config_path.exists():
            self.test_config_path.unlink()

    def _write_default(self):
        self.test_config_path.write_text(self.test_config)

    def test_pathlib_path_accepted(self):
        config_to_file(self.test_config_path, ('a', 'b', 'c'))

    def test_config_written_with_tuple(self):
        written = ('id', 'secret', 'uri')
        config_to_file(self.test_config_path, written)
        loaded = config_from_file(self.test_config_path)
        self.assertTupleEqual(written, loaded)

    def test_config_written_with_dict(self):
        from tekore.util import config
        written = {config.client_secret_var: 'secret'}

        config_to_file(self.test_config_path, written)
        loaded = config_from_file(self.test_config_path)
        self.assertTupleEqual((None, 'secret', None), loaded)

    def test_config_write_to_section(self):
        written = ('id', 'secret', 'uri')
        config_to_file(self.test_config_path, written, section='SEC')
        loaded = config_from_file(self.test_config_path, section='SEC')
        self.assertTupleEqual(written, loaded)

    def test_config_written_with_tuple_refresh_token(self):
        written = ('id', 'secret', 'uri', 'refresh')
        config_to_file(self.test_config_path, written)
        loaded = config_from_file(self.test_config_path, return_refresh=True)
        self.assertTupleEqual(written, loaded)

    def test_config_tuple_nones_not_written(self):
        original = ('id', 'secret', 'uri')
        config_to_file(self.test_config_path, original)

        written = (None, 'another', None)
        config_to_file(self.test_config_path, written)

        loaded = config_from_file(self.test_config_path)
        self.assertTupleEqual(('id', 'another', 'uri'), loaded)

    def test_existing_configuration_preserved(self):
        self._write_default()
        config_to_file(self.test_config_path, ('a', 'b', 'c'))
        text = self.test_config_path.read_text()
        self.assertTupleEqual(
            (True, True, True),
            tuple(i in text for i in ('SOMETHING', 'WHATEVER', 'SECTION'))
        )


if __name__ == '__main__':
    unittest.main()
