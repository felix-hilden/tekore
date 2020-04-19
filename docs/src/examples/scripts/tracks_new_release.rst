Tracks of a new release
=======================
The following script shows the tracks of a newly released album.

It assumes that your credentials are saved in the environment and
there is at least new release in the Spotify catalogue.

.. code:: python

    import tekore as tk

    conf = tk.config_from_environment()
    token = tk.request_client_token(*conf[:2])

    spotify = tk.Spotify(token)
    simple_album = spotify.new_releases(limit=1).items[0]
    album = spotify.album(simple_album.id)

    print(f'Songs from {album.album_type} {album.name}:')
    for t in album.tracks.items:
        print(t.track_number, '-', t.name)
