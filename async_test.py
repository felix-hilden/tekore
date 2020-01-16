import asyncio

from httpx import AsyncClient

from tekore import SpotifyAsync
from tekore.util import request_client_token

client_id = 'fb0cb8329a2d4711b35bcf125a5e3d43'
client_secret = 'c745313550404335b44524df80455b50'

# Can also be converted to async
app_token = request_client_token(client_id, client_secret)
spotify = SpotifyAsync(app_token)

async def main():
    album = await spotify.album('3RBULTZJ97bvVzZLpxcB0j')
    for track in album.tracks.items:
        print(track.track_number, track.name)

if __name__ == "__main__":
    asyncio.run(main())
