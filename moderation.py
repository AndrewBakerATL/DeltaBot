import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import chalk
from itertools import cycle
import youtube_dl
import json
import os

class Moderation:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.has_role("Admin")
    async def kick(self, ctx, user: discord.Member):
        server_log = discord.utils.get(user.server.channels, name='server-logs')
        channel = ctx.message.channel
        embed = discord.Embed(title="Kicking User", description="Taking action on `{}`'s  File From `{} Database`".format(user.name, ctx.message.server.name), color=0xfc4156)
        embed.set_footer(text="Delta Discipline Report")
        embed.set_author(name="Discipline Report", icon_url="https://cdn.discordapp.com/app-icons/481923206848970803/394817ba790d2fbb9c36715a7ec00576.png")
        embed.add_field(name="User Name", value="`Name:` | {}".format(user.name), inline=True)
        embed.add_field(name="User ID", value="`ID:` | {}".format(user.id), inline=True)
        embed.add_field(name="User Role", value="`Highest:` | {} ".format(user.top_role), inline=True)
        embed.add_field(name="Date Joined", value="`Joined:` | {}".format(user.joined_at), inline=True)
        embed.add_field(name="Action Taken", value="`Discipline:` | **Kicked {} **".format(user.name), inline=True)
        embed.set_thumbnail(url=user.avatar_url)
        await self.bot.send_message(channel, embed=embed)
        await self.bot.send_message(server_log, embed=embed)
        await self.bot.kick(user)

    @commands.command(pass_context=True)
    @commands.has_role("Admin")
    async def ban(self, ctx, user: discord.Member):
        server_log = discord.utils.get(user.server.channels, name='server-logs')
        channel = ctx.message.channel
        embed = discord.Embed(title="Banning User", description="Taking action on `{}`'s  File From `{} Database`".format(user.name, ctx.message.server.name), color=0xfc4156)
        embed.set_footer(text="Delta Discipline Report")
        embed.set_author(name="Discipline Report", icon_url="https://cdn.discordapp.com/app-icons/481923206848970803/394817ba790d2fbb9c36715a7ec00576.png")
        embed.add_field(name="User Name", value="`Name:` | {}".format(user.name), inline=True)
        embed.add_field(name="User ID", value="`ID:` | {}".format(user.id), inline=True)
        embed.add_field(name="User Role", value="`Highest:` | {} ".format(user.top_role), inline=True)
        embed.add_field(name="Date Joined", value="`Joined:` | {}".format(user.joined_at), inline=True)
        embed.add_field(name="Action Taken", value="`Discipline:` | **Banned {} **".format(user.name), inline=True)
        embed.set_thumbnail(url=user.avatar_url)
        await self.bot.send_message(channel, embed=embed)
        await self.bot.send_message(server_log, embed=embed)
        await self.bot.ban(user)

    @commands.command(pass_context=True)
    @commands.has_role("Admin")
    async def hammer(self, ctx, user: discord.Member):
        server_log = discord.utils.get(user.server.channels, name='server-logs')
        channel = ctx.message.channel
        embed = discord.Embed(title="Banning User", description="Taking action on `{}`'s  File From `{} Database`".format(user.name, ctx.message.server.name), color=0xfc4156)
        embed.set_footer(text="Delta Discipline Report")
        embed.set_author(name="Discipline Report", icon_url="https://cdn.discordapp.com/app-icons/481923206848970803/394817ba790d2fbb9c36715a7ec00576.png")
        embed.add_field(name="User Name", value="`Name:` | {}".format(user.name), inline=True)
        embed.add_field(name="User ID", value="`ID:` | {}".format(user.id), inline=True)
        embed.add_field(name="User Role", value="`Highest:` | {} ".format(user.top_role), inline=True)
        embed.add_field(name="Date Joined", value="`Joined:` | {}".format(user.joined_at), inline=True)
        embed.add_field(name="Action Taken", value="`Discipline:` | **Banned {} **".format(user.name), inline=True)
        await self.bot.send_message(channel, embed=embed)
        await self.bot.send_message(server_log, embed=embed)
        await self.bot.ban(user, delete_message_days=7)

def setup(bot):
    bot.add_cog(Moderation(bot))
