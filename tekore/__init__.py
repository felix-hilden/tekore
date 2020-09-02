"""
Client for the Spotify Web API.

This module holds all public objects provided by Tekore
with the exception of response models, which are located in ``tekore.model``.

See online documentation at `RTD <http://tekore.rtfd.io>`_.
"""

from tekore._start import check_python_version as _check_python_version
from tekore._start import read_version_file as _read_version_file

_check_python_version()

from tekore import model
from ._auth import (
    Credentials,
    Token,
    AccessToken,
    RefreshingCredentials,
    RefreshingToken,
    scope,
    Scope,
    UserAuth,
    gen_state,
    parse_code_from_url,
    parse_state_from_url,
    prompt_for_user_token,
    refresh_user_token,
    prompt_for_pkce_token,
    refresh_pkce_token,
    request_client_token,
)
from ._client import Spotify
from ._error import (
    HTTPError,
    ClientError,
    ServerError,
    BadRequest,
    Unauthorised,
    Forbidden,
    NotFound,
    TooManyRequests,
    InternalServerError,
    BadGateway,
    ServiceUnavailable,
)
from ._convert import (
    ConversionError,
    IdentifierType,
    to_uri,
    to_url,
    from_uri,
    from_url,
    check_type,
    check_id,
)
from ._sender import (
    Sender,
    SyncSender,
    AsyncSender,
    ExtendingSender,
    RetryingSender,
    CachingSender,
    SenderConflictWarning,
    Client,
    Request,
    Response,
)
from ._config import (
    config_from_environment,
    config_from_file,
    config_to_file,
    MissingConfigurationWarning,
)

__version__ = _read_version_file()

# Change the module of classes to hide module structure
# and fix Sphinx base class links
_classes = [
    Spotify,
    Credentials,
    Token,
    AccessToken,
    RefreshingCredentials,
    RefreshingToken,
    scope,
    Scope,
    UserAuth,
    HTTPError,
    ClientError,
    ServerError,
    BadRequest,
    Unauthorised,
    Forbidden,
    NotFound,
    TooManyRequests,
    InternalServerError,
    BadGateway,
    ServiceUnavailable,
    ConversionError,
    IdentifierType,
    Sender,
    SyncSender,
    AsyncSender,
    ExtendingSender,
    RetryingSender,
    CachingSender,
    SenderConflictWarning,
    Client,
    Request,
    Response,
    MissingConfigurationWarning,
]

for _cls in _classes:
    _cls.__module__ = 'tekore'

client_id_var: str = 'SPOTIFY_CLIENT_ID'
"""Configuration variable name for a client ID."""

client_secret_var: str = 'SPOTIFY_CLIENT_SECRET'
"""Configuration variable name for a client secret."""

redirect_uri_var: str = 'SPOTIFY_REDIRECT_URI'
"""Configuration variable name for a redirect URI."""

user_refresh_var: str = 'SPOTIFY_USER_REFRESH'
"""Configuration variable name for a user refresh token."""
