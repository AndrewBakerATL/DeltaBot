import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import chalk
from itertools import cycle
import youtube_dl
import json
import os

class Log:
    def __init__(self, bot):
        self.bot = bot

    async def on_member_join(self, member):
        channel = discord.utils.get(member.server.channels, name='welcome')
        role = discord.utils.get(member.server.roles, name='Newcomer')
        await self.bot.add_roles(member, role)
        await self.bot.send_message(channel, "**Welcome To The Server** | *{}*".format(member))
        await self.bot.send_message(channel, "Welcome to the server, {}. We hope you enjoy your stay. Staff is located to your right if you have any problems. Be aware that the server uses a #terms-conditions and take notice of it. If you have any problems, let us know.".format(member.mention))

        channel = discord.utils.get(member.server.channels, name='server-logs')
        embed = discord.Embed(title='**User Joined**', description='Detected User Join', color=0xfc4156)
        embed.add_field(name="**Name**", value=member, inline=False)
        embed.add_field(name="**Message**", value="User joined the server", inline=False)
        embed.add_field(name="**Date Joined**", value="`Joined:` | {}".format(member.joined_at), inline=True)
        embed.set_author(name="Data Report", icon_url="https://cdn.discordapp.com/app-icons/481923206848970803/394817ba790d2fbb9c36715a7ec00576.png")
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text="Delta Data Report")
        await self.bot.send_message(channel, embed=embed)

    async def on_member_remove(self, member):
        channel = discord.utils.get(member.server.channels, name='welcome')
        await self.bot.send_message(channel, "**Left The Server** | *{}*".format(member))
        await self.bot.send_message(channel, "Goodbye, {}. Seeing as you left the server, for whichever reason, we're sorry to see you go. Looking towards the future, we'll keep an eye out for you..".format(member.mention))

        channel = discord.utils.get(member.server.channels, name='server-logs')
        embed = discord.Embed(title='**User Left**', description='Detected User Leave', color=0xfc4156)
        embed.add_field(name="**Name**", value=member.mention, inline=False)
        embed.add_field(name="**Message**", value="User has left the server", inline=False)
        embed.set_author(name="Data Report", icon_url="https://cdn.discordapp.com/app-icons/481923206848970803/394817ba790d2fbb9c36715a7ec00576.png")
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text="Delta Data Report")
        await self.bot.send_message(channel, embed=embed)

    async def on_message_delete(self, message):
        channel = discord.utils.get(message.server.channels, name='server-logs')
        embed = discord.Embed(title='**Deleted Message**', description='Pulling Deleted Message', color=0xfc4156)
        author = message.author
        content = message.content
        embed.add_field(name="**Name**", value=author, inline=False)
        embed.add_field(name="**Message**", value=content, inline=False)
        embed.set_author(name="Data Report", icon_url="https://cdn.discordapp.com/app-icons/481923206848970803/394817ba790d2fbb9c36715a7ec00576.png")
        embed.set_thumbnail(url=message.author.avatar_url)
        embed.set_footer(text="Delta Data Report")
        await self.bot.send_message(channel, embed=embed)

    async def on_message_edit(before, after):
        channel = discord.utils.get(before.server.channels, name='server-logs')
        embed = discord.Embed(title='**Message Edited**', description='Pulling Edited Message', color=0xfc4156)
        embed.set_author(name="Data Report", icon_url="https://cdn.discordapp.com/app-icons/481923206848970803/394817ba790d2fbb9c36715a7ec00576.png")
        embed.add_field(name="**Name**", value=before.author, inline=False)
        embed.add_field(name="``Before:``", value=before.content, inline=False)
        embed.add_field(name="``After:``", value=after.content, inline=False)
        embed.set_footer(text="Delta Data Report")
        embed.set_thumbnail(url=before.author.avatar_url)
        await self.bot.send_message(channel, embed=embed)

    async def on_member_update(self, before, after):
        channel = discord.utils.get(before.server.channels, name='server-logs')
        embed = discord.Embed(title='**Status Change**', description="Users' Status Changed", color=0xfc4156)
        embed.set_author(name="Status Change", icon_url="https://cdn.discordapp.com/app-icons/481923206848970803/394817ba790d2fbb9c36715a7ec00576.png")
        embed.add_field(name="**Name**", value=before.mention, inline=False)
        embed.add_field(name="``Before Status:``", value=before.status, inline=True)
        embed.add_field(name="``After Status:``", value=after.status, inline=True)
        embed.add_field(name="``Before Game:``", value=before.game, inline=True)
        embed.add_field(name="``After Game:``", value=after.game, inline=True)
        embed.add_field(name="``Before Name:``", value=before.nick, inline=True)
        embed.add_field(name="``After Name:``", value=after.nick, inline=True)
        embed.add_field(name="``Before Role:``", value=before.top_role, inline=True)
        embed.add_field(name="``After Role:``", value=after.top_role, inline=True)
        embed.set_footer(text="Delta Data Report")
        embed.set_thumbnail(url=before.avatar_url)
        await self.bot.send_message(channel, embed=embed)

    async def on_member_ban(self, member):
        server = message.server
        channel = discord.utils.get(member.server.channels, name='server-logs')
        embed = discord.Embed(title='**User Banned**', description="Users' Ban Changed", color=0xfc4156)
        embed.set_author(name="Ban Change", icon_url="https://cdn.discordapp.com/app-icons/481923206848970803/394817ba790d2fbb9c36715a7ec00576.png")
        embed.add_field(name="**User Banned**", value=member.mention, inline=False)
        await self.bot.send_message(channel, embed=embed)

    async def on_member_unban(self, server, user):
        server = message.server
        channel = discord.utils.get(server.channels, name='server-logs')
        embed = discord.Embed(title='**User Unbanned**', description="Users' Ban Changed", color=0xfc4156)
        embed.set_author(name="Ban Change", icon_url="https://cdn.discordapp.com/app-icons/481923206848970803/394817ba790d2fbb9c36715a7ec00576.png")
        embed.add_field(name="**Action**", value="User was unbanned, {}".format(user), inline=False)
        await self.bot.send_message(channel, embed=embed)



    @commands.command(pass_context=True)
    async def identify(self, ctx, user: discord.Member):
        embed = discord.Embed(title="{}'s Info".format(user.name), description="Pulling ` {}`'s  File From Database".format(user.name), color=0xfc4156)
        embed.set_footer(text="Delta Data Report")
        embed.set_author(name="Database File", icon_url="https://cdn.discordapp.com/app-icons/481923206848970803/394817ba790d2fbb9c36715a7ec00576.png")
        embed.add_field(name="User Name", value="`Name:` | {}".format(user.name), inline=True)
        embed.add_field(name="User ID", value="`ID:` | {}".format(user.id), inline=True)
        embed.add_field(name="User Status", value="`Status:` | {}".format(user.status), inline=True)
        embed.add_field(name="User Role", value="`Highest:` | {}".format(user.top_role), inline=True)
        embed.add_field(name="Date Joined", value="`Joined:` | {}".format(user.joined_at), inline=True)
        embed.set_thumbnail(url=user.avatar_url)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def serverinfo(self, ctx):
        embed = discord.Embed(title="{}'s Information".format(ctx.message.server.name), description="Polling known information. | Subject: `{}`".format(ctx.message.server.name), color=0xfc4156)
        embed.set_author(name="Location File", icon_url="https://cdn.discordapp.com/app-icons/481923206848970803/394817ba790d2fbb9c36715a7ec00576.png")
        embed.add_field(name="Server Name", value="`Name:` | {}".format(ctx.message.server.name))
        embed.add_field(name="Server ID", value="`ID:` | {}".format(ctx.message.server.id), inline=True)
        embed.add_field(name="Server Roles", value=len(ctx.message.server.roles), inline=True)
        embed.add_field(name="Server Members", value=len(ctx.message.server.members))
        embed.set_thumbnail(url=ctx.message.server.icon_url)
        embed.set_footer(text="Delta Data Report")
        await self.bot.say(embed=embed)

def setup(bot):
    bot.add_cog(Log(bot))
