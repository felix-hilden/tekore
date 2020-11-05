import pytest
from unittest.mock import patch
from tekore._start import check_python_version


class TestPackage:
    def test_too_small_python_version_raises(self):
        """
        Check if the python version of python 2.

        Args:
            self: (todo): write your description
        """
        version_info = (3, 5, 5)

        with patch('sys.version_info', version_info):
            with pytest.raises(ImportError):
                check_python_version()
