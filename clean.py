import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import chalk
from itertools import cycle
import youtube_dl
import json
import os

class Verification:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def clear(self, ctx, amount=5):
        channel = ctx.message.channel
        messages = []
        async for message in self.bot.logs_from(channel, limit=int(amount)):
            messages.append(message)
        await self.bot.delete_messages(messages)
        await self.bot.say('Messages Deleted')

    @commands.command(pass_context=True)
    async def purge(self, ctx, amount=5):
        channel = ctx.message.channel
        deleted = await self.bot.purge_from(channel, limit=int(amount))
        await self.bot.send_message(channel, 'Deleted {} message(s)'.format(len(deleted)))

def setup(bot):
    bot.add_cog(Verification(bot))
