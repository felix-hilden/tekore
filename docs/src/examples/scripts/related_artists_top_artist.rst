Related artists of user's top artist
====================================
The following script shows artists related to one of your top artists
and whether you have followed them or not.

It assumes that your credentials are saved in the environment
and you have used Spotify enough to have top artists.

.. code:: python

    import tekore as tk

    conf = tk.config_from_environment()
    scope = tk.scope.user_top_read + tk.scope.user_follow_read
    token = tk.prompt_for_user_token(*conf, scope=scope)

    spotify = tk.Spotify(token)
    artist = spotify.current_user_top_artists(limit=1).items[0]
    related = spotify.artist_related_artists(artist.id)
    followed = spotify.followed_artists(limit=50)
    followed = spotify.all_items(followed)
    followed_ids = [f.id for f in followed]

    print(f'Artists related to {artist.name}:')
    for a in related:
        f = ' F -' if a.id in followed_ids else 'NF -'
        print(f, a.name)
