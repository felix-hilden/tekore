import os as _os
from pathlib import Path as _Path

from spotipy.auth import Token, Credentials
from spotipy.scope import Scope, scopes
from spotipy.client import Spotify
from spotipy._verify import _check_version

_version_file = _Path(_os.path.realpath(__file__)).parent / 'VERSION'
__version__ = _version_file.read_text().strip()

_check_version()
