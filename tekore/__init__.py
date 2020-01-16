from tekore._start import check_python_version as _check_python_version
from tekore._start import read_version_file as _read_version_file

_check_python_version()

from tekore import scope, util
from tekore.auth import Credentials
from tekore.client import Spotify, SpotifyAsync

__version__ = _read_version_file()
