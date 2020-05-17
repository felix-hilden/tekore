from tekore._start import check_python_version as _check_python_version
from tekore._start import read_version_file as _read_version_file

_check_python_version()

from typing import Union as _Union, Type as _Type
from tekore import model
from tekore._auth import (
    Credentials,
    Token,
    AccessToken,
    RefreshingCredentials,
    RefreshingToken,
    scope,
    Scope,
    parse_code_from_url,
    prompt_for_user_token,
    refresh_user_token,
    request_client_token,
)
from tekore._client import Spotify
from tekore._error import (
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
from tekore._convert import (
    ConversionError,
    IdentifierType,
    to_uri,
    to_url,
    from_uri,
    from_url,
    check_type,
    check_id,
)
from tekore._sender import (
    Sender,
    SyncSender,
    AsyncSender,
    ExtendingSender,
    TransientSender,
    AsyncTransientSender,
    PersistentSender,
    AsyncPersistentSender,
    SingletonSender,
    AsyncSingletonSender,
    RetryingSender,
    CachingSender,
    SenderConflictWarning,
    Client,
)
from tekore._config import (
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
    TransientSender,
    AsyncTransientSender,
    PersistentSender,
    AsyncPersistentSender,
    SingletonSender,
    AsyncSingletonSender,
    RetryingSender,
    CachingSender,
    SenderConflictWarning,
    Client,
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

default_requests_kwargs: dict = {}
"""
Default keyword arguments to send with in synchronous mode.
Not used when any other keyword arguments are passed in.
"""

default_httpx_kwargs: dict = {}
"""
Default keyword arguments to send with in asynchronous mode.
Not used when any other keyword arguments are passed in.
"""

default_sender_type: _Union[_Type[SyncSender], _Type[AsyncSender]] = PersistentSender
"""
Sender to instantiate by default.
"""

default_sender_instance: Sender = None
"""
Default sender instance to use in clients.
If specified, overrides :attr:`default_sender_type`.
"""
