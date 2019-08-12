import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import chalk
from itertools import cycle
import youtube_dl
import json
import os

os.chdir(r'./system/')

class Leveling:
    def __init__(self, bot):
        self.bot = bot

    async def on_member_join(self, member):
        with open('experience.json', 'r') as f:
            experience = json.load(f)
        await update_data(experience, member)
        with open('experience.json', 'w') as f:
            json.dump(experience, f)


    async def on_message(self, message):
        with open('experience.json', 'r') as f:
            experience = json.load(f)
        await update_data(experience, message.author)
        await add_experience(experience, message.author, 5)
        await level_up(experience, message.author, message.channel)
        with open('experience.json', 'w') as f:
            json.dump(experience, f)

    async def update_data(self, experience, user):
        if not user.id in experience:
            experience[user.id] = {}
            experience[user.id]['experience'] = 0
            experience[user.id]['level'] = 0

    async def add_experience(self, experience, user, exp):
        experience[user.id]['experience'] += exp

    async def level_up(self, experience, user, channel):
        xp = experience[user.id]['experience']
        lvl_start = experience[users.id]['level']
        lvl_end = int(xp ** (1/4))

        if lvl_start < lvl_end:
            await self.bot.send_message(channel, '{} has leveled up to {}'.format(user.mention, lvl_end))
            experience[user.id]['level'] = lvl_end

def setup(bot):
    bot.add_cog(Leveling(bot))
