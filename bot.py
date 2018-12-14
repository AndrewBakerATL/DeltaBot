import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import chalk
from itertools import cycle
import youtube_dl
import json
import os

#Prefix

bot = commands.Bot(command_prefix='!')

players = {}
queues = {}

status = ['Managing The Server', 'Scanning Server Logs', 'Compiling Anomalies']
bot.remove_command('help')

async def change_status():
    await bot.wait_until_ready()
    msgs = cycle(status)

    while not bot.is_closed:
        current_status = next(msgs)
        await bot.change_presence(game=discord.Game(name=current_status))
        await asyncio.sleep(30)

#On Ready Status

def check_queue(id):
    if queues[id] != []:
        player = queues[id].pop(0)
        players[id] = player
        player.start()

@bot.event
async def on_ready():
    print ("Bot Online")
    print ("Bot Name: " + bot.user.name)
    print ("Bot ID: " + bot.user.id)
    print ("Bot running under user: {}".format(bot.user))
    #await bot.change_presence(game=discord.Game(name='Managing The Server'))

#Commands

@bot.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(color = 0xfc4156)
    embed.set_author(name='Requesting Help Report', icon_url="https://cdn.discordapp.com/app-icons/481923206848970803/394817ba790d2fbb9c36715a7ec00576.png")
    embed.add_field(name='Introduction', value="For any major problems, please seek out the server staff. For any problems relating to the functioning of the bot, alert the creator of the problem and wait for a fix. The help menu consists of all commands relating to the server. Some of these commands may only be ran by a user with the appropriate rank. To see the commands, please check below.", inline=False)
    embed.add_field(name='Moderation Commands ──────────────────────────────────────', value="Use these to moderate the server", inline=False)
    embed.add_field(name='Ban User', value="!ban | Bans a user from the server, indefinitely.", inline=False)
    embed.add_field(name='Kick User', value="!kick | Kicks a user from the server.", inline=False)
    embed.add_field(name='Clear Messages', value="!clear (Number) | Clears a number of messages from the server.", inline=False)
    embed.add_field(name='Information Commands ──────────────────────────────────────', value="Use these to get information.", inline=False)
    embed.add_field(name='Identify User', value="!Identify (name) | Pulls a user's file from the server.", inline=False)
    embed.add_field(name='Server Information', value="!serverinfo | Shows information about the active server.", inline=False)
    embed.add_field(name='Miscellaneous Commands ──────────────────────────────────────', value="Added on commands.", inline=False)
    embed.add_field(name='Echo Command', value="!echo (text) | The bot echoes the text given to it.", inline=False)
    await bot.send_message(author, embed=embed)

@bot.command(pass_context=True)
async def ping(ctx):
    await bot.say(":ping_pong:  Pong!!")
    print ("user has pinged")

@bot.command()
async def echo(*args):
    output = ''
    for word in args:
        output += word
        output += ' '
    await bot.say(output)

@bot.command(pass_context=True)
async def clear(ctx, amount=5):
    channel = ctx.message.channel
    messages = []
    async for message in bot.logs_from(channel, limit=int(amount)):
        messages.append(message)
    await bot.delete_messages(messages)
    await bot.say('Messages Deleted')

@bot.command(pass_context=True)
async def purge(ctx, amount=5):
    channel = ctx.message.channel
    deleted = await bot.purge_from(channel, limit=int(amount))
    await bot.send_message(channel, 'Deleted {} message(s)'.format(len(deleted)))

@bot.command(pass_context=True)
@commands.has_role("Admin")
async def kick(ctx, user: discord.Member):
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
    await bot.send_message(channel, embed=embed)
    await bot.send_message(server_log, embed=embed)
    await bot.kick(user)

@bot.command(pass_context=True)
@commands.has_role("Admin")
async def ban(ctx, user: discord.Member):
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
    await bot.send_message(channel, embed=embed)
    await bot.send_message(server_log, embed=embed)
    await bot.ban(user)

@bot.command(pass_context=True)
@commands.has_role("Admin")
async def hammer(ctx, user: discord.Member):
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
    await bot.send_message(channel, embed=embed)
    await bot.send_message(server_log, embed=embed)
    await bot.ban(user, delete_message_days=7)


