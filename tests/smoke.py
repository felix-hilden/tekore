import unittest


class Import(unittest.TestCase):
    """
    Import parts of the system to check for
    e.g. syntax errors and cyclic imports.
    """
    @staticmethod
    def test_import_spotipy():
        import spotipy

    @staticmethod
    def test_import_auth():
        from spotipy import auth

    @staticmethod
    def test_import_client():
        from spotipy import client

    @staticmethod
    def test_import_convert():
        from spotipy import convert

    @staticmethod
    def test_import_enum():
        from spotipy import enum

    @staticmethod
    def test_import_model():
        from spotipy import model

    @staticmethod
    def test_import_scope():
        from spotipy import scope

    @staticmethod
    def test_import_sender():
        from spotipy import sender


if __name__ == '__main__':
    unittest.main()
