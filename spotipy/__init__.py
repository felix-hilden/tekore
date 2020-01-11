from spotipy._start import check_python_version as _check_python_version
from spotipy._start import read_version_file as _read_version_file

_check_python_version()

from spotipy import scope, util
from spotipy.auth import Credentials
from spotipy.client import Spotify

__version__ = _read_version_file()
