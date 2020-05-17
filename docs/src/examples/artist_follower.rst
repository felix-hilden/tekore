Artist follower
===============
This script will find all the artists you aren't already following
from your playlists, and prompt you to do so.

.. code:: python

    import tekore as tk

    conf = tk.config_from_environment()
    scope = [
        tk.scope.user_follow_read,
        tk.scope.user_follow_modify,
        tk.scope.playlist_read_private
    ]
    user_token = tk.prompt_for_user_token(*conf, scope=scope)
    s = tk.Spotify(user_token, max_limits_on=True, chunked_on=True)


    def prompt_user(what: str) -> bool:
        while True:
            resp = input(f"{what} [Y/n]: ").strip()
            if resp.lower() == "y" or resp == "":
                return True
            elif resp.lower() == "n":
                return False


    artists = set()
    for playlist in s.all_items(s.followed_playlists()):
        if not prompt_user(f"Analyze playlist '{playlist.name}'?"):
            continue

        for item in s.all_items(s.playlist_items(playlist.id)):
            if not item.track.track or item.track.is_local:
                continue

            for artist in item.track.artists:
                artists.add((artist.id, artist.name))


    ids = [a[0] for a in artists]
    names = [a[1] for a in artists]
    following = s.artists_is_following(ids)
    for id_, name, status in zip(ids, names, following):
        if status:
            print(f"Skipping '{name}' as it's already being followed.")
            continue

        if not prompt_user(f"Follow '{name}'?"):
            continue

        s.artists_follow([id_])
        print(f"Followed '{name}'.")
