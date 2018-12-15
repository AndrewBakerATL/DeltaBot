import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import chalk
from itertools import cycle
import youtube_dl
import json
import os

# Prefix

bot = commands.Bot(command_prefix='!')
extensions = ['moderation', 'starter', 'verify', 'clean', 'log']
bot.remove_command('help')

if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(extension, error))

players = {}
queues = {}

# Status Cycle

status = ['Managing The Server', 'Scanning Server Logs', 'Compiling Anomalies']

async def change_status():
    await bot.wait_until_ready()
    msgs = cycle(status)

    while not bot.is_closed:
        current_status = next(msgs)
        await bot.change_presence(game=discord.Game(name=current_status))
        await asyncio.sleep(30)

bot.loop.create_task(change_status())

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

# Basic Commands

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
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(color = 0xfc4156)
    embed.set_author(name='Requesting Help Report', icon_url="https://cdn.discordapp.com/app-icons/481923206848970803/394817ba790d2fbb9c36715a7ec00576.png")
    embed.add_field(name='Introduction', value="For any major problems, please seek out the server staff. For any problems relating to the functioning of the bot, alert the creator of the problem and wait for a fix. The help menu consists of all commands relating to the server. Some of these commands may only be ran by a user with the appropriate rank. To see the commands, please check below.", inline=False)
    embed.add_field(name='__**Getting Started**__', value="Installing the bot.", inline=False)
    embed.add_field(name='Install Delta', value="!intro | Installs the bot's dependencies.", inline=False)
    embed.add_field(name='__**Moderation Commands**__', value="Use these to moderate the server", inline=False)
    embed.add_field(name='Ban User', value="!ban | Bans a user from the server, indefinitely.", inline=False)
    embed.add_field(name='Kick User', value="!kick | Kicks a user from the server.", inline=False)
    embed.add_field(name='Clear Messages', value="!clear (Number) | Clears a number of messages from the server.", inline=False)
    embed.add_field(name='Purge Messages', value="!purge (Number) | Purges a number of messages from the server.", inline=False)
    embed.add_field(name='Hammer User', value="!hammer | An advanced form of a ban deleting messages.", inline=False)
    embed.add_field(name='__**Information Commands**__', value="Use these to get information.", inline=False)
    embed.add_field(name='Identify User', value="!Identify (name) | Pulls a user's file from the server.", inline=False)
    embed.add_field(name='Server Information', value="!serverinfo | Shows information about the active server.", inline=False)
    embed.add_field(name='__**Music Commands**__', value="Music Playback Commands.", inline=False)
    embed.add_field(name='Play Song', value="!play (Terms) | Plays a song by the artist specified, or grabs the specific song.", inline=False)
    embed.add_field(name='Pause Song', value="!pause | Pauses the active playback.", inline=False)
    embed.add_field(name='Queue Song', value="!queue (Terms) | Adds a song into the queue.", inline=False)
    embed.add_field(name='Stop Song', value="!stop | Stops current playback.", inline=False)
    embed.add_field(name='Skip Song', value="!skip | Skips current playback.", inline=False)
    embed.add_field(name='Join Channel', value="!join | Bot joins your voice channel.", inline=False)
    embed.add_field(name='Leave Channel', value="!leave | Bot leaves your voice channel.", inline=False)
    embed.add_field(name='__**Verify Commands**__', value="Terms & Conditions.", inline=False)
    embed.add_field(name='Accept Terms', value="!accept | Accepts Terms of the Server and grants entry.", inline=False)
    embed.add_field(name='__**Miscellaneous Commands**__', value="Added on commands.", inline=False)
    embed.add_field(name='Echo Command', value="!echo (text) | The bot echoes the text given to it.", inline=False)
    embed.add_field(name='Ping Command', value="!ping | It replies back with pong.", inline=False)
    await bot.send_message(author, embed=embed)

# Music Commands

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

# Tasks

bot.loop.create_task(change_status())

# Tokens

Token = "NDgxOTIzMjA2ODQ4OTcwODAz.DrpPng.oKeZXc2hieFe4R7_ETK9Q_tewu0"
bot.run(Token)
