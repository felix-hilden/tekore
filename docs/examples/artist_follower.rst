Artist follower
===============
This script will find all the artists you aren't already following
from your playlists, and prompt you to do so.

.. code:: python

    from tekore import Spotify
    from tekore.util import prompt_for_user_token, config_from_environment
    from tekore.scope import scopes, Scope

    conf = config_from_environment()
    scope = Scope(
        scopes.user_follow_read,
        scopes.user_follow_modify,
        scopes.playlist_read_private
    )
    user_token = prompt_for_user_token(*conf, scope=scope)
    s = Spotify(user_token, max_limits_on=True)


    def prompt_user(what: str) -> bool:
        while True:
            resp = input(f"{what} [Y/n]: ").strip()
            if resp.lower() == "y" or resp == "":
                return True
            elif resp.lower() == "n":
                return False


    def chunks(lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i + n]


    artists = set()
    for playlist in s.all_items(s.followed_playlists()):
        if not prompt_user(f"Analyze playlist '{playlist.name}'?"):
            continue

        for track in s.all_items(s.playlist_tracks(playlist.id)):
            for artist in track.track.artists:
                artists.add((artist.id, artist.name))


    for chunk in chunks(list(artists), 50):
        ids = [c[0] for c in chunk]
        names = [c[1] for c in chunk]
        following = s.artists_is_following(ids)
        for id_, name, status in zip(ids, names, following):
            if status:
                print(f"Skipping '{name}' as it's already being followed.")
                continue

            if not prompt_user(f"Follow '{name}'?"):
                continue

            s.artists_follow([id_])
            print(f"Followed '{name}'.")
