"""
Conversions between Spotify IDs, URIs and URLs.

.. code:: python

    from spotipy.convert import to_url, from_url

    # Create ULR for opening an album in the browser
    mountain = '3RBULTZJ97bvVzZLpxcB0j'
    m_url = to_url('album', mountain)

    # Parse input
    type_, id_ = from_url(m_url)
    print(f'Got type `{type_}` with ID `{id_}`')
"""

import re

from typing import Union
from spotipy.serialise import SerialisableEnum


class ConversionError(Exception):
    pass


class IdentifierType(SerialisableEnum):
    """
    Valid types of Spotify IDs.
    """
    artist = 'artist'
    album = 'album'
    playlist = 'playlist'
    track = 'track'


def check_type(type_: Union[str, IdentifierType]):
    """
    Validate type of an ID and raise if invalid.
    """
    if str(type_) not in IdentifierType.__members__:
        raise ConversionError(f'Invalid type "{type_}"!')


# Match beginning, all base62 characters and end of string
all_base62 = re.compile('^[0-9a-zA-Z]*$')


def check_id(id_: str):
    """
    Validate resource ID and raise if invalid.
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
    """
    check_type(type_)
    check_id(id_)
    return f'http://open.spotify.com/{type_}/{id_}'


def from_uri(uri: str) -> tuple:
    """
    Parse type and ID from an URI.

    Parameters
    ----------
    uri
        URI to parse

    Returns
    -------
    tuple
        (type, ID) parsed from the URI
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

    Parameters
    ----------
    url
        URL to parse

    Returns
    -------
    tuple
        (type, ID) parsed from the URL
    """
    *prefix, type_, id_ = url.split('/')
    prefix = '/'.join(prefix)

    if prefix not in ('http://open.spotify.com', 'open.spotify.com'):
        raise ConversionError(f'Invalid URL prefix "{prefix}"!')
    check_type(type_)
    check_id(id_)

    return type_, id_
