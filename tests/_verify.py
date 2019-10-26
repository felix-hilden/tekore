import unittest
from unittest.mock import patch

from spotipy._verify import _check_version


class TestPackage(unittest.TestCase):
    def test_too_small_python_version_raises(self):
        version_info = (3, 6, 5)

        with patch('sys.version_info', version_info):
            with self.assertRaises(ImportError):
                _check_version()
