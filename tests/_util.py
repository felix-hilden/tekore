"""
Test utilities.
"""

import warnings
from contextlib import contextmanager
from unittest.mock import MagicMock


@contextmanager
def handle_warnings(filt: str = "ignore"):
    warnings.simplefilter(filt)
    yield
    warnings.resetwarnings()


class AsyncMock(MagicMock):
    async def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)
