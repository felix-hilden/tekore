"""
Test utilities.
"""

import warnings

from contextlib import contextmanager
from unittest.mock import MagicMock


@contextmanager
def handle_warnings(filt: str = 'ignore'):
    """
    Yield warnings.

    Args:
        filt: (str): write your description
    """
    warnings.simplefilter(filt)
    yield
    warnings.resetwarnings()


class AsyncMock(MagicMock):
    async def __call__(self, *args, **kwargs):
          """
          Calls the given callable.

          Args:
              self: (todo): write your description
          """
        return super(AsyncMock, self).__call__(*args, **kwargs)
