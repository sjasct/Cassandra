import discord
from discord.ext import commands
import random
import asyncio
from datetime import datetime
import Dependencies

class Bot():
    def __init__(self, bot):
        self.bot = bot

        # Commands
    # Role Command
    @commands.command(pass_context = True)
    async def role(self, ctx, action : str=None, role : str=None):
        """Adds roles that you are eligible for."""
        acceptableRoles = ["battlenet", "ping"]
        acceptableTypes = ["add", "remove", "+", "-"]

        if(action in acceptableTypes and role in acceptableRoles):
            if action == "add" or action == "+":
                try:
                    await self.bot.add_roles(ctx.message.author, discord.utils.get(ctx.message.server.roles, name=role))
                except:
                    await self.bot.send_message(ctx.message.channel, "Failed to add `{0}` role to {1}".format(role, ctx.message.author.name))
                    logMsg = "{1} failed to add the {0} role to themselves".format(role, ctx.message.author.name)
                    log(logMsg)
                finally:
                    await self.bot.send_message(ctx.message.channel, "Successfully added `{0}` role to {1}".format(role, ctx.message.author.name))
                    logMsg = "{1} added the {0} role to themselves".format(role, ctx.message.author.name)
                    log(logMsg)
            else:
                try:
                    await self.bot.remove_roles(ctx.message.author, discord.utils.get(ctx.message.server.roles, name=role))
                except:
                    await self.bot.send_message(ctx.message.channel, "Failed to remove `{0}` role from {1}".format(role, ctx.message.author.name))
                    logMsg = "{1} failed to remove the {0} role from themselves".format(role, ctx.message.author.name)
                    log(logMsg)
                finally:
                    await self.bot.send_message(ctx.message.channel, "Successfully removed `{0}` role from {1}".format(role, ctx.message.author.name))
                    logMsg = "{} removed the {} role from themselves".format(role, ctx.message.author.name)
                    log(logMsg)
        elif action not in acceptableTypes:
            await self.bot.send_message(ctx.message.channel, "Invalid parameter!")
        elif action in acceptableTypes and role not in acceptableRoles:
            await self.bot.send_message(ctx.message.channel, "Invalid role!")

    @commands.command(pass_context = True)
    async def whoami(self, ctx):
        """Tells you your identity"""
        whoamiEmbed = discord.Embed(title="{0}'s Information".format(ctx.message.author.name), description='Join Date: {0.joined_at} \n User ID: {0.id} \n Discriminator: {0.discriminator}'.format(ctx.message.author), color=discord.Color.gold())
        whoamiEmbed.set_footer(text='Who Am I Command')
        whoamiEmbed.set_thumbnail(url=ctx.message.author.avatar_url)
        await self.bot.send_message(ctx.message.channel, embed=whoamiEmbed)
        
    @commands.command()
    async def userinfo(self, member : str=None):
        """[W.I.P] Says when a member joined."""
        member = ctx.message.mentions[0]
        if member is None:
            await self.bot.say('Please input a user.')
        else:
            await self.bot.say('{0.name} joined in {0.joined_at}'.format(member))

        # suggest command
    @commands.command(pass_context=True)
    async def suggest(self, ctx, *, suggestion : str=None):
        '''Suggest features you hope to see on this bot!'''
        if suggestion is None:
            self.bot.say('Please input your suggestion.')
        else:
            await self.bot.say('Feedback Taken.')
            suggestion_embed = discord.Embed(title="Suggestion", description= 'Suggestion: *{0} by {1}*'.format(suggestion, ctx.message.author), color=discord.Color.purple())
            suggestion_embed.set_footer(text='Suggestion for TomBot')
            await self.bot.send_message(discord.utils.get(ctx.message.server.channels, id=dependencies.suggestions_channel), embed=suggestion_embed)

        # rule command
    """@commands.command(pass_context = True)
    async def rule(self, ctx, rule : str):
        '''Displays a specific rule, or all rules.'''
        rule_array = ['1', '2', '3', '4', '5', '6', '7']
        if (rule == '1'):
            await self.bot.send_message(ctx.message.channel, dep.rule_one)
        if (rule == '2'):
            await self.bot.send_message(ctx.message.channel, dep.rule_two)
        if (rule == '3'):
            await self.bot.send_message(ctx.message.channel, dep.rule_three)
        if (rule == '4'):
            await self.bot.send_message(ctx.message.channel, dep.rule_four)
        if (rule == '5'):
            await self.bot.send_message(ctx.message.channel, dep.rule_five)
        if (rule == '6'):
            await self.bot.send_message(ctx.message.channel, dep.rule_six)
        if (rule == '7'):
            await self.bot.send_message(ctx.message.channel, dep.rule_seven)
        if (rule not in rule_array):
            await self.bot.send_message(ctx.message.channel, 'There are only 7 rules.')"""

        # ping command
    @commands.command(pass_context = True)
    async def ping(self, ctx):
        """Pong!"""
        msgTimeSent = ctx.message.timestamp
        msgNow = datetime.now()
        await self.bot.send_message(ctx.message.channel, "Pong! This message was sent at: " + str(msgNow - msgTimeSent))

        # About Command
    @commands.command(pass_context = True)
    async def about(self, ctx):
        """Tells you about this bot."""
        aboutEmbed = discord.Embed(title='About Cassandra', description="Custom Discord Bot", url="https://github.com/Avinch/CassBotPy", color=discord.Color.gold())
        aboutEmbed.set_footer(text=Dependencies.version)
        aboutEmbed.set_thumbnail(url=self.bot.user.avatar_url)
        await self.bot.send_message(ctx.message.channel, embed=aboutEmbed)

def log(message):
    print(datetime.now(), message)
    
def setup(bot):
    bot.add_cog(Bot(bot))