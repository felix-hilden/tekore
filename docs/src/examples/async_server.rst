.. _async-server:

Async server
============
The following scripts starts up a simple AIOHTTP web server for song search.

Run the script and navigate to ``localhost:5000`` to see the main page.
Enter search terms to the address bar to search for songs.

Asynchronous programming is particularly handy in web server contexts.
This is a small example, but the bottleneck of this server is Spotify's API.
Therefore at larger scale more requests can be served
using this configuration than the synchronous counterpart.
To demonstrate this, one can insert an artificial delay to the search call.
First :code:`import asyncio`, then insert :code:`await asyncio.sleep(10)`
somewhere in the function.
When searching in parallel (e.g. with two browser tabs) one should observe that
requests take about ten seconds, no matter how many are sent at once.

.. code:: python

    import tekore as tk
    from aiohttp import web

    conf = tk.config_from_environment()
    token = tk.request_client_token(*conf[:2])
    spotify = tk.Spotify(token, asynchronous=True)

    routes = web.RouteTableDef()

    @routes.get('/')
    async def main(_) -> web.Response:
        html = '<br>'.join([
            'Enter text in the address bar to search for songs!',
            'Search terms should be separated by plus signs.',
            'For example:',
            'host:5000/monty+python',
            'host:5000/bright+side',
        ])
        return web.Response(text=html, content_type='text/html')

    @routes.get('/{search}')
    async def search(request: web.Request) -> web.Response:
        # await asyncio.sleep(10)
        try:
            query = request.match_info['search'].replace('+', ' ')
            tracks, = await spotify.search(query, limit=5)
            items = [t.artists[0].name + ': ' + t.name for t in tracks.items]
            html = '<br>'.join(items)
            return web.Response(text=html, content_type='text/html')
        except Exception:
            return web.Response(text='An error occured while searching!')

    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, port=5000)
