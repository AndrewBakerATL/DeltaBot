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

    async def on_message_edit(self, before, after):
        channel = discord.utils.get(before.server.channels, name='server-logs')
        author = before.author.mention
        embed = discord.Embed(title='**Message Edited** | :pencil:', description="Pulling {}'s Edited Message".format(author), color=0xfc4156)
        embed.set_author(name="Data Report", icon_url="https://cdn.discordapp.com/app-icons/481923206848970803/394817ba790d2fbb9c36715a7ec00576.png")
        embed.add_field(name="**Before:**", value=before.content, inline=False)
        embed.add_field(name="**After:**", value=after.content, inline=False)
        embed.set_footer(text="Delta Data Report")
        embed.set_thumbnail(url=before.author.avatar_url)
        await self.bot.send_message(channel, embed=embed)

    async def on_member_update(self, before, after):
        channel = discord.utils.get(before.server.channels, name='server-logs')
        if before.status != after.status:
            user = before.mention
            embed = discord.Embed(title='**Status Change** | :eyes: ', description="{}'s status changed".format(user), color=0xfc4156)
            embed.add_field(name="**Changed To**", value="Member's status changed from **{}** to **{}**".format(before.status, after.status))
            embed.set_thumbnail(url=before.avatar_url)
            embed.set_author(name="Logging Change", icon_url="https://cdn.discordapp.com/app-icons/481923206848970803/394817ba790d2fbb9c36715a7ec00576.png")
            embed.set_footer(text="Delta Data Report")
            await self.bot.send_message(channel, embed=embed)
        if before.game != after.game:
            user = before.mention
            embed = discord.Embed(title='**Game Changed** | :joystick: ', description="{}'s playing a new game".format(user), color=0xfc4156)
            embed.add_field(name="**Changed To**", value="Member's game changed from **{}** to **{}**".format(before.game, after.game))
            embed.set_thumbnail(url=before.avatar_url)
            embed.set_author(name="Logging Change", icon_url="https://cdn.discordapp.com/app-icons/481923206848970803/394817ba790d2fbb9c36715a7ec00576.png")
            embed.set_footer(text="Delta Data Report")
            await self.bot.send_message(channel, embed=embed)
        if before.nick != after.nick:
            user = before.mention
            embed = discord.Embed(title='**Name Changed** | :pencil: ', description="{}'s name changed".format(user), color=0xfc4156)
            embed.add_field(name="**Username**", value=before.name)
            embed.add_field(name="**Changed To**", value="Member's name changed from **{}** to **{}**".format(before.nick, after.nick))
            embed.set_thumbnail(url=before.avatar_url)
            embed.set_author(name="Logging Change", icon_url="https://cdn.discordapp.com/app-icons/481923206848970803/394817ba790d2fbb9c36715a7ec00576.png")
            embed.set_footer(text="Delta Data Report")
            await self.bot.send_message(channel, embed=embed)
        if before.top_role != after.top_role:
            roles = after.roles
            user = before.mention
            embed = discord.Embed(title='**Role Changed** | :briefcase: ', description="{}'s role changed".format(user), color=0xfc4156)
            embed.add_field(name="**Username**", value=before.name)
            embed.add_field(name="**Changed To**", value="Member's role changed from **{}** to **{}**".format(before.top_role, after.top_role))
            embed.add_field(name="**Held Roles**", value=", ".join([role.name for role in roles]))
            embed.set_thumbnail(url=before.avatar_url)
            embed.set_author(name="Logging Change", icon_url="https://cdn.discordapp.com/app-icons/481923206848970803/394817ba790d2fbb9c36715a7ec00576.png")
            embed.set_footer(text="Delta Data Report")
            await self.bot.send_message(channel, embed=embed)
        if before.avatar_url != after.avatar_url:
            user = before.mention
            embed = discord.Embed(title='**Avatar Changed** | :eyes: ', description="{}'s changed their avatar".format(user), color=0xfc4156)
            embed.add_field(name="**Username**", value=before.name)
            embed.set_thumbnail(url=before.avatar_url)
            embed.set_author(name="Logging Change", icon_url="https://cdn.discordapp.com/app-icons/481923206848970803/394817ba790d2fbb9c36715a7ec00576.png")
            embed.set_footer(text="Delta Data Report")
            await self.bot.send_message(channel, embed=embed)
            embed.set_thumbnail(url=after.avatar_url)
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
