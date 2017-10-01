import discord
from discord.ext import commands
import random
import asyncio
import Dependencies
from datetime import datetime
from Plugins import Bot as botPlg

def log(message):
    botPlg.log(message)

class Admin():

    def __init__(self, bot):
        self.bot = bot

    #strike
    @commands.has_role('Mods')
    @commands.command()
    async def strike(self, ctx, member: str=None, *, reason: str=None):
        'Gives a strike to a specified person.'
        if (member is None):
            await ctx.send('Please input a user.')
        elif ((member is not None) and (reason is None)):
            await ctx.send('Please input a reason')
        elif ((member is not None) and (reason is not None)):
            member = ctx.message.mentions[0]
            strike_embed = discord.Embed(title='Strike', description='User: **{0}** \nReason: {1}'.format(member, reason), color=discord.Color.red())
            strike_embed.set_footer(text='Strike')
            await discord.utils.get(ctx.guild.channels, name=Dependencies.logChannel).send('<@&332973960318943233>', embed=strike_embed)
            strike_embed = discord.Embed(title='Strike', description='You have been given a strike in {0}. \nReason: {1}'.format(ctx.guild, reason), color=discord.Color.red())
            strike_embed.set_footer(text='Strike')
            await member.send(embed=strike_embed)
            logMsg = '{0} has been striked on the {1} server. Reason: {2}'.format(member, ctx.guild, reason)
            log(logMsg)

    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def kick(self, ctx, member: str=None, *, reason: str=None):
        'Kicks a specified person.'
        if (member is None):
            await ctx.send('Please input a user.')
        elif ((member is not None) and (reason is None)):
            await ctx.send('Please input a reason')
        elif ((member is not None) and (reason is not None)):
            member = ctx.message.mentions[0]
            await member.kick()
            await ctx.send('Kicked {0}. Reason: {1}'.format(member, reason))
            log('{0} has been kicked from {1}. Reason: {2}'.format(member, ctx.guild, reason))

    @commands.has_permissions(ban_members=True)
    @commands.command()
    async def ban(self, ctx, member: str=None, *, reason: str=None):
        'Bans a specified person.'
        if (member is None):
            await ctx.send('Please input a user.')
        elif ((member is not None) and (reason is None)):
            await ctx.send('Please input a reason')
        elif ((member is not None) and (reason is not None)):
            member = ctx.message.mentions[0]
            await member.ban()
            await ctx.send('Kicked {0}. Reason: {1}'.format(member, reason))
            log('{0} has been kicked from {1}. Reason: {2}'.format(member, ctx.guild, reason))
#'\ndef log(message):\n    print(datetime.now(), message)\n'

def setup(bot):
    bot.add_cog(Admin(bot))
