import discord
from discord.ext import commands
import random
import asyncio
import Dependencies

class Admin():
    def __init__(self, bot):
        self.bot = bot   
        # strike command
    @commands.has_any_role("Moderators™", "TomCord Mod")
    @commands.command(pass_context=True)
    async def strike(self, ctx, member : str=None, *, reason : str=None):
        '''Gives a strike to a specified person.'''
        if member is None:
            await self.bot.say('Please input a user.')
        elif member is not None and reason is None:
            await self.bot.say('Please input a reason')
        elif member is not None and reason is not None:
            member = ctx.message.mentions[0]
            strike_embed = discord.Embed(title="Strike", description= 'User: **{0}** \nReason: {1}'.format(member, reason), color=discord.Color.red())
            strike_embed.set_footer(text='Strike')
            await self.bot.send_message(discord.utils.get(ctx.message.server.channels, name="strikes"), '<&332973960318943233>', embed=strike_embed)
            strike_embed = discord.Embed(title="Strike", description= 'You have been given a strike on the {0} server. \nReason: {1}'.format(ctx.message.server, reason), color=discord.Color.red())
            strike_embed.set_footer(text='Strike')
            await self.bot.send_message(member, embed=strike_embed)
            logMsg = "{0} has been striked on the {1} server. Reason: {2}".format(member, ctx.message.server, reason)
            log(logMsg)

    @commands.has_permissions(kick_members=True)
    @commands.command(pass_context=True)
    async def kick(self, ctx, member : str=None, *, reason : str=None):
        '''Kicks a specified person.'''
        if member is None:
            await self.bot.say('Please input a user.')
        elif member is not None and reason is None:
            await self.bot.say('Please input a reason')
        elif member is not None and reason is not None:
            member = ctx.message.mentions[0]
            await self.bot.kick(member)
            await self.bot.say('Kicked {0}. Reason: {1}'.format(member, reason))
            log('{0} has been kicked from {1}. Reason: {2}'.format(member, ctx.message.server, reason))

    @commands.has_permissions(ban_members=True)
    @commands.command(pass_context=True)
    async def ban(self, ctx, member : str=None, *, reason : str=None):
        '''Bans a specified person.'''
        if member is None:
            await self.bot.say('Please input a user.')
        elif member is not None and reason is None:
            await self.bot.say('Please input a reason')
        elif member is not None and reason is not None:
            member = ctx.message.mentions[0]
            await self.bot.ban(member)
            await self.bot.say('Kicked {0}. Reason: {1}'.format(member, reason))
            log('{0} has been kicked from {1}. Reason: {2}'.format(member, ctx.message.server, reason))

def log(message):
    print(datetime.now(), message)

def setup(bot):
    bot.add_cog(Admin(bot))