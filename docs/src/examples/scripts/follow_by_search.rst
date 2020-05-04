Follow with a search
====================
The following script searches for an artist
and prompts the user to follow the first match.

It assumes that your credentials are saved in the environment.

.. code:: python

    import tekore as tk

    conf = tk.config_from_environment()
    scope = tk.scope.user_follow_modify
    token = tk.prompt_for_user_token(*conf, scope=scope)
    spotify = tk.Spotify(token)

    search = input('Search for an artist: ')
    artists, = spotify.search(search, types=('artist',), limit=1)
    artist = artists.items[0]
    follow = input(f'Follow {artist.name}? (y/n) ')

    if follow.lower() == 'y':
        spotify.artists_follow([artist.id])
        print(f'{artist.name} followed.')
    else:
        print('Follow cancelled.')
