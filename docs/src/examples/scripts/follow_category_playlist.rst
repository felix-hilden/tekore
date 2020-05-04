Follow category playlist
========================
The following script retrieves a Spotify playlist in one of the preset
categories and follows it as the current user.

It assumes that your credentials are saved in the environment.

.. code:: python

    import tekore as tk

    conf = tk.config_from_environment()
    scope = tk.scope.playlist_modify_private
    token = tk.prompt_for_user_token(*conf, scope=scope)

    spotify = tk.Spotify(token)
    category = spotify.categories(limit=1).items[0]
    playlist = spotify.category_playlists(category.id, limit=1).items[0]

    print(f'Following "{playlist.name}"" from category "{category.name}"...')
    spotify.playlist_follow(playlist.id, public=False)
