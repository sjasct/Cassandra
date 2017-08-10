import discord
from discord.ext import commands
import random
import asyncio
import Dependencies

class Dev():
    def __init__(self, bot):
        self.bot = bot

        # addsuggestion command
    @commands.group(aliases=["addsuggest"], pass_context=True)
    @commands.has_any_role("Devs", "Developers")
    async def addsuggestion(self, ctx, *, suggestion : str=None):
        '''Add features people hope to see on this bot!'''
        if suggestion is None:
            self.bot.say('Please input a suggestion.')
        else:
            await self.bot.say('Feedback Taken.')
            suggestion_embed = discord.Embed(title="Suggestion", description= 'Suggestion: *{0}*'.format(suggestion), color=discord.Color.purple())
            suggestion_embed.set_footer(text='Suggestion for Cassandra')
            await self.bot.send_message(discord.utils.get(ctx.message.server.channels, id=dependencies.suggestions_channel), embed=suggestion_embed)

def log(message):
    print(datetime.now(), message)

def setup(bot):
    bot.add_cog(Dev(bot))