Follow with a search
====================
The following script searches for an artist and follows the first match.

It assumes that your credentials are saved in the environment.

.. code:: python

    from tekore import util, Spotify
    from tekore.scope import scopes

    conf = util.config_from_environment()
    scope = scopes.user_follow_modify
    token = util.prompt_for_user_token(*conf, scope=scope)

    spotify = Spotify(token)
    artists, = spotify.search('sheeran', types=('artist',), limit=1)

    artist = artists.items[0]
    print(f'Following {artist.name}...')
    spotify.artists_follow([artist.id])
