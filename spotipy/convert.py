"""
Conversions between Spotify IDs, URIs and URLs.
"""

import re
from enum import Enum


class ConversionError(Exception):
    pass


class Type(Enum):
    """
    Enumerate valid types of Spotify IDs.
    """
    artist = 'artist'
    album = 'album'
    track = 'track'


def check_type(type_: str):
    """
    Validate type of an ID and raise if invalid.
    """
    if type_ not in Type.__members__:
        raise ConversionError(f'Invalid type "{type_}"!')


# Match beginning, all base62 characters and end of string
all_base62 = re.compile('^[0-9a-zA-Z]*$')


def check_id(id_: str):
    """
    Validate Spotify ID and raise if invalid.
    """
    if id_ == '' or all_base62.search(id_) is None:
        raise ConversionError(f'Invalid id: "{id_}"!')


def to_uri(type_: str, id_: str) -> str:
    """
    Convert an ID to an URI of the appropriate type.
    """
    check_type(type_)
    check_id(id_)
    return f'spotify:{type_}:{id_}'


def to_url(type_: str, id_: str) -> str:
    """
    Convert an ID to an URL of the appropriate type.
    """
    check_type(type_)
    check_id(id_)
    return f'http://open.spotify.com/{type_}/{id_}'


def from_uri(uri: str) -> tuple:
    """
    Parse type and ID from an URI.
    """
    spotify, type_, id_ = uri.split(':')

    if spotify != 'spotify':
        raise ConversionError(f'Invalid URI prefix "{spotify}"!')
    check_type(type_)
    check_id(id_)

    return type_, id_


def from_url(url: str) -> tuple:
    """
    Parse type and ID from an URL.
    """
    *prefix, type_, id_ = url.split('/')
    prefix = '/'.join(prefix)

    if prefix not in ('http://open.spotify.com', 'open.spotify.com'):
        raise ConversionError(f'Invalid URL prefix "{prefix}"!')
    check_type(type_)
    check_id(id_)

    return type_, id_
