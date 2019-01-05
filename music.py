import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import chalk
from itertools import cycle
import youtube_dl
import json
import os

players = {}
queues = {}

class Music:
    def __init__(self, bot):
        self.bot = bot

    def check_queue(id):
        if queues[id] != []:
            player = queues[id].pop(0)
            players[id] = player
            player.start()

    @commands.command(pass_context=True)
    async def join(self, ctx):
        channel = ctx.message.author.voice.voice_channel
        await self.bot.join_voice_channel(channel)

    @commands.command(pass_context=True)
    async def leave(self, ctx):
        server = ctx.message.server
        voice_client = self.bot.voice_client_in(server)
        await voice_client.disconnect()

    @commands.command(pass_context=True)
    async def play(self, ctx, *, url):
        server = ctx.message.server
        voice_client = self.bot.voice_client_in(server)
        player = await voice_client.create_ytdl_player(f"ytsearch:{url}", after=lambda: check_queue(server.id))
        players[server.id] = player
        channel = ctx.message.author.voice.voice_channel

        if self.bot in channel:
            player.start()
        else:
            await self.bot.join_voice_channel(channel)
            player.start()

        await self.bot.say("**Playing Song** -> `` {} ``".format(url))

    @commands.command(pass_context=True)
    async def pause(self, ctx):
        id = ctx.message.server.id
        players[id].pause()
        await self.bot.say("**Pausing Playback**")

    @commands.command(pass_context=True)
    async def stop(self, ctx):
        id = ctx.message.server.id
        players[id].stop()
        await self.bot.say("**Stopping Playback**")

    @commands.command(pass_context=True)
    async def resume(self, ctx):
        id = ctx.message.server.id
        players[id].resume()
        await self.bot.say("**Resuming Playback**")

    @commands.command(pass_context=True)
    async def queue(self, ctx, *, url):
        server = ctx.message.server
        voice_client = self.bot.voice_client_in(server)
        player = await voice_client.create_ytdl_player(f"ytsearch:{url}", after=lambda: check_queue(server.id))

        if server.id in queues:
            queues[server.id].append(player)
        else:
            queues[server.id] = [player]

        await self.bot.say("**Added To Queue** -> `` {} ``".format(url))

    @commands.command(pass_context=True)
    async def skip(self, ctx):
        server = ctx.message.server
        id = ctx.message.server.id
        if server.id in queues:
            players[id].stop()
            await self.bot.say("**Skipping Song**")
        else:
            await self.bot.say("**Queue is Empty**")

    @commands.command(pass_context=True)
    async def queued(self, ctx):
        server = ctx.message.server
        id = ctx.message.server.id
        channel = ctx.message.channel
        if server.id in queues:
            embed = discord.Embed(title='**Song Queue** | :musical_note: ', description="{}'s Song Queue".format(server.name), color=0xfc4156)
            embed.add_field(name="**Queued Songs**", value=queues.values())
            embed.set_thumbnail(url=server.icon_url)
            await self.bot.send_message(channel, embed=embed)
        else:
            await self.bot.say("**Queue is Empty**")

def setup(bot):
    bot.add_cog(Music(bot))
