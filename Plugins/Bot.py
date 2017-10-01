import discord
from discord.ext import commands
import random
import asyncio
from datetime import datetime
import Dependencies

class Bot():

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def role(self, ctx, action: str=None, role: str=None):
        'Adds roles that you are eligible for.'
        acceptableRoles = ['battlenet', 'ping']
        acceptableTypes = ['add', 'remove', '+', '-']
        if ((action in acceptableTypes) and (role in acceptableRoles)):
            if ((action == 'add') or (action == '+')):
                try:
                    await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, name=role))
                except:
                    await ctx.channel.send('Failed to add `{0}` role to {1}'.format(role, ctx.author.name))
                    logMsg = '{1} failed to add the {0} role to themselves'.format(role, ctx.author.name)
                    log(logMsg)
                finally:
                    await ctx.channel.send('Successfully added `{0}` role to {1}'.format(role, ctx.author.name))
                    logMsg = '{1} added the {0} role to themselves'.format(role, ctx.author.name)
                    log(logMsg)
            else:
                try:
                    await ctx.author.remove_roles(discord.utils.get(ctx.guild.roles, name=role))
                except:
                    await ctx.channel.send('Failed to remove `{0}` role from {1}'.format(role, ctx.author.name))
                    logMsg = '{1} failed to remove the {0} role from themselves'.format(role, ctx.author.name)
                    log(logMsg)
                finally:
                    await ctx.channel.send('Successfully removed `{0}` role from {1}'.format(role, ctx.author.name))
                    logMsg = '{} removed the {} role from themselves'.format(role, ctx.author.name)
                    log(logMsg)
        elif (action not in acceptableTypes):
            await ctx.channel.send('Invalid parameter!')
        elif ((action in acceptableTypes) and (role not in acceptableRoles)):
            await ctx.channel.send('Invalid role!')

    @commands.command()
    async def whoami(self, ctx):
        'Tells you your identity'
        whoamiEmbed = discord.Embed(title="{0}'s Information".format(ctx.author.name), description='Join Date: {0.joined_at} \n User ID: {0.id} \n Discriminator: {0.discriminator}'.format(ctx.author), color=discord.Color.gold())
        whoamiEmbed.set_footer(text='Who Am I Command')
        whoamiEmbed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.channel.send(embed=whoamiEmbed)

    @commands.command()
    async def userinfo(self, ctx, member: str=None):
        '[W.I.P] Says when a member joined.'
        member = ctx.message.mentions[0]
        if (member is None):
            await ctx.send('Please input a user.')
        else:
            await ctx.send('{0.name} joined in {0.joined_at}'.format(member))

    @commands.command()
    async def suggest(self, ctx, *, suggestion: str=None):
        'Suggest features you hope to see on this bot!'
        if (suggestion is None):
            ctx.send('Please input your suggestion.')
        else:
            await ctx.send('Feedback Taken.')
            suggestion_embed = discord.Embed(title='Suggestion', description='Suggestion: *{0} by {1}*'.format(suggestion, ctx.author), color=discord.Color.purple())
            suggestion_embed.set_footer(text='Suggestion for Cassandra')
            await discord.utils.get(ctx.guild.channels, id=Dependencies.logChannel).send(embed=suggestion_embed)
    # @commands.command(pass_context = True)\n    async def rule(self, ctx, rule : str):\n        '''Displays a specific rule, or all rules.'''\n        rule_array = ['1', '2', '3', '4', '5', '6', '7']\n        if (rule == '1'):\n            await self.bot.send_message(ctx.channel, dep.rule_one)\n        if (rule == '2'):\n            await self.bot.send_message(ctx.channel, dep.rule_two)\n        if (rule == '3'):\n            await self.bot.send_message(ctx.channel, dep.rule_three)\n        if (rule == '4'):\n            await self.bot.send_message(ctx.channel, dep.rule_four)\n        if (rule == '5'):\n            await self.bot.send_message(ctx.channel, dep.rule_five)\n        if (rule == '6'):\n            await self.bot.send_message(ctx.channel, dep.rule_six)\n        if (rule == '7'):\n            await self.bot.send_message(ctx.channel, dep.rule_seven)\n        if (rule not in rule_array):\n            await self.bot.send_message(ctx.channel, 'There are only 7 rules.')"

    @commands.command()
    async def ping(self, ctx):
        'Pong!'
        msgTimeSent = ctx.message.timestamp
        msgNow = datetime.now()
        await ctx.channel.send(('Pong! This message was sent at: ' + str((msgNow - msgTimeSent))))
        logMsg = (ctx.author.name + ' just sent the bot a ball! (-ping)')
        log(logMsg)

    @commands.command()
    async def about(self, ctx):
        'Tells you about this bot.'
        aboutEmbed = discord.Embed(title='About Cassandra', description='Custom Discord Bot', url='https://github.com/Avinch/CassBotPy', color=discord.Color.gold())
        aboutEmbed.set_footer(text=Dependencies.version)
        aboutEmbed.set_thumbnail(url=self.bot.user.avatar_url)
        await ctx.channel.send(embed=aboutEmbed)

    @commands.command()
    async def id(self, ctx, type: str=None, request: str=None):
        message = 'The id of the {0} `{1}` is '.format(type, request)
        accept_type = ['channel', 'user', 'member', 'server', 'role']
        if (type in accept_type):
            if (type == 'server'):
                message = 'The id of the {0} is '.format(type)
                await ctx.channel.send((message + ctx.guild.id))
                log((ctx.author.name + ' requested the ID of the {0}'.format(type)))
            elif (request is not None):
                object = get(ctx, type, request)
                if (object == None):
                    await ctx.channel.send('**Error!** A {0} named {1} could not be found! You must enter the exact name (including caps)'.format(request, type))
                else:
                    message = 'The id of the {0} `{1}` is '.format(type, request)
                    await ctx.channel.send((message + get(ctx, type, request).id))
                    log((ctx.author.name + ' requested the ID of the {0} {1}'.format(type, request)))
        else:
            await ctx.channel.send((type + ' does not have an ID!'))

    @commands.has_role("Mods")
    @commands.command()
    async def disclaimer(self, ctx):
        message = "The Area 11 Discord:tm: is a space where all users should be happy and comfortable. Breaking the rules is a violation of that comfort, and though it seems hostile to do so, the moderator team must enorce the rules."
        await ctx.send(message)

    
    @commands.command(pass_context = True)
    async def parvJar(self, ctx):
        """The Parv Jar"""

        name = discord.utils.get(ctx.message.guild.members, id="254840014876180492").name
    
        parvfile = open("parvjar.txt", "r")

        noOfParv = parvfile.read()

        parvfile.close()

        message = "{0} has mentioned Parv a total of {1} times!".format(name, noOfParv)
    
        await ctx.send(message)

    @commands.command(pass_context = True)
    async def trello(self, ctx):
        """Trello Board for Cassandra!"""

        message = "**Cassandra Trello board for bot progress:**\nhttps://trello.com/b/RPRZyqWx/cassandra-discord-bot"
    
        await ctx.send(message)

def get(ctx, type, name):
    if (type == 'channel'):
        get = ctx.guild.channels
    elif ((type == 'user') or (type == 'member')):
        get = ctx.guild.members
    elif (type == 'role'):
        get = ctx.guild.roles
    elif (type == 'server'):
        get = ctx.guild
    try:
        fin = discord.utils.get(get, name=name)
    except:
        print('failed')
    finally:
        return fin

def log(message):
    print(datetime.now(), '｜｜', message)

def setup(bot):
    bot.add_cog(Bot(bot))
