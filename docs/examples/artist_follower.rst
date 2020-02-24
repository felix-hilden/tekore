Artist follower
===============
This script will find all the artists you aren't already following from your playlists, and prompt you to do so.

Note: the Spotify API will only return about 100 artists per playlist maximum.

.. code:: python

    from tekore import Spotify
    from tekore.util import prompt_for_user_token
    from tekore.scope import scopes


    # Credentials: client_id and client_secret should be changed
    client_id = ''
    client_secret = ''

    # Authenticating to Spotify
    user_token = prompt_for_user_token(
        client_id,
        client_secret,
        'http://localhost:8888/callback/',
        scope=scopes.user_follow_read + scopes.user_follow_modify \
                + scopes.playlist_read_private
    )
    s = Spotify(user_token)


    # The user will be prompted before following any artist.
    def prompt_user(what: str) -> bool:
        while True:
            resp = input(f"{what} [Y/n]: ").strip()
            if resp.lower() == "y" or resp == "":
                return True
            elif resp.lower() == "n":
                return False


    # Iterating all the playlists and artists inside them
    artists = set()
    for playlist in s.followed_playlists().items:
        if not prompt_user(f"Analyze playlist '{playlist.name}'?"):
            continue

        # All items in the playlist (tracks)
        for item in s.playlist_tracks(playlist.id).items:
            # All artists in the track
            for artist in item.track.artists:
                # Only follow new artists
                if artist.id in artists:
                    continue

                # And ones that aren't being followed already
                artists.add(artist.id)
                if s.artists_is_following([artist.id])[0]:
                    print(f"❌ Skipping '{artist.name}' as it's already being followed.")
                    continue

                if not prompt_user(f"Follow '{artist.name}'?"):
                    continue

                s.artists_follow([artist.id])
                print(f"✔️ Followed '{artist.name}'.")
