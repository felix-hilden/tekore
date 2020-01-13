Follow category playlist
========================
The following script retrieves a Spotify playlist in one of the preset
categories and follows it as the current user.

It assumes that your credentials are saved in the environment.

.. code:: python

    from tekore import util, Spotify
    from tekore.scope import scopes

    conf = util.config_from_environment()
    scope = scopes.playlist_modify_private
    token = util.prompt_for_user_token(*conf, scope=scope)

    spotify = Spotify(token)
    category = spotify.categories(limit=1).items[0]
    playlist = spotify.category_playlists(category.id, limit=1).items[0]

    print(f'Following "{playlist.name}"" from category "{category.name}"...')
    spotify.playlist_follow(playlist.id, public=False)
