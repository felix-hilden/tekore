from enum import Enum


class scope(Enum):
    """
    User access token privileges.

    The string representation of a member is its enum value.

    .. code:: python

       s = tk.scope.user_read_email
       print(s)  # -> 'user-read-email'

    Also provides three scopes that are a combination of others.

    .. code:: python

        tk.scope.read: Scope = ...            # All read scopes
        tk.scope.write: Scope = ...           # All write scopes
        tk.scope.every: Scope = read + write  # All available scopes

    Addition and subtraction of two members is supported.
    Both operations return a :class:`Scope`.
    Subtraction is implemented for consistency with :class:`Scope` objects.
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
    user_read_playback_position = 'user-read-playback-position'
    user_modify_playback_state = 'user-modify-playback-state'

    playlist_modify_public = 'playlist-modify-public'
    playlist_read_collaborative = 'playlist-read-collaborative'
    playlist_read_private = 'playlist-read-private'
    playlist_modify_private = 'playlist-modify-private'

    ugc_image_upload = 'ugc-image-upload'

    def __str__(self):
        return self.value

    def __add__(self, other: 'scope') -> 'Scope':
        if not isinstance(other, scope):
            return NotImplemented

        return Scope(self, other)

    def __sub__(self, other: 'scope') -> 'Scope':
        if not isinstance(other, scope):
            return NotImplemented

        return Scope(self) - other


class Scope(frozenset):
    """
    Set of :class:`scopes <scope>` for a token.

    Immutable, supports unpacking and flexible addition and subtraction
    with :class:`Scope`, :class:`str` and :class:`scope`.
    Addition is a set-like union, subtraction is a set-like relative complement.
    The addition operation is also supported with reflected operands.
    Reflected subtraction tries to convert the left-side operand to a Scope.
    If any operation is unsuccessful, :class:`NotImplementedError` is raised.

    .. code:: python

       bruce = tk.Scope(*tk.scope)
       sally = tk.Scope(tk.scope.user_read_email, tk.scope.user_read_private)
       timmy = tk.Scope('ugc-image-upload', 'user-top-read')
       elise = tk.Scope(*sally, *timmy, tk.scope.user_follow_modify)
       waldo = sally + timmy - 'user-read-email' + tk.scopes.user_follow_read

       r_add = 'playlist-read-private' + timmy
       r_sub = 'user-top-read' - timmy

    The string representation of a :class:`Scope` is a sorted,
    space-separated concatenation of its members.

    .. code:: python

       s = tk.Scope('b', 'c', 'a')
       print(s)  # -> 'a b c'
    """
    def __new__(cls, *members):
        return super().__new__(cls, [str(m) for m in members])

    def __repr__(self):
        members = "'" + "', '".join(sorted(self)) + "'"
        return f'Scope({members})'

    def __str__(self):
        return ' '.join(sorted(self))

    def __add__(self, other) -> 'Scope':
        if isinstance(other, (str, scope)):
            other = {str(other)}
        elif not isinstance(other, Scope):
            e = f'Addition not defined for {type(self)} and {type(other)}!'
            raise NotImplementedError(e)
        return type(self)(*self.union(other))

    def __radd__(self, other) -> 'Scope':
        return self + other

    def __sub__(self, other) -> 'Scope':
        if isinstance(other, (str, scope)):
            other = {str(other)}
        elif not isinstance(other, Scope):
            e = f'Difference not defined for {type(self)} and {type(other)}!'
            raise NotImplementedError(e)
        return type(self)(*self.difference(other))

    def __rsub__(self, other) -> 'Scope':
        if not isinstance(other, (str, scope)):
            e = f'Difference not defined for {type(other)} and {type(self)}!'
            raise NotImplementedError(e)
        return Scope(other) - self


scope.read = Scope(
    scope.user_read_email,
    scope.user_read_private,
    scope.user_top_read,
    scope.user_read_recently_played,
    scope.user_follow_read,
    scope.user_library_read,
    scope.user_read_currently_playing,
    scope.user_read_playback_state,
    scope.user_read_playback_position,
    scope.playlist_read_collaborative,
    scope.playlist_read_private
)
scope.write = Scope(
    scope.user_follow_modify,
    scope.user_library_modify,
    scope.user_modify_playback_state,
    scope.playlist_modify_public,
    scope.playlist_modify_private,
    scope.ugc_image_upload
)
scope.every = scope.read + scope.write
