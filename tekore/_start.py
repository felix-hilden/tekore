import os
import sys

required_version = (3, 6)
error_msg = """You are running Tekore on Python <{0}!

Tekore is not compatible with Python <{0}, and you still
ended up with this version installed. That's unfortunate; sorry about that.
It should not have happened. Make sure you have pip >= 9.0 to avoid this kind
of issue, as well as setuptools >= 24.2:

    $ pip install pip setuptools --upgrade

To properly use this library, please upgrade to Python {0} or above.

It would be great if you can figure out how this version ended up being
installed, and try to check how to prevent that for future users.

See the PyPI page for more up-to-date information:
https://pypi.org/project/tekore
"""


def check_python_version():
    """Verify that the Python version is acceptable."""
    if sys.version_info < required_version:
        _required_version_str = '.'.join(str(i) for i in required_version)
        raise ImportError(error_msg.format(_required_version_str))


def read_version_file() -> str:
    """Read version file to determine current library version."""
    from pathlib import Path
    version_file = Path(os.path.realpath(__file__)).parent / 'VERSION'
    return version_file.read_text().strip()
