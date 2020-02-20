Discord bot
===========
The following example script creates a simple Discord bot that can be used to search tracks.

A bot account is required for sending messages in Discord.
A quickstart guide for setting up a bot can be found here_.

Once the bot is added to the server users can call it with the prefix ``>tk track``.
The bot responds to the query by sending a brief summary of the search results.
Queries can be for example:

.. code::

    >tk track Sheeran
    >tk track "Monty Python"

.. _here: https://discordpy.readthedocs.io/en/latest/quickstart.html#

.. code:: python

    from discord import Game, Embed
    from discord.ext import commands

    from tekore import Spotify
    from tekore.util import request_client_token, config_from_environment

    token_discord = "your_discord_token"
    conf = config_from_environment()
    token_spotify = request_client_token(*conf[:2])

    description = "Spotify track search bot using Tekore"
    bot = commands.Bot(command_prefix='>tk ', description=description)
    spotify = Spotify(token_spotify, asynchronous=True)


    @bot.command(help="Multiword query in quotes")
    async def track(ctx, query: str = None):
        if query is None:
            await ctx.send("No search query specified")
            return

        tracks, = await spotify.search(query, limit=5)
        embed = Embed(title="Track search results", color=0x1DB954)
        embed.set_thumbnail(url="https://i.imgur.com/890YSn2.png")
        embed.set_footer(text="Requested by " + ctx.author.display_name)

        for t in tracks.items:
            artist = t.artists[0].name
            url = t.external_urls["spotify"]

            message = "\n".join([
                "[Spotify](" + url + ")",
                ":busts_in_silhouette: " + artist,
                ":cd: " + t.album.name
            ])
            embed.add_field(name=t.name, value=message, inline=False)

        await ctx.send(embed=embed)


    @bot.event
    async def on_ready():
        print("Ready to demo!")
        await bot.change_presence(activity=Game(name=">tk help"))


    if __name__ == "__main__":
        bot.run(token_discord)