@bot.command(pass_context=True)
async def identify(ctx, user: discord.Member):
    embed = discord.Embed(title="{}'s Info".format(user.name), description="Pulling ` {}`'s  File From Database".format(user.name), color=0xfc4156)
    embed.set_footer(text="Delta Data Report")
    embed.set_author(name="Database File", icon_url="https://cdn.discordapp.com/app-icons/481923206848970803/394817ba790d2fbb9c36715a7ec00576.png")
    embed.add_field(name="User Name", value="`Name:` | {}".format(user.name), inline=True)
    embed.add_field(name="User ID", value="`ID:` | {}".format(user.id), inline=True)
    embed.add_field(name="User Status", value="`Status:` | {}".format(user.status), inline=True)
    embed.add_field(name="User Role", value="`Highest:` | {}".format(user.top_role), inline=True)
    embed.add_field(name="Date Joined", value="`Joined:` | {}".format(user.joined_at), inline=True)
    embed.set_thumbnail(url=user.avatar_url)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def serverinfo(ctx):
    embed = discord.Embed(title="{}'s Information".format(ctx.message.server.name), description="Polling known information. | Subject: `{}`".format(ctx.message.server.name), color=0xfc4156)
    embed.set_author(name="Location File", icon_url="https://cdn.discordapp.com/app-icons/481923206848970803/394817ba790d2fbb9c36715a7ec00576.png")
    embed.add_field(name="Server Name", value="`Name:` | {}".format(ctx.message.server.name))
    embed.add_field(name="Server ID", value="`ID:` | {}".format(ctx.message.server.id), inline=True)
    embed.add_field(name="Server Roles", value=len(ctx.message.server.roles), inline=True)
    embed.add_field(name="Server Members", value=len(ctx.message.server.members))
    embed.set_thumbnail(url=ctx.message.server.icon_url)
    embed.set_footer(text="Delta Data Report")
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await bot.join_voice_channel(channel)

@bot.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = bot.voice_client_in(server)
    await voice_client.disconnect()

@bot.command(pass_context=True)
async def play(ctx, *, url):
    server = ctx.message.server
    voice_client = bot.voice_client_in(server)
    player = await voice_client.create_ytdl_player(f"ytsearch:{url}", after=lambda: check_queue(server.id))
    players[server.id] = player
    player.start()
    await bot.say("**Playing Song** -> `` {} ``".format(url))

@bot.command(pass_context=True)
async def pause(ctx):
    id = ctx.message.server.id
    players[id].pause()
    await bot.say("**Pausing Playback**")

@bot.command(pass_context=True)
async def stop(ctx):
    id = ctx.message.server.id
    players[id].stop()
    await bot.say("**Stopping Playback**")

@bot.command(pass_context=True)
async def resume(ctx):
    id = ctx.message.server.id
    players[id].resume()
    await bot.say("**Resuming Playback**")

@bot.command(pass_context=True)
async def queue(ctx, *, url):
    server = ctx.message.server
    voice_client = bot.voice_client_in(server)
    player = await voice_client.create_ytdl_player(f"ytsearch:{url}", after=lambda: check_queue(server.id))

    if server.id in queues:
        queues[server.id].append(player)
    else:
        queues[server.id] = [player]
    await bot.say("**Added To Queue** -> `` {} ``".format(url))

@bot.command(pass_context=True)
async def skip(ctx):
    server = ctx.message.server
    voice_client = bot.voice_client_in(server)
    id = ctx.message.server.id

    if server.id in queues:
        players[id].stop()
        await bot.say("**Skipping Song**")
    else:
        await bot.say("**Queue is Empty**")

#Events

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.server.channels, name='welcome')
    role = discord.utils.get(member.server.roles, name='Newcomer')
    await bot.add_roles(member, role)
    await bot.send_message(channel, "**Welcome To The Server** | *{}*".format(member))
    await bot.send_message(channel, "Welcome to the server, {}. We hope you enjoy your stay. Staff is located to your right if you have any problems. Be aware that the server uses a #terms-conditions and take notice of it. If you have any problems, let us know.".format(member.mention))

    channel = discord.utils.get(member.server.channels, name='server-logs')
    embed = discord.Embed(title='**User Joined**', description='Detected User Join', color=0xfc4156)
    embed.add_field(name="**Name**", value=member, inline=False)
    embed.add_field(name="**Message**", value="User joined the server", inline=False)
    embed.add_field(name="**Date Joined**", value="`Joined:` | {}".format(member.joined_at), inline=True)
    embed.set_author(name="Data Report", icon_url="https://cdn.discordapp.com/app-icons/481923206848970803/394817ba790d2fbb9c36715a7ec00576.png")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text="Delta Data Report")
    await bot.send_message(channel, embed=embed)

