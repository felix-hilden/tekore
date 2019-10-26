import sys as _sys

_required_version = (3, 7)
_error_msg = """You are running Spotipy 3.x on Python <{0}!

Spotipy 3.0 and above are no longer compatible with Python <{0}, and you still
ended up with this version installed. That's unfortunate; sorry about that.
It should not have happened. Make sure you have pip >= 9.0 to avoid this kind
of issue, as well as setuptools >= 24.2:

    $ pip install pip setuptools --upgrade

Your choices:
- Upgrade to Python {0}
- Install an older version of Spotipy

    $ pip install 'spotipy=2.4.5'

It would be great if you can figure out how this version ended up being
installed, and try to check how to prevent that for future users.

See the PyPI page for more up-to-date information:
https://pypi.org/project/spotipy
"""


def _check_version():
    """
    Verify that the Python version is acceptable.
    """
    if _sys.version_info < _required_version:
        _required_version_str = '.'.join(str(i) for i in _required_version)
        raise ImportError(_error_msg.format(_required_version_str))
