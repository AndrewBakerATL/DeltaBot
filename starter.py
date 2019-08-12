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
    async def terms(self, ctx):
        channel = ctx.message.channel
        server = ctx.message.server
        member = ctx.message.author
        await self.bot.send_message(channel, "**Terms & Condtitions** | Accepting the Terms")
        await self.bot.send_message(channel, "Whether agreed upon or not, this server is moderated by **Delta Bot**. Because of this, the server uses a specific set of Terms & Conditions, or rules, and it's required to agree upon these rules to gain full access to the server. Should you have read the Terms and Conditions made available to you already in the applicable channel, please use the command `accept` to join the server.")

    #@commands.command(pass_context=True)
    #async def accept(self, ctx):
#        channel = ctx.message.channel
#        server = ctx.message.server
#        member = ctx.message.author
#        role = discord.utils.get(ctx.server.roles, name='M')
#        await self.bot.send_message("**Terms & Conditions** | *Accepted*")
#        await self.bot.send_message("Granting access to the server and applying applicable roles. This process may take a minute...")
#        await self.bot.send_message("**Status** | *Loading Roles...*")
#        await self.bot.add_roles(member, role)
#        await self.bot.send_message("**Status** | *Role Granted, Process Complete*")

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
        await self.bot.send_message(channel, "**Creating Newbie Role |** *Done*")
        await self.bot.send_message(channel, "**Creating Member Role |** *Loading...*")
        await self.bot.send_message(channel, "Creating the role for server members. This is going to be named, 'Member'. This will signify agreement with the terms and conditions. Other mechanics rely on this. Do not change this name.")
        await self.bot.create_role(server, name='Member', hoist=True, mentionable=True)
        await self.bot.send_message(channel, "**Creating Member Role |** *Done*")
        await self.bot.send_message(channel, "**Setup Complete |** *Delta Bot*")
        await self.bot.send_message(channel, "Your setup is complete. You should find the channels to your left, the roles in your server settings, and the welcome channel allocation in your server settings. Feel free to adjust permissions how you see fit and set the welcome channel.")

    @commands.command(pass_context=True)
    async def advstart(self, ctx):
        #Objects
        channel = ctx.message.channel
        server = ctx.message.server
        muted = await self.bot.create_role(server, name='Muted', hoist=True, mentionable=True)
        permissions = discord.Permissions(permissions=1115136)
        color = discord.Colour(0x0d0909)
        #Starter Channels
        #Welcome Channel
        await self.bot.send_message(channel, "**Creating Welcome Channel |** *Loading...*")
        await self.bot.send_message(channel, "Creating the welcome channel and placing at the top of the list. This should be the channel set to the server welcome channel in your server settings. Do not change this name.")
        await self.bot.create_channel(server, 'welcome', type=discord.ChannelType.text)
        await self.bot.send_message(channel, "**Creating Welcome Channel |** *Done*")
        #Logging Channel
        await self.bot.send_message(channel, "**Creating Logging Channel |** *Loading...*")
        await self.bot.send_message(channel, "Creating the logging channel and placing at the top of the list. This is the channel that all the logs and server events will report to. This is your source of information on events. Do not change this name.")
        await self.bot.create_channel(server, 'server-logs', type=discord.ChannelType.text)
        await self.bot.send_message(channel, "**Creating Logging Channel |** *Done*")
        #Terms Channel
        await self.bot.send_message(channel, "**Creating Terms Channel |** *Loading...*")
        await self.bot.send_message(channel, "Creating the terms channel and placing at the top of the list. This is the dedicated channel for your server rules and / or conditions Any terms of use, or terms and conditions should be placed here. This name can be changed, but it will break record keeping.")
        await self.bot.create_channel(server, 'terms-conditions', type=discord.ChannelType.text)
        await self.bot.send_message(channel, "**Creating Terms Channel |** *Done*")
        #creating Roles
        #Newcomer Role
        await self.bot.send_message(channel, "**Creating Newbie Role |** *Loading...*")
        await self.bot.send_message(channel, "Creating the role for new members. This is going to be named, 'Newcomer'. Other mechnics rely on this. Do not change this name.")
        await self.bot.create_role(server, name='Newcomer', hoist=True, mentionable=True)
        await self.bot.send_message(channel, "**Creating Newbie Role |** *Done*")
        #Member Role
        await self.bot.send_message(channel, "**Creating Member Role |** *Loading...*")
        await self.bot.send_message(channel, "Creating the role for server members. This is going to be named, 'Member'. This will signify agreement with the terms and conditions. Other mechanics rely on this. Do not change this name.")
        await self.bot.create_role(server, name='Member', hoist=True, mentionable=True)
        await self.bot.send_message(channel, "**Creating Member Role |** *Done*")
        #Creating the Mute Command
        role = discord.utils.get(ctx.message.server.roles, name='Muted')
        await self.bot.send_message(channel, "**Creating Mute Command |** *Loading...*")
        await self.bot.send_message(channel, "Creating the role for muted members. This is going to be named, 'Muted'. This will remove access to message, or talk, in all applicable channels. Other mechanics rely on this. Do not change this name.")
        await self.bot.edit_role(server, role=muted, name='Muted', permissions=permissions, color=color, hoist=True, mentionable=True)
        await self.bot.send_message(channel, "**Creating Mute Command |** *Done*")
        await self.bot.send_message(channel, "**Setup Complete |** *Delta Bot*")
        await self.bot.send_message(channel, "Your setup is complete. You should find the channels to your left, the roles in your server settings, and the welcome channel allocation in your server settings. Feel free to adjust permissions how you see fit and set the welcome channel.")


        #Creating Level Roles
        await self.bot.create_role(server, name='Level 0', hoist=True, mentionable=True)
        await self.bot.create_role(server, name='Level 5', hoist=True, mentionable=True)
        await self.bot.create_role(server, name='Level 10', hoist=True, mentionable=True)
        await self.bot.create_role(server, name='Level 15', hoist=True, mentionable=True)
        await self.bot.create_role(server, name='Level 20', hoist=True, mentionable=True)
        await self.bot.create_role(server, name='Level 25', hoist=True, mentionable=True)
        await self.bot.create_role(server, name='Level 30', hoist=True, mentionable=True)
        await self.bot.create_role(server, name='Level 35', hoist=True, mentionable=True)
        await self.bot.create_role(server, name='Level 40', hoist=True, mentionable=True)
        await self.bot.create_role(server, name='Level 45', hoist=True, mentionable=True)
        await self.bot.create_role(server, name='Level 50', hoist=True, mentionable=True)

def setup(bot):
    bot.add_cog(Starter(bot))
