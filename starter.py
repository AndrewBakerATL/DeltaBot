import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import chalk
from itertools import cycle
import youtube_dl
import json
import os

class Starter:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def intro(self, ctx):
        channel = ctx.message.channel
        server = ctx.message.server
        member = ctx.message.author
        await self.bot.send_message(channel, "**Welcome To The Introduction |** *Delta Bot*")
        await self.bot.send_message(channel, "The user {} has triggered the Getting Started process from the command list, running in server {}. The following actions are being requested. Delta will create the necessary channels and roles for those wanting an automated solution. From this part forward, at least two channels will be created, as well as two roles. Delta will create both a welcome channel and a logging channel. As of this moment, it's still up to the individual users to configure channel and role permissions. This may change in a future release, but stands for now. It's imperative that these channels' and roles' names are not changed for the bot to function correctly. Delta isn't responsible for any user error, which may include changing channel names.".format(member.mention, server))
        await self.bot.send_message(channel, "**Acknowledgement** | *Starting*")
        await self.bot.send_message(channel, "If you understand this and want to continue, run the command, ``start``.")

    @commands.command(pass_context=True)
    async def start(self, ctx):
        channel = ctx.message.channel
        server = ctx.message.server
        await self.bot.send_message(channel, "**Creating Welcome Channel |** *Loading...*")
        await self.bot.send_message(channel, "Creating the welcome channel and placing at the top of the list. This should be the channel set to the server welcome channel in your server settings. Do not change this name.")
        await self.bot.create_channel(server, 'welcome', type=discord.ChannelType.text)
        await self.bot.send_message(channel, "**Creating Welcome Channel |** *Done*")
        await self.bot.send_message(channel, "**Creating Logging Channel |** *Loading...*")
        await self.bot.send_message(channel, "Creating the logging channel and placing at the top of the list. This is the channel that all the logs and server events will report to. This is your source of information on events. Do not change this name.")
        await self.bot.create_channel(server, 'server-logs', type=discord.ChannelType.text)
        await self.bot.send_message(channel, "**Creating Logging Channel |** *Done*")
        await self.bot.send_message(channel, "**Creating Terms Channel |** *Loading...*")
        await self.bot.send_message(channel, "Creating the terms channel and placing at the top of the list. This is the dedicated channel for your server rules and / or conditions Any terms of use, or terms and conditions should be placed here. This name can be changed, but it will break record keeping.")
        await self.bot.create_channel(server, 'terms-conditions', type=discord.ChannelType.text)
        await self.bot.send_message(channel, "**Creating Terms Channel |** *Done*")
        await self.bot.send_message(channel, "**Creating Newbie Role |** *Loading...*")
        await self.bot.send_message(channel, "Creating the role for new members. This is going to be named, 'Newcomer'. Other mechnics rely on this. Do not change this name.")
        await self.bot.create_role(server, name='Newcomer', hoist=True, mentionable=True)
        await self.bot.send_message(channel, "**Creating Member Role |** *Done*")
        await self.bot.send_message(channel, "Creating the role for server members. This is going to be named, 'Member'. This will signify agreement with the terms and conditions. Other mechanics rely on this. Do not change this name.")
        await self.bot.create_role(server, name='Member', hoist=True, mentionable=True)
        await self.bot.send_message(channel, "**Creating Member Role |** *Done*")
        await self.bot.send_message(channel, "**Setup Complete |** *Delta Bot*")
        await self.bot.send_message(channel, "Your setup is complete. You should find the channels to your left, the roles in your server settings, and the welcome channel allocation in your server settings. Feel free to adjust permissions how you see fit and set the welcome channel.")

def setup(bot):
    bot.add_cog(Starter(bot))
