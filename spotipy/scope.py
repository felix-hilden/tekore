"""
Scope
=====

Scopes for user authorisation.
An enumeration with every possible right is defined in :class:`AuthorisationScopes`.
They can be used with :class:`Scope` to provide flexible set-like functionality.

Some ready-made scopes are also made available.

.. code:: python

   read: Scope = ...            # All read scopes
   write: Scope = ...           # All write scopes
   every: Scope = read + write  # All available scopes
"""

from enum import Enum
from typing import Union


class AuthorisationScopes(Enum):
    """
    Spotify Web API Authorisation Scopes.

    The string representation of an instance is its enum value.

    .. code:: python

       s = AuthorisationScopes.user_read_email
       print(s)  # -> 'user-read-email'
    """
    user_read_email = 'user-read-email'
    user_read_private = 'user-read-private'
    user_top_read = 'user-top-read'
    user_read_recently_played = 'user-read-recently-played'

    user_follow_read = 'user-follow-read'
    user_follow_modify = 'user-follow-modify'
    user_library_read = 'user-library-read'
    user_library_modify = 'user-library-modify'

    user_read_currently_playing = 'user-read-currently-playing'
    user_read_playback_state = 'user-read-playback-state'
    user_modify_playback_state = 'user-modify-playback-state'

    playlist_modify_public = 'playlist-modify-public'
    playlist_read_collaborative = 'playlist-read-collaborative'
    playlist_read_private = 'playlist-read-private'
    playlist_modify_private = 'playlist-modify-private'

    ugc_image_upload = 'ugc-image-upload'

    def __str__(self):
        return self.value


scopes = AuthorisationScopes


class Scope(frozenset):
    """
    Set of AuthorisationScopes constituting a scope for a token.

    Immutable, supports unpacking and flexible addition and subtraction.

    .. code:: python

       bruce = Scope(*scopes)
       sally = Scope(scopes.user_read_email, scopes.user_read_private)
       timmy = Scope('ugc-image-upload', 'user-top-read')
       elise = Scope(*sally, *timmy, scopes.user_follow_modify)
       waldo = sally + timmy - 'user-read-email' + scopes.user_follow_read

    The string representation of a :class:`Scope` is a sorted,
    space-separated concatenation of its members.

    .. code:: python

       s = Scope('b', 'c', 'a')
       print(s)  # -> 'a b c'
    """
    def __new__(cls, *members):
        if len(members) == 1 and isinstance(members[0], frozenset):
            members = [*members[0]]
        members = [str(m) for m in members]
        return super().__new__(cls, members)

    def __str__(self):
        return ' '.join(sorted(self))

    def __add__(
            self,
            other: Union[set, frozenset, str, AuthorisationScopes]
    ) -> 'Scope':
        if type(other) in (str, AuthorisationScopes):
            other = {str(other)}
        return type(self)(self.union(other))

    def __sub__(
            self,
            other: Union[set, frozenset, str, AuthorisationScopes]
    ) -> 'Scope':
        if type(other) in (str, AuthorisationScopes):
            other = {str(other)}
        return type(self)(self.difference(other))


read = Scope(
    AuthorisationScopes.user_read_email,
    AuthorisationScopes.user_read_private,
    AuthorisationScopes.user_top_read,
    AuthorisationScopes.user_read_recently_played,
    AuthorisationScopes.user_follow_read,
    AuthorisationScopes.user_library_read,
    AuthorisationScopes.user_read_currently_playing,
    AuthorisationScopes.user_read_playback_state,
    AuthorisationScopes.playlist_read_collaborative,
    AuthorisationScopes.playlist_read_private
)
write = Scope(
    AuthorisationScopes.user_follow_modify,
    AuthorisationScopes.user_library_modify,
    AuthorisationScopes.user_modify_playback_state,
    AuthorisationScopes.playlist_modify_public,
    AuthorisationScopes.playlist_modify_private,
    AuthorisationScopes.ugc_image_upload
)
every = read + write
