from __future__ import annotations

import re

from tekore.model import StrEnum


class ConversionError(Exception):
    """Error in conversion."""


class IdentifierType(StrEnum):
    """Valid types of Spotify IDs."""

    artist = "artist"
    album = "album"
    episode = "episode"
    playlist = "playlist"
    show = "show"
    track = "track"
    user = "user"


def check_type(type_: str | IdentifierType) -> None:
    """
    Validate type of an ID.

    Raises
    ------
    ConversionError
        When type is invalid.
    """
    if str(type_) not in IdentifierType.__members__:
        msg = f"Invalid type {type_!r}!"
        raise ConversionError(msg)


# Match beginning, all base62 characters and end of string
all_base62 = re.compile("^[0-9a-zA-Z]*$")


def check_id(id_: str) -> None:
    """
    Validate resource ID to be base 62.

    Note that user IDs can have special characters, so they cannot be validated.

    Raises
    ------
    ConversionError
        When ID is invalid.
    """
    if id_ == "" or all_base62.search(id_) is None:
        msg = f"Invalid id: {id_!r}!"
        raise ConversionError(msg)


def to_uri(type_: str | IdentifierType, id_: str) -> str:
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
    if type_ != IdentifierType.user:
        check_id(id_)
    return f"spotify:{type_}:{id_}"


def to_url(type_: str | IdentifierType, id_: str) -> str:
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
    if type_ != IdentifierType.user:
        check_id(id_)
    else:
        id_ = id_.replace("#", "%23")
    return f"https://open.spotify.com/{type_}/{id_}"


def from_uri(uri: str) -> tuple[str, str]:
    """
    Parse type and ID from an URI.

    Parameters
    ----------
    uri
        URI to parse

    Returns
    -------
    tuple[str, str]
        type and ID parsed from the URI

    Raises
    ------
    ConversionError
        On invalid format, prefix, type or ID.
    """
    try:
        type_, id_ = _parse_uri(uri)
    except ValueError as e:
        msg = f'Invalid URI: expected format "spotify:{{type}}:{{id}}", got {uri!r}!'
        raise ConversionError(msg) from e

    check_type(type_)
    if type_ != IdentifierType.user:
        check_id(id_)

    return type_, id_


def _parse_uri(uri: str) -> tuple[str, str]:
    spotify, type_, id_ = uri.split(":")
    if spotify != "spotify":
        raise ValueError
    return type_, id_


_url_prefixes = (
    "open.spotify.com",
    "http://open.spotify.com",
    "https://open.spotify.com",
)


def from_url(url: str) -> tuple[str, str]:
    """
    Parse type and ID from an URL.

    Any parameters in the URL will be ignored.

    Parameters
    ----------
    url
        URL to parse

    Returns
    -------
    tuple[str, str]
        type and ID parsed from the URL

    Raises
    ------
    ConversionError
        On invalid format, prefix, type or ID.
    """
    try:
        type_, id_ = _parse_url(url)
    except ValueError as e:
        valid_url = "[http[s]://]open.spotify.com/{type}/{id}"
        msg = f"Invalid URL: expected format {valid_url!r}, got {url!r}!"
        raise ConversionError(msg) from e

    id_ = id_.split("?")[0]
    check_type(type_)
    if type_ != IdentifierType.user:
        check_id(id_)

    return type_, id_


def _parse_url(url: str) -> tuple[str, str]:
    *prefixes, type_, id_ = url.split("/")
    prefix = "/".join(prefixes)
    if prefix not in _url_prefixes:
        raise ValueError
    return type_, id_
