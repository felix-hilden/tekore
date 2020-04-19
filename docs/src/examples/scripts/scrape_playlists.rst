Scrape playlist artists
=======================
The following script retrieves all tracks of your playlists
and aggregates the most common artists by total track count.

It assumes that your credentials are saved in the environment and
you have followed or created at least one playlist.
For this example, the artist of podcast episodes is the name of the show.

Asynchronous functions should be used to achieve a faster runtime
when making lots of parallelisable calls to the API.
To avoid errors when hitting rate limits,
a :class:`RetryingSender <tekore.sender.RetryingSender>` is used.

.. code:: python

    import asyncio
    import tekore as tk

    from tekore.scope import scopes
    from collections import Counter

    conf = tk.config_from_environment()
    scope = scopes.playlist_read_private
    token = tk.prompt_for_user_token(*conf, scope=scope)

    sender = tk.RetryingSender(sender=tk.AsyncPersistentSender())
    spotify = tk.Spotify(token, sender=sender, max_limits_on=True)


    def get_artist(track) -> str:
        if getattr(track, 'episode', False):
            return track.show.name
        else:
            return track.artists[0].name


    async def count_artists(playlist_id: str):
        tracks = await spotify.playlist_tracks(playlist_id)
        tracks = spotify.all_items(tracks)
        return Counter([get_artist(t.track) async for t in tracks])


    async def main() -> Counter:
        playlists = await spotify.followed_playlists()
        playlists = spotify.all_items(playlists)
        counts = [await count_artists(p.id) async for p in playlists]
        return sum(counts, Counter())


    artists = asyncio.run(main())

    for name, count in artists.most_common(3):
        print(count, name)
