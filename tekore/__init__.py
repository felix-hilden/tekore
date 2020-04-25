from tekore._start import check_python_version as _check_python_version
from tekore._start import read_version_file as _read_version_file

_check_python_version()

from tekore import scope
from tekore.auth import Credentials, RefreshingCredentials
from tekore.auth.expiring import OAuthError
from tekore.client import Spotify
from tekore.client.decor.error import (
    BadRequest,
    Unauthorised,
    Forbidden,
    NotFound,
    TooManyRequests,
    InternalServerError,
    BadGateway,
    ServiceUnavailable,
)
from tekore.convert import (
    ConversionError,
    IdentifierType,
    to_uri,
    to_url,
    from_uri,
    from_url,
)
from tekore.sender import (
    TransientSender,
    AsyncTransientSender,
    PersistentSender,
    AsyncPersistentSender,
    SingletonSender,
    AsyncSingletonSender,
    RetryingSender,
    CachingSender,
    SenderConflictWarning,
)
from tekore.util import (
    config_from_environment,
    config_from_file,
    config_to_file,
    parse_code_from_url,
    prompt_for_user_token,
    refresh_user_token,
    request_client_token,
)
from tekore.util.config import MissingConfigurationWarning

__version__ = _read_version_file()
