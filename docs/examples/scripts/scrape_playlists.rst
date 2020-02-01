Scrape playlist artists
=======================
The following script retrieves all tracks of your playlists
and aggregates the most common artists by total track count.

It assumes that your credentials are saved in the environment and
you have followed or created at least one playlist.

Asynchronous functions should be used to achieve a faster runtime
when making lots of parallelisable calls to the API.
To avoid errors when hitting rate limits,
a :class:`RetryingSender <tekore.sender.RetryingSender>` is used.

.. code:: python

    import asyncio
    from collections import Counter

    from tekore import util, Spotify
    from tekore.scope import scopes
    from tekore.sender import AsyncPersistentSender, RetryingSender

    conf = util.config_from_environment()
    scope = scopes.playlist_read_private
    token = util.prompt_for_user_token(*conf, scope=scope)

    sender = RetryingSender(sender=AsyncPersistentSender())
    spotify = Spotify(token, sender=sender)


    async def count_artists(playlist_id: str):
        tracks = await spotify.playlist_tracks(playlist_id)
        tracks = spotify.all_items(tracks)
        return Counter([t.track.artists[0].name async for t in tracks])


    async def main() -> Counter:
        playlists = await spotify.followed_playlists()
        playlists = spotify.all_items(playlists)
        counts = [await count_artists(p.id) async for p in playlists]
        return sum(counts, Counter())


    artists = asyncio.run(main())

    for name, count in artists.most_common(3):
        print(count, name)
