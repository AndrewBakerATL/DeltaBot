import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import chalk
from itertools import cycle

Token = "NDgxOTIzMjA2ODQ4OTcwODAz.DrpPng.oKeZXc2hieFe4R7_ETK9Q_tewu0"

#Prefix

bot = commands.Bot(command_prefix='!')
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

@bot.event
async def on_ready():
    print ("Bot Online")
    print ("Bot Name: " + bot.user.name)
    print ("Bot ID: " + bot.user.id)
    #await bot.change_presence(game=discord.Game(name='Managing The Server'))

#Commands

@bot.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(color = 0xffffff)
    embed.set_author(name='Requesting Help Report', icon_url="https://willjackward.files.wordpress.com/2013/02/screen-shot-2013-02-11-at-10-40-04.png")
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
@commands.has_role("Admin")
async def kick(ctx, user: discord.Member):
    embed = discord.Embed(title="Kicking User", description="Taking action on `{}`'s  File From `{} Database`".format(user.name, ctx.message.server.name), color=0xffffff)
    embed.set_footer(text="Testing Bot Discipline Report")
    embed.set_author(name="Discipline Report", icon_url="https://willjackward.files.wordpress.com/2013/02/screen-shot-2013-02-11-at-10-40-04.png")
    embed.add_field(name="User Name", value="`Name:` | {}".format(user.name), inline=True)
    embed.add_field(name="User ID", value="`ID:` | {}".format(user.id), inline=True)
    embed.add_field(name="User Role", value="`Highest:` | {} ".format(user.top_role), inline=True)
    embed.add_field(name="Date Joined", value="`Joined:` | {}".format(user.joined_at), inline=True)
    embed.add_field(name="Action Taken", value="`Discipline:` | **Kicked {} **".format(user.name), inline=True)
    embed.set_thumbnail(url=user.avatar_url)
    await bot.say(embed=embed)
    await bot.kick(user)

@bot.command(pass_context=True)
@commands.has_role("Admin")
async def ban(ctx, user: discord.Member):
    embed = discord.Embed(title="Banning User", description="Taking action on `{}`'s  File From `{} Database`".format(user.name, ctx.message.server.name), color=0xffffff)
    embed.set_footer(text="Testing Bot Discipline Report")
    embed.set_author(name="Discipline Report", icon_url="https://willjackward.files.wordpress.com/2013/02/screen-shot-2013-02-11-at-10-40-04.png")
    embed.add_field(name="User Name", value="`Name:` | {}".format(user.name), inline=True)
    embed.add_field(name="User ID", value="`ID:` | {}".format(user.id), inline=True)
    embed.add_field(name="User Role", value="`Highest:` | {} ".format(user.top_role), inline=True)
    embed.add_field(name="Date Joined", value="`Joined:` | {}".format(user.joined_at), inline=True)
    embed.add_field(name="Action Taken", value="`Discipline:` | **Banned {} **".format(user.name), inline=True)
    embed.set_thumbnail(url=user.avatar_url)
    await bot.say(embed=embed)
    await bot.ban(user)

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
    embed = discord.Embed(title="{}'s Information".format(ctx.message.server.name), description="Polling known information. | Subject: `{}`".format(ctx.message.server.name), color=0xffffff)
    embed.set_author(name="Location File", icon_url="https://willjackward.files.wordpress.com/2013/02/screen-shot-2013-02-11-at-10-40-04.png")
    embed.add_field(name="Server Name", value="`Name:` | {}".format(ctx.message.server.name))
    embed.add_field(name="Server ID", value="`ID:` | {}".format(ctx.message.server.id), inline=True)
    embed.add_field(name="Server Roles", value=len(ctx.message.server.roles), inline=True)
    embed.add_field(name="Server Members", value=len(ctx.message.server.members))
    embed.set_thumbnail(url=ctx.message.server.icon_url)
    embed.set_footer(text="Testing Bot Data Report")
    await bot.say(embed=embed)

#Events

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles, name='Admin')
    await bot.add_roles(member, role)

bot.loop.create_task(change_status())

#Tokens
bot.run(Token)
