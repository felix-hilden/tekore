from enum import Enum


class AuthorisationScopes(Enum):
    """
    Spotify Web API Authorisation Scopes.
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

    streaming = 'streaming'
    app_remote_control = 'app-remote-control'


scopes = AuthorisationScopes


class Scope:
    """
    Set of AuthorisationScopes constituting a scope for a token.
    """
    def __init__(self, *members: AuthorisationScopes):
        self._members = set([m.value for m in members])

    @property
    def members(self):
        return self._members

    def __str__(self):
        return ' '.join(sorted(self.members))

    def __eq__(self, other: 'Scope') -> bool:
        return self.members == other.members

    def __lt__(self, other: 'Scope') -> bool:
        return self.members < other.members

    def __le__(self, other: 'Scope') -> bool:
        return self.members <= other.members

    def __gt__(self, other: 'Scope') -> bool:
        return self.members > other.members

    def __ge__(self, other: 'Scope') -> bool:
        return self.members >= other.members
