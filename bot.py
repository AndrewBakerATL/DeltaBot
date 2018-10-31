#initial Python-based bot

import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import chalk

Token = "NDgxOTIzMjA2ODQ4OTcwODAz.DrpPng.oKeZXc2hieFe4R7_ETK9Q_tewu0"

#Prefix

bot = commands.Bot(command_prefix='!')
client = commands.Bot(command_prefix='!')
#client = commands.Bot(command_prefix='!')
#On Ready Status

@bot.event
async def on_ready():
    print ("All ready to go")
    print ("I am running on " + bot.user.name)
    print ("With the ID: " + bot.user.id)

#Commands

@bot.command(pass_context=True)
async def ping(ctx):
    await bot.say(":ping_pong:  Pong!!")
    print ("user has pinged")

@bot.command(pass_context=True)
async def info(ctx, user: discord.Member):
    embed = discord.Embed(title="{}'s Info".format(user.name), description="Here's their report.", color=0x00ff00)
    await bot.say("The users name is: {}".format(user.name))
    await bot.say("The users ID is {}".format(user.id))
    await bot.say("the users status is{}".format(user.status))
    await bot.say("The users highest role is: {}".format(user.top_role))
    await bot.say("the user joined at: {}".format(user.joined_at))

@bot.command(pass_context=True)
@commands.has_role("Administrator")
async def kick(ctx, user: discord.Member):
    await bot.say(":boot: Cya, {}. Ya loser!".format(user.name))
    await bot.kick(user)

@bot.command(pass_context=True)
async def identify(ctx, user: discord.Member):
    embed = discord.Embed(title="{}'s Info".format(user.name), description="Pulling ` {}`'s  File From Database".format(user.name), color=0xffffff)
    embed.set_footer(text="Testing Bot Data Report")
    embed.set_author(name="Database File", icon_url="https://willjackward.files.wordpress.com/2013/02/screen-shot-2013-02-11-at-10-40-04.png")
    embed.add_field(name="User Name", value="`Name:` | {}".format(user.name), inline=True)
    embed.add_field(name="User ID", value="`ID:` | {}".format(user.id), inline=True)
    embed.add_field(name="User Status", value="`Status:` | {}".format(user.status), inline=True)
    embed.add_field(name="User Role", value="`Highest:` | {}".format(user.top_role), inline=True)
    embed.add_field(name="Date Joined", value="`Joined:` | {}".format(user.joined_at), inline=True)
    embed.set_thumbnail(url=user.avatar_url)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def serverinfo(ctx):
    embed = discord.Embed(title="{}'s Information".format(ctx.message.server.name), desription="Polling known information. | Subject: `{}`".format(ctx.message.server.name), color=0xffffff)
    embed.set_author(name="Location File", icon_url="https://willjackward.files.wordpress.com/2013/02/screen-shot-2013-02-11-at-10-40-04.png")
    embed.add_field(name="Server Name", value="`Name:` | {}".format(ctx.message.server.name))
    embed.add_field(name="Server ID", value="`ID:` | {}".format(ctx.message.server.id), inline=True)
    embed.add_field(name="Server Roles", value=len(ctx.message.server.roles), inline=True)
    embed.add_field(name="Server Members", value=len(ctx.message.server.members))
    embed.set_thumbnail(url=ctx.message.server.icon_url)
    embed.set_footer(text="Testing Bot Data Report")
    await bot.say(embed=embed)

#Events

@client.event
async def on_message(message):
    author = message.author
    content = message.content
    print ('{}: {}'.format(author, content))

@client.event
async def on_message_delete(message):
    author = message.author
    content = message.content
    channel = message.channel
    await client.send_message(channel,'{}: {}'.format(author, content))

#Token

bot.run(Token)
#bot.run("NDgxOTIzMjA2ODQ4OTcwODAz.DrpPng.oKeZXc2hieFe4R7_ETK9Q_tewu0")
