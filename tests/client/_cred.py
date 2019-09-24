from unittest import TestCase, SkipTest
from spotipy.auth import Credentials
from spotipy.util import read_environment


class TestCaseWithCredentials(TestCase):
    @classmethod
    def setUpClass(cls):
        id_, secret, redirect = read_environment()
        if any(i is None for i in (id_, secret, redirect)):
            raise SkipTest('Invalid credentials!')

        cls.client_id = id_
        cls.client_secret = secret
        cls.redirect_uri = redirect

        cls.cred = Credentials(id_, secret, redirect)
        cls.app_token = cls.cred.request_client_credentials()
