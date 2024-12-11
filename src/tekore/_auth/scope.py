from enum import Enum


class scope(Enum):  # noqa: N801
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

    .. note::

        :attr:`app_remote_control` and :attr:`streaming` are only used outside
        of the Web API, and are not included in the premade scope combinations.

    Addition and subtraction from both sides is supported
    but delegated to :class:`Scope` and always returns a :class:`Scope`.
    """

    user_read_email = "user-read-email"
    user_read_private = "user-read-private"
    user_top_read = "user-top-read"
    user_read_recently_played = "user-read-recently-played"

    user_follow_read = "user-follow-read"
    user_follow_modify = "user-follow-modify"
    user_library_read = "user-library-read"
    user_library_modify = "user-library-modify"

    user_read_currently_playing = "user-read-currently-playing"
    user_read_playback_state = "user-read-playback-state"
    user_read_playback_position = "user-read-playback-position"
    user_modify_playback_state = "user-modify-playback-state"

    playlist_modify_public = "playlist-modify-public"
    playlist_read_collaborative = "playlist-read-collaborative"
    playlist_read_private = "playlist-read-private"
    playlist_modify_private = "playlist-modify-private"

    ugc_image_upload = "ugc-image-upload"

    app_remote_control = "app-remote-control"
    streaming = "streaming"

    def __str__(self) -> str:
        """Enum value."""
        return self.value

    def __add__(self, other) -> "Scope":
        """Combine to a set of scopes."""
        return Scope(self) + other

    def __radd__(self, other) -> "Scope":
        """Combine to a set of scopes."""
        return other + Scope(self)

    def __sub__(self, other) -> "Scope":
        """Remove scope from another."""
        return Scope(self) - other

    def __rsub__(self, other) -> "Scope":
        """Remove scope from another."""
        return other - Scope(self)


class Scope(frozenset):
    """
    Set of :class:`scopes <scope>` for a token.

    Instantiated with an unpacked list of strings or :class:`scopes <scope>`.

    .. code:: python

        bruce = tk.Scope(*tk.scope)
        sally = tk.Scope(tk.scope.user_read_email, 'ugc-image-upload')
        elise = tk.Scope(*sally, *timmy, tk.scope.user_follow_modify)

    Also supports flexible addition and subtraction from both sides
    with strings, :class:`scopes <scope>` and other :class:`Scope` objects.
    Addition is a set-like union, subtraction is a set-like relative complement.
    If any operation is unsuccessful, :class:`NotImplementedError` is raised.

    .. code:: python

        waldo = tk.scopes.user_follow_read + sally + elise - 'user-read-email'

    The string representation of a :class:`Scope` is a sorted,
    space-separated concatenation of its members.

    .. code:: python

       s = tk.Scope('b', 'c', 'a')
       print(s)  # -> 'a b c'
    """

    def __new__(cls, *members) -> "Scope":
        """
        Construct a new set of scopes.

        Parameters
        ----------
        members
            unpacked list of members of the new scope
        """
        return super().__new__(cls, [str(m) for m in members])

    def __repr__(self) -> str:
        """Readable representation."""
        members = "'" + "', '".join(sorted(self)) + "'"
        return f"Scope({members})"

    def __str__(self) -> str:
        """Join members with spaces."""
        return " ".join(sorted(self))

    def __add__(self, other) -> "Scope":
        """Combine two sets of scopes."""
        if isinstance(other, (str, scope)):
            other = {str(other)}
        elif not isinstance(other, Scope):
            e = f"Addition not defined for {type(self)} and {type(other)}!"
            raise NotImplementedError(e)
        return type(self)(*self.union(other))

    def __radd__(self, other) -> "Scope":
        """Combine two sets of scopes."""
        return self + other

    def __sub__(self, other) -> "Scope":
        """Remove scopes from a set."""
        if isinstance(other, (str, scope)):
            other = {str(other)}
        elif not isinstance(other, Scope):
            e = f"Difference not defined for {type(self)} and {type(other)}!"
            raise NotImplementedError(e)
        return type(self)(*self.difference(other))

    def __rsub__(self, other) -> "Scope":
        """Remove scopes from a set."""
        if not isinstance(other, (str, scope)):
            e = f"Difference not defined for {type(other)} and {type(self)}!"
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
    scope.playlist_read_private,
)
scope.write = Scope(
    scope.user_follow_modify,
    scope.user_library_modify,
    scope.user_modify_playback_state,
    scope.playlist_modify_public,
    scope.playlist_modify_private,
    scope.ugc_image_upload,
)
scope.every = scope.read + scope.write
