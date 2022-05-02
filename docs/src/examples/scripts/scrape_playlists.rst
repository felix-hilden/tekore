.. _scrape-playlists:

.. currentmodule:: tekore

Scrape playlist artists
=======================
The following script retrieves all tracks of your playlists
and aggregates the most common artists by total track count.

It assumes that your credentials are saved in the environment and
you have followed or created at least one playlist.
For this example, the artist of podcast episodes is the name of the show.
To avoid errors when hitting rate limits, a :class:`RetryingSender` is used.

.. code:: python

    import asyncio
    import tekore as tk

    from collections import Counter

    conf = tk.config_from_environment()
    scope = tk.scope.playlist_read_private
    token = tk.prompt_for_user_token(*conf, scope=scope)


    def get_artist(track) -> str:
        if track.episode:
            return track.show.name
        else:
            return track.artists[0].name

Asynchronous functions can be used to achieve a faster runtime
when making lots of parallelisable calls to the API.
A series of asynchronous calls alone does not help much, but the calls can be
parallelised with :func:`asyncio.gather`.
The code is more complex, but with bigger workloads more time is saved.

.. tabs::

   .. tab:: Ordinary async

      .. code:: python

          async def count_artists(spotify: tk.Spotify, playlist_id: str):
              tracks = await spotify.playlist_items(playlist_id)
              tracks = spotify.all_items(tracks)
              return Counter([get_artist(t.track) async for t in tracks])


          async def main() -> Counter:
              sender = tk.RetryingSender(sender=tk.AsyncSender())
              spotify = tk.Spotify(token, sender=sender, max_limits_on=True)

              playlists = await spotify.followed_playlists()
              playlists = spotify.all_items(playlists)
              counts = [await count_artists(spotify, p.id) async for p in playlists]

              await spotify.close()
              return sum(counts, Counter())


          artists = asyncio.run(main())

          for name, count in artists.most_common(3):
              print(count, name)

   .. tab:: Parallel async

      .. code:: python

          async def count_artists(spotify: tk.Spotify, playlist_id: str):
              tracks_paging = await spotify.playlist_items(playlist_id)
              paging_len = len(tracks_paging.items)
              track_calls = [
                  spotify.playlist_items(playlist_id, offset=ofs)
                  for ofs in range(paging_len, tracks_paging.total, paging_len)
              ]
              pages = [tracks_paging] + await asyncio.gather(*track_calls)
              tracks = sum([page.items for page in pages], [])
              return Counter([get_artist(t.track) for t in tracks])


          async def main() -> Counter:
              sender = tk.RetryingSender(sender=tk.AsyncSender())
              spotify = tk.Spotify(token, sender=sender, max_limits_on=True)

              playlists_paging = await spotify.followed_playlists()
              paging_len = len(playlists_paging.items)
              playlist_calls = [
                  spotify.followed_playlists(offset=ofs)
                  for ofs in range(paging_len, playlists_paging.total, paging_len)
              ]
              pages = [playlists_paging] + await asyncio.gather(*playlist_calls)
              playlists = sum([page.items for page in pages], [])

              count_calls = [count_artists(spotify, p.id) for p in playlists]
              counts = await asyncio.gather(*count_calls)

              await spotify.close()
              return sum(counts, Counter())


          artists = asyncio.run(main())

          for name, count in artists.most_common(3):
              print(count, name)
