import discord
import asyncio
import websockets
#import authDeets
import time
from discord.ext import commands
import random
from datetime import datetime
import Plugins
import Dependencies
from datetime import datetime
from Plugins import Bot as botPlg

def log(message):
    botPlg.log(message)
startup_extensions = ['Plugins.Admin', 'Plugins.Bot', 'Plugins.Dev']
description = 'Cassandra Help'
client = commands.Bot(command_prefix='-', description=description)
bot = client

@client.event
async def on_ready():
    print('================')
    log('Connect Successful')
    logMsg = 'Logged in as: {0}, with the ID of: {1}'.format(client.user, client.user.id)
    log(logMsg)
    print('================')
    await client.change_presence(game=discord.Game(name='in a Digital Haunt', url='https://twitch.tv/ghostofsparkles', type=1))
    if (__name__ == '__main__'):
        for extension in startup_extensions:
            try:
                bot.load_extension(extension)
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load extension {}\n{}'.format(extension, exc))

@client.event
async def on_member_join(member):
    guild = member.guild
    joinEmbed = discord.Embed(title='{} has joined the server.'.format(member), description='Join Date: {} UTC'.format(member.joined_at), color=discord.Color.green())
    joinEmbed.set_footer(text='User Joined')
    joinEmbed.set_thumbnail(url=member.avatar_url)
    await discord.utils.get(member.guild.channels, name='joinleave').send(embed=joinEmbed)
    await member.add_roles(discord.utils.get(member.guild.roles, name='Elevens [Users]'))
    logMsg = "{0} ({0.id}) has just joined {1}. Added the 'Elevens [User]' Role to {0}.".format(member, guild)
    log(logMsg)

@client.event
async def on_member_remove(member):
    guild = member.guild
    leaveEmbed = discord.Embed(title='{} has left the server.'.format(member), description='Leave Date: {} UTC'.format(datetime.utcnow()), color=discord.Color.red())
    leaveEmbed.set_footer(text='User Left')
    leaveEmbed.set_thumbnail(url=member.avatar_url)
    await discord.utils.get(member.guild.channels, name='joinleave').send(embed=leaveEmbed)
    logMsg = '{0} ({0.id}) has just left {1}.'.format(member, guild)
    log(logMsg)


@client.event
async def on_message_edit(before, after):

    backupServer = discord.utils.get(client.guilds, id=backupServerId)

    if after.author.id != client.user.id and before.guild.id == "212982046992105473":

        channelName = "ar-"+after.channel.name

        if(discord.utils.get(backupServer.channels, name=channelName) == None):

            channelName = "ar-other"
        
            archiveMessage = "**EDIT**\n\n**Author:** {}#{}\n\n**Message ID:** {}\n\n**Channel:** {}\n\n**Before:**\n{}\n\n**After:**\n{}\n\n-----------------------------------\n\n".format(after.author.name, after.author.discriminator, after.id, after.channel.name, before.clean_content, after.clean_content)
        
        else:

            channelName = "ar-"+after.channel.name
        
            archiveMessage = "**EDIT**\n\n**Author:** {}#{}\n\n**Message ID:** {}\n\n**Before:**\n{}\n\n**After:**\n{}\n\n-----------------------------------\n\n".format(after.author.name, after.author.discriminator, after.id, before.clean_content, after.clean_content)

        

        archiveFile.append(archiveMessage)
        archiveChannelOne = discord.utils.get(backupServer.channels, name=channelName)
        archiveChannelTwo = discord.utils.get(before.guild.channels, name=channelName)
        await archiveChannelOne.send(archiveMessage)
        await archiveChannelTwo.send(archiveMessage)

