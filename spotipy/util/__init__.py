"""
Utility module for your convenience <3

The main motivation for this module is to make authorisation effortless.
That goal is achieved by three mechanisms:
reading configuration, an automatically refreshing access token and
functions that implement everything needed to retrieve tokens.

Some applications might have different needs,
so please do create your own versions of these routines.
Particularly, :class:`prompt_for_user_token` opens up a web browser
for the user to log in with, doesn't expose all parameters that are available
when using lower-level functions, and forces the login dialog to be shown.

Almost everything in submodules is imported to :class:`util` for easy access.
"""

from spotipy.util.config import (
    config_from_environment,
    config_from_file,
)
from spotipy.util.credentials import (
    parse_code_from_url,
    prompt_for_user_token,
    RefreshingCredentials,
    RefreshingToken,
    refresh_user_token,
    request_client_token,
)