@bot.event
async def on_member_remove(member):
    channel = discord.utils.get(member.server.channels, name='welcome')
    await bot.send_message(channel, "**Left The Server** | *{}*".format(member))
    await bot.send_message(channel, "Goodbye, {}. Seeing as you left the server, for whichever reason, we're sorry to see you go. Looking towards the future, we'll keep an eye out for you..".format(member.mention))

    channel = discord.utils.get(member.server.channels, name='server-logs')
    embed = discord.Embed(title='**User Left**', description='Detected User Leave', color=0xfc4156)
    embed.add_field(name="**Name**", value=member.mention, inline=False)
    embed.add_field(name="**Message**", value="User has left the server", inline=False)
    embed.set_author(name="Data Report", icon_url="https://cdn.discordapp.com/app-icons/481923206848970803/394817ba790d2fbb9c36715a7ec00576.png")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text="Delta Data Report")
    await bot.send_message(channel, embed=embed)

@bot.event
async def on_message_delete(message):
    channel = discord.utils.get(message.server.channels, name='server-logs')
    embed = discord.Embed(title='**Deleted Message**', description='Pulling Deleted Message', color=0xfc4156)
    author = message.author
    content = message.content
    embed.add_field(name="**Name**", value=author, inline=False)
    embed.add_field(name="**Message**", value=content, inline=False)
    embed.set_author(name="Data Report", icon_url="https://cdn.discordapp.com/app-icons/481923206848970803/394817ba790d2fbb9c36715a7ec00576.png")
    embed.set_thumbnail(url=message.author.avatar_url)
    embed.set_footer(text="Delta Data Report")
    await bot.send_message(channel, embed=embed)

@bot.event
async def on_message_edit(before, after):
    channel = discord.utils.get(before.server.channels, name='server-logs')
    embed = discord.Embed(title='**Message Edited**', description='Pulling Edited Message', color=0xfc4156)
    embed.set_author(name="Data Report", icon_url="https://cdn.discordapp.com/app-icons/481923206848970803/394817ba790d2fbb9c36715a7ec00576.png")
    embed.add_field(name="**Name**", value=before.author, inline=False)
    embed.add_field(name="``Before:``", value=before.content, inline=False)
    embed.add_field(name="``After:``", value=after.content, inline=False)
    embed.set_footer(text="Delta Data Report")
    embed.set_thumbnail(url=before.author.avatar_url)
    await bot.send_message(channel, embed=embed)

@bot.event
async def on_member_update(before, after):
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
    await bot.send_message(channel, embed=embed)

@bot.event
async def on_member_ban(member):
    server = message.server
    channel = discord.utils.get(member.server.channels, name='server-logs')
    embed = discord.Embed(title='**User Banned**', description="Users' Ban Changed", color=0xfc4156)
    embed.set_author(name="Ban Change", icon_url="https://cdn.discordapp.com/app-icons/481923206848970803/394817ba790d2fbb9c36715a7ec00576.png")
    embed.add_field(name="**User Banned**", value=member.mention, inline=False)
    await bot.send_message(channel, embed=embed)

@bot.event
async def on_member_unban(server, user):
    server = message.server
    channel = discord.utils.get(server.channels, name='server-logs')
    embed = discord.Embed(title='**User Unbanned**', description="Users' Ban Changed", color=0xfc4156)
    embed.set_author(name="Ban Change", icon_url="https://cdn.discordapp.com/app-icons/481923206848970803/394817ba790d2fbb9c36715a7ec00576.png")
    embed.add_field(name="**Action**", value="User was unbanned, {}".format(user), inline=False)
    await bot.send_message(channel, embed=embed)

#Tasks

bot.loop.create_task(change_status())

#Tokens

Token = "NDgxOTIzMjA2ODQ4OTcwODAz.DrpPng.oKeZXc2hieFe4R7_ETK9Q_tewu0"
bot.run(Token)
