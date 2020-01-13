"""
User access token privileges.

Scopes are used in user authorisation to provide tokens with additional privileges.
An enumeration with every possible right is defined in :class:`AuthorisationScopes`.
They can be used with :class:`Scope` for flexible set-like functionality.

.. code:: python

    from tekore.scope import scopes
    from tekore.util import prompt_for_user_token

    cred = (client_id, client_secret, redirect_uri)
    scope = scopes.user_read_email + scopes.user_read_private
    token = prompt_for_user_token(*cred, scope)

Some ready-made scopes are also made available.

.. code:: python

   read: Scope = ...            # All read scopes
   write: Scope = ...           # All write scopes
   every: Scope = read + write  # All available scopes
"""

from enum import Enum


class AuthorisationScopes(Enum):
    """
    Web API authorisation scopes, also accessable with the alias :class:`scopes`.

    The string representation of a member is its enum value.

    .. code:: python

       s = scopes.user_read_email
       print(s)  # -> 'user-read-email'

    Addition and subtraction of two members is supported.
    Both operations return a :class:`Scope`.
    Subtraction is mainly implemented for consistency with scope objects.
    Subtracting any other scope simply returns the first operand,
    and subtracting the same scope returns an empty scope.

    .. code:: python

        janet = scopes.user_read_private + scopes.user_top_read
        mikey = scopes.user_follow_read - scopes.user_library_read
        blank = scopes.user_read_email - scopes.user_read_email
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

    def __add__(self, other: 'AuthorisationScopes') -> 'Scope':
        if not isinstance(other, AuthorisationScopes):
            return NotImplemented

        return Scope(self, other)

    def __sub__(self, other: 'AuthorisationScopes') -> 'Scope':
        if not isinstance(other, AuthorisationScopes):
            return NotImplemented

        return Scope(self) - other


scopes = AuthorisationScopes


class Scope(frozenset):
    """
    Set of :class:`AuthorisationScopes` constituting a scope for a token.

    Immutable, supports unpacking and flexible addition and subtraction
    with :class:`Scope`, :class:`str` and :class:`AuthorisationScopes`.
    Addition is a set-like union, subtraction is a set-like relative complement.
    The addition operation is also supported with reflected operands.
    Reflected subtraction tries to convert the left-side operand to a Scope.
    If any operation is unsuccessful, :class:`NotImplementError` is raised.

    .. code:: python

       bruce = Scope(*scopes)
       sally = Scope(scopes.user_read_email, scopes.user_read_private)
       timmy = Scope('ugc-image-upload', 'user-top-read')
       elise = Scope(*sally, *timmy, scopes.user_follow_modify)
       waldo = sally + timmy - 'user-read-email' + scopes.user_follow_read

       r_add = 'playlist-read-private' + timmy
       r_sub = 'user-top-read' - timmy

    The string representation of a :class:`Scope` is a sorted,
    space-separated concatenation of its members.

    .. code:: python

       s = Scope('b', 'c', 'a')
       print(s)  # -> 'a b c'
    """
    def __new__(cls, *members):
        return super().__new__(cls, [str(m) for m in members])

    def __str__(self):
        return ' '.join(sorted(self))

    def __add__(self, other) -> 'Scope':
        if isinstance(other, (str, AuthorisationScopes)):
            other = {str(other)}
        elif not isinstance(other, Scope):
            e = f'Addition not defined for {type(self)} and {type(other)}!'
            raise NotImplementedError(e)
        return type(self)(*self.union(other))

    def __radd__(self, other) -> 'Scope':
        return self + other

    def __sub__(self, other) -> 'Scope':
        if isinstance(other, (str, AuthorisationScopes)):
            other = {str(other)}
        elif not isinstance(other, Scope):
            e = f'Difference not defined for {type(self)} and {type(other)}!'
            raise NotImplementedError(e)
        return type(self)(*self.difference(other))

    def __rsub__(self, other) -> 'Scope':
        if not isinstance(other, (str, AuthorisationScopes)):
            e = f'Difference not defined for {type(other)} and {type(self)}!'
            raise NotImplementedError(e)
        return Scope(other) - self


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
