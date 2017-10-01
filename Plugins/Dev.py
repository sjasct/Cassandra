import discord
from discord.ext import commands
import random
import asyncio
import Dependencies
from Plugins import Bot as botPlg

def log(message):
    botPlg.log(message)

class Dev():

    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['addsuggest'])
    @commands.has_any_role('Devs', 'Developers')
    async def addsuggestion(self, ctx, *, suggestion: str=None):
        'Add features people hope to see on this bot!'
        if (suggestion is None):
            await ctx.send('Please input a suggestion.')
        else:
            await ctx.send('Feedback Taken.')
            suggestion_embed = discord.Embed(title='Suggestion', description='Suggestion: *{0}*'.format(suggestion), color=discord.Color.purple())
            suggestion_embed.set_footer(text='Suggestion for Cassandra')
            await discord.utils.get(ctx.guild.channels, name=Dependencies.logChannel).send(embed=suggestion_embed)

def setup(bot):
    bot.add_cog(Dev(bot))
    