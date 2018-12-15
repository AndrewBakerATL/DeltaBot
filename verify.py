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
    async def accept(self, ctx):
        channel = ctx.message.channel
        server = ctx.message.server
        member = ctx.message.author
        role = discord.utils.get(ctx.message.server.roles, name='Member')
        await self.bot.send_message(channel, "**Terms & Conditions |** *Accepted*")
        await self.bot.send_message(channel, "User, {}, has accepted the {}'s Terms & Conditons, as per the chat channel. They are now being allowed into the server and given the role of ``Member``.'".format(member.mention, server))
        await self.bot.send_message(channel, "**Verifying Role |** *Verifying & Adding*")
        await self.bot.send_message(channel, "Verifying that the user has the role. If user does not hold the role, granting them the role.")
        await self.bot.add_roles(member, role)
        await self.bot.send_message(channel, "**Verification Complete |** *Role Granted*")
        terms = discord.utils.get(ctx.message.server.channels, name='terms-conditions')
        await self.bot.send_message(terms, "**Terms & Conditions |** *Accepted*")
        await self.bot.send_message(terms, "User, {}, has accepted the {}'s Terms & Conditons, as per the chat channel. They are now being allowed into the server and given the role of ``Member``.'".format(member.mention, server))
        await self.bot.send_message(terms, "**Verifying Role |** *Verifying & Adding*")
        await self.bot.send_message(terms, "Verifying that the user has the role. If user does not hold the role, granting them the role.")
        await self.bot.send_message(terms, "**Verification Complete |** *Role Granted*")

def setup(bot):
    bot.add_cog(Verification(bot))
