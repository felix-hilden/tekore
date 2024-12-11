"""
Client for the Spotify Web API.

This module holds all public objects provided by Tekore
with the exception of response models, which are located in ``tekore.model``.

See online documentation at `RTD <http://tekore.rtfd.io>`_.
"""

from tekore import model

from ._auth import (
    AccessToken,
    Credentials,
    RefreshingCredentials,
    RefreshingToken,
    Scope,
    Token,
    UserAuth,
    gen_state,
    parse_code_from_url,
    parse_state_from_url,
    prompt_for_pkce_token,
    prompt_for_user_token,
    refresh_pkce_token,
    refresh_user_token,
    request_client_token,
    scope,
)
from ._client import Spotify, is_short_link
from ._config import (
    MissingConfigurationWarning,
    config_from_environment,
    config_from_file,
    config_to_file,
)
from ._convert import (
    ConversionError,
    IdentifierType,
    check_id,
    check_type,
    from_uri,
    from_url,
    to_uri,
    to_url,
)
from ._sender import (
    AsyncSender,
    BadGateway,
    BadRequest,
    CachingSender,
    Client,
    ClientError,
    ExtendingSender,
    Forbidden,
    HTTPError,
    InternalServerError,
    NotFound,
    Request,
    Response,
    RetryingSender,
    Sender,
    SenderConflictWarning,
    ServerError,
    ServiceUnavailable,
    SyncSender,
    TooManyRequests,
    Unauthorised,
)

__version__ = "6.0.0"

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
    _cls.__module__ = "tekore"

client_id_var: str = "SPOTIFY_CLIENT_ID"
"""Configuration variable name for a client ID."""

client_secret_var: str = "SPOTIFY_CLIENT_SECRET"
"""Configuration variable name for a client secret."""

redirect_uri_var: str = "SPOTIFY_REDIRECT_URI"
"""Configuration variable name for a redirect URI."""

user_refresh_var: str = "SPOTIFY_USER_REFRESH"
"""Configuration variable name for a user refresh token."""
