import re

from typing import Union, Tuple
from tekore.model import StrEnum


class ConversionError(Exception):
    """Error in conversion."""


class IdentifierType(StrEnum):
    """Valid types of Spotify IDs."""

    artist = 'artist'
    album = 'album'
    episode = 'episode'
    playlist = 'playlist'
    show = 'show'
    track = 'track'


def check_type(type_: Union[str, IdentifierType]) -> None:
    """
    Validate type of an ID.

    Raises
    ------
    ConversionError
        When type is invalid.
    """
    if str(type_) not in IdentifierType.__members__:
        raise ConversionError(f'Invalid type "{type_}"!')


# Match beginning, all base62 characters and end of string
all_base62 = re.compile('^[0-9a-zA-Z]*$')


def check_id(id_: str) -> None:
    """
    Validate resource ID.

    Raises
    ------
    ConversionError
        When ID is invalid.
    """
    if id_ == '' or all_base62.search(id_) is None:
        raise ConversionError(f'Invalid id: "{id_}"!')


def to_uri(type_: Union[str, IdentifierType], id_: str) -> str:
    """
    Convert an ID to an URI of the appropriate type.

    Parameters
    ----------
    type_
        valid :class:`IdentifierType`
    id_
        resource identifier

    Returns
    -------
    str
        converted URI

    Raises
    ------
    ConversionError
        On invalid type or ID.
    """
    check_type(type_)
    check_id(id_)
    return f'spotify:{type_}:{id_}'


def to_url(type_: Union[str, IdentifierType], id_: str) -> str:
    """
    Convert an ID to an URL of the appropriate type.

    Parameters
    ----------
    type_
        valid :class:`IdentifierType`
    id_
        resource identifier

    Returns
    -------
    str
        converted URL

    Raises
    ------
    ConversionError
        On invalid type or ID.
    """
    check_type(type_)
    check_id(id_)
    return f'https://open.spotify.com/{type_}/{id_}'


def from_uri(uri: str) -> Tuple[str, str]:
    """
    Parse type and ID from an URI.

    Parameters
    ----------
    uri
        URI to parse

    Returns
    -------
    Tuple[str, str]
        type and ID parsed from the URI

    Raises
    ------
    ConversionError
        On invalid type or ID.
    """
    spotify, type_, id_ = uri.split(':')

    if spotify != 'spotify':
        raise ConversionError(f'Invalid URI prefix "{spotify}"!')
    check_type(type_)
    check_id(id_)

    return type_, id_


_url_prefixes = (
    'open.spotify.com',
    'http://open.spotify.com',
    'https://open.spotify.com'
)


def from_url(url: str) -> Tuple[str, str]:
    """
    Parse type and ID from an URL.

    If the URL includes the tracking token (?si=x) 
    it will be stripped away.

    Parameters
    ----------
    url
        URL to parse

    Returns
    -------
    Tuple[str, str]
        type and ID parsed from the URL

    Raises
    ------
    ConversionError
        On invalid type or ID.
    """
    *prefixes, type_, id_ = url.split('/')
    prefix = '/'.join(prefixes)

    id_, _ = id_.split('?si=')

    if prefix not in _url_prefixes:
        raise ConversionError(f'Invalid URL prefix "{prefix}"!')
    check_type(type_)
    check_id(id_)

    return type_, id_