@client.event
async def on_message(message):

    backupServer = discord.utils.get(client.guilds, id=backupServerId)

    if("parv" in message.content.lower() and message.guild.id == "254840014876180492" and message.content.lower() != "-parvjar"):

        parvfile = open("parvjar.txt", "r")

        noOfParv = int(parvfile.read())

        parvfile.close()

        noOfParv += 1

        parvfile = open("parvjar.txt", "w")
        
        parvfile.write(str(noOfParv))

        parvfile.close()


    if message.author.id != client.user.id and message.server.id == "212982046992105473":

        channelName = "ar-"+message.channel.name

        if(discord.utils.get(backupServer.channels, name=channelName) == None):

            channelName = "ar-other"
        
            archiveMessage = "**Author:** {}#{}\n\n**Message ID:** {}\n\n**Channel:** {}\n\n{}\n\n-----------------------------------\n\n".format(message.author.name, message.author.discriminator, message.id, message.channel.name, message.clean_content)
        
        else:

            channelName = "ar-"+message.channel.name
        
            archiveMessage = "**Author**: {}#{}\n\n**Message ID:** {}\n\n{}\n\n-----------------------------------\n\n".format(message.author.name, message.author.discriminator, message.id, message.clean_content)

        
        archiveFile.append(archiveMessage)
        archiveChannelOne = discord.utils.get(backupServer.channels, name=channelName)
        archiveChannelTwo = discord.utils.get(before.guild.channels, name=channelName)
        await archiveChannelOne.send(archiveMessage)
        await archiveChannelTwo.send(archiveMessage)

    if (str(discord.utils.get(message.guild.roles, name='ping').id) in message.content) and (message.author.id != client.user.id) and (discord.utils.get(message.guild.roles, name='Mods') not in message.author.roles):
        warningPing = '**Do not abuse the ping role!** {}'.format(message.author.mention)
        await message.channel.send(warningPing)
        await message.delete()
        logMsg = '!! PING ABUSE !! {0} ({1})'.format(message.author, message.author.id)
        log(logMsg)
        await message.author.replace_roles()
        alert_embed = discord.Embed(title='Ping Role Mention', description='User: **{0}** \nChannel: {1}'.format(message.author.name, message.channel.name), color=discord.Color.red())
        alert_embed.set_footer(text='Abuse Notification')
        await discord.utils.get(message.guild.channels, name=Dependencies.logChannel).send(embed=alert_embed)
        alert_embed = discord.Embed(title='Ping Role Mention', description='User: **{0}** \nChannel: {1}'.format(message.author.name, message.channel.name), color=discord.Color.red())
        alert_embed.set_footer(text='Abuse Notification')
        await discord.utils.get(message.guild.channels, name=Dependencies.logChannel).send(embed=alert_embed)
    if (('discord.gg/' in message.clean_content) or (('discordapp.com/invite' in message.clean_content)
     and (message.author.id != client.user.id) and (discord.utils.get(message.guild.roles, name='Mods') not in message.author.roles))):
        warningPing = '**Do not send invites!** {}'.format(message.author.mention)
        await message.channel.send(warningPing)
        await message.delete()
        logMsg = '{0} ({1}) sent an invite in {2}'.format(message.author, message.author.id, message.guild.name)
        log(logMsg)
        alert_embed = discord.Embed(title='Invite Sent', description='User: **{0}** \nChannel: {1}'.format(message.author.name, message.channel.name), color=discord.Color.red())
        alert_embed.set_footer(text='Abuse Notification')
        await discord.utils.get(message.guild.channels, name=Dependencies.logChannel).send(embed=alert_embed)
    if (message.content.lower() == 'cassandra can you hear me'):
        if (message.author.voice.voice_channel == None):
            await message.channel.send('Yes.')
            logMsg = '{} asked Cassandra if she could hear them (text)'.format(message.author)
            log(logMsg)
        else:
            vc = discord.utils.get(message.guild.channels, id=message.author.voice.voice_channel.id)
            voice = await vc.connect
            player = voice.create_ffmpeg_player('ss1.mp3')
            player.start()
            await asyncio.sleep(4)
            await voice.disconnect()
            logMsg = '{} asked Cassandra if she could hear them (voice)'.format(message.author)
            log(logMsg)
    if ((message.content.lower() == 'cassandra are you ready to begin') or (message.content.lower() == 'are you ready to begin')):
        if (message.author.voice.voice_channel == None):
            await message.channel.send('Yes,')
            time.sleep(1)
            await message.channel.send("I'm ready.")
            logMsg = '{} asked Cassandra if she was ready to begin (text)'.format(message.author)
            log(logMsg)
        else:
            vc = discord.utils.get(message.guild.channels, id=message.author.voice.voice_channel.id)
            voice = await vc.connect
            player = voice.create_ffmpeg_player('ss2.mp3')
            player.start()
            await asyncio.sleep(5)
            await voice.disconnect()
            logMsg = '{} asked Cassandra if she was ready to begin (voice)'.format(message.author)
            log(logMsg)
    if (message.author.id == 301449773200834561):
        member = message.author.mention
        await message.channel.send('Thank you for your time at {0}. Understandable, have a nice day, {1}.'.format(message.guild.name, message.author.mention))
        await asyncio.sleep(10)
        await message.author.replace_roles()
        await message.author.send('You are being banned from {0} in 50 seconds. Hope you have a good evening.'.format(message.guild.name))
        await asyncio.sleep(50)
        await message.author.ban()
        await message.channel.send('{} has been banned.'.format(member))
    await bot.process_commands(message)
log('Attempting to connect to Discord...')
client.run('MzM1NDc1NDI3Mjk0MzE0NDk4.DLLhlQ.k7e1D7HzhmXlAM0lHrn3h8EVW1w')
