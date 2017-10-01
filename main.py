import discord
import asyncio
import websockets
import authDeets
import time
from discord.ext import commands
import random
from datetime import datetime
import Plugins
import Dependencies
from datetime import datetime
from Plugins import Bot as botPlg

#from apscheduler.schedulers.blocking import BlockingScheduler

# Custom logging
def log(message):
    botPlg.log(message)

global archiveFile
archiveFile = []

backupServerId = "349652162948759555"

# list of files to be included
startup_extensions = ["Plugins.Admin", "Plugins.Bot", "Plugins.Dev"]

# help command 
description = '''Cassandra Help'''

# sets command prefix and help 
client = commands.Bot(command_prefix='-', description=description)

bot = client

# Event: When the bot comes online
@client.event
async def on_ready():

    # print to console success message
    print("================")
    log("Connect Successful")
    logMsg = "Logged in as: {0}, with the ID of: {1}".format(client.user, client.user.id)
    log(logMsg)
    print("================")

    # set game to "in a digital haunt.." and streaming to true
    await client.change_presence(
game=discord.Game(name='in a Digital Haunt', url="https://twitch.tv/ghostofsparkles", type=1))

    # loads all the extension files (as defined )
    if __name__ == "__main__":
        for extension in startup_extensions:
            try:
                bot.load_extension(extension)
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load extension {}\n{}'.format(extension, exc))

# Event: When someone joines
@client.event
async def on_member_join(member):

    # gets the member's server
    server = member.server

    # sets the embed style
    joinEmbed = discord.Embed(title="{} has joined the server.".format(member), description= 'Join Date: {} UTC'.format(member.joined_at), color=discord.Color.green())
    joinEmbed.set_footer(text='User Joined')
    joinEmbed.set_thumbnail(url=member.avatar_url)

    # gets a channel named 'joinleave' in the member's server and sends the embed variable
    await bot.send_message(discord.utils.get(member.server.channels, name='joinleave'), embed=joinEmbed)

    # gets a role named 'elevens [us]..' from the member's server and adds it to the member
    await bot.add_roles(member, discord.utils.get(member.server.roles, name="Elevens [Users]"))
    logMsg = "{0} ({0.id}) has just joined {1}. Added the 'Elevens [User]' Role to {0}.".format(member, server)
    log(logMsg)

@client.event
async def on_member_remove(member):
    server = member.server
    leaveEmbed = discord.Embed(title="{} has left the server.".format(member), description= 'Leave Date: {} UTC'.format(datetime.utcnow()), color=discord.Color.red())
    leaveEmbed.set_footer(text='User Left')
    leaveEmbed.set_thumbnail(url=member.avatar_url)
    await bot.send_message(discord.utils.get(member.server.channels, name='joinleave'), embed=leaveEmbed)
    logMsg = "{0} ({0.id}) has just left {1}.".format(member, server)
    log(logMsg)




@client.event
async def on_message_edit(before, after):

    backupServer = discord.utils.get(client.servers, id=backupServerId)

    if after.author.id != client.user.id and before.server.id == "212982046992105473":

        channelName = "ar-"+after.channel.name

        if(discord.utils.get(backupServer.channels, name=channelName) == None):

            channelName = "ar-other"
        
            archiveMessage = "**EDIT**\n\n**Author:** {}#{}\n\n**Message ID:** {}\n\n**Channel:** {}\n\n**Before:**\n{}\n\n**After:**\n{}\n\n-----------------------------------\n\n".format(after.author.name, after.author.discriminator, after.id, after.channel.name, before.clean_content, after.clean_content)
        
        else:

            channelName = "ar-"+after.channel.name
        
            archiveMessage = "**EDIT**\n\n**Author:** {}#{}\n\n**Message ID:** {}\n\n**Before:**\n{}\n\n**After:**\n{}\n\n-----------------------------------\n\n".format(after.author.name, after.author.discriminator, after.id, before.clean_content, after.clean_content)

        

        archiveFile.append(archiveMessage)
        archiveChannelOne = discord.utils.get(backupServer.channels, name=channelName)
        archiveChannelTwo = discord.utils.get(before.server.channels, name=channelName)
        await bot.send_message(archiveChannelOne, archiveMessage)
        await bot.send_message(archiveChannelTwo, archiveMessage)

@client.event
async def on_message(message):

    backupServer = discord.utils.get(client.servers, id=backupServerId)

    if("parv" in message.content.lower() and message.author.id == "254840014876180492" and message.content.lower() != "-parvjar"):

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
        archiveChannelTwo = discord.utils.get(message.server.channels, name=channelName)
        await bot.send_message(archiveChannelOne, archiveMessage)
        await bot.send_message(archiveChannelTwo, archiveMessage)

    # Ping mention abuse
    if (message.server.id != backupServerId and (discord.utils.get(message.server.roles, name="ping").id) in message.content) and message.author.id != client.user.id and discord.utils.get(message.server.roles, name="Mods") not in message.author.roles:
        warningPing = "**Do not abuse the ping role!** {}".format(message.author.mention)
        await client.send_message(message.channel, warningPing)
        await client.delete_message(message)

        logMsg = "!! PING ABUSE !! {0} ({1})".format(message.author, message.author.id)
        log(logMsg)
        await bot.replace_roles(message.author)

        alert_embed = discord.Embed(title="Ping Role Mention", description= 'User: **{0}** \nChannel: {1}'.format(message.author.name, message.channel.name), color=discord.Color.red())
        alert_embed.set_footer(text='Abuse Notification')
        await bot.send_message(discord.utils.get(message.server.channels, name=Dependencies.logChannel),embed=alert_embed)

        alert_embed = discord.Embed(title="Ping Role Mention", description= 'User: **{0}** \nChannel: {1}'.format(message.author.name, message.channel.name), color=discord.Color.red())
        alert_embed.set_footer(text='Abuse Notification')
        await bot.send_message(discord.utils.get(message.server.channels, name=Dependencies.logChannel),embed=alert_embed)

    if (message.server.id != backupServerId and  ("discord.gg/" in message.clean_content or "discordapp.com/invite" in message.clean_content) and message.author.id != client.user.id and discord.utils.get(message.server.roles, name="Mods") not in message.author.roles):

        warningPing = "**Do not send invites!** {}".format(message.author.mention)
        await client.send_message(message.channel, warningPing)
        await client.delete_message(message)

        logMsg = "{0} ({1}) sent an invite in {2}".format(message.author, message.author.id, message.server.name)
        log(logMsg)

        alert_embed = discord.Embed(title="Invite Sent", description= 'User: **{0}** \nChannel: {1}'.format(message.author.name, message.channel.name), color=discord.Color.red())
        alert_embed.set_footer(text='Abuse Notification')
        await bot.send_message(discord.utils.get(message.server.channels, name=Dependencies.logChannel),embed=alert_embed)

    # System;Start #1
    if message.content.lower() == "cassandra can you hear me":
        if message.author.voice.voice_channel == None:
            if True:
                await bot.send_message(message.channel, "Yes.")
                logMsg = "{} asked Cassandra if she could hear them (text)".format(message.author)
                log(logMsg)
        else:
            vc = discord.utils.get(message.server.channels, id=message.author.voice.voice_channel.id)
            voice = await client.join_voice_channel(vc)
            player = voice.create_ffmpeg_player('ss1.mp3')
            player.start()
            await asyncio.sleep(4)
            await voice.disconnect()
            logMsg = "{} asked Cassandra if she could hear them (voice)".format(message.author)
            log(logMsg)

    # System;Start #2
    if message.content.lower() == "cassandra are you ready to begin" or message.content.lower() == "are you ready to begin":
        if message.author.voice.voice_channel == None:
            if True:
                await bot.send_message(message.channel, "Yes,")
                time.sleep(1)
                await bot.send_message(message.channel, "I'm ready.")
                logMsg = "{} asked Cassandra if she was ready to begin (text)".format(message.author)
                log(logMsg)
        else:
            vc = discord.utils.get(message.server.channels, id=message.author.voice.voice_channel.id)
            voice = await client.join_voice_channel(vc)
            player = voice.create_ffmpeg_player('ss2.mp3')
            player.start()
            await asyncio.sleep(5)
            await voice.disconnect()
            logMsg = "{} asked Cassandra if she was ready to begin (voice)".format(message.author)
            log(logMsg)

    # r/Area11Banned Discord 1st Anniversary Update Special
    if message.author.id == "166312640329547776":
        member = message.author.mention
        await bot.send_message(message.channel, 'Thank you for your time at {0}. Understandable, have a nice day, {1}.'.format(message.server.name, message.author.mention))
        await asyncio.sleep(10)
        await bot.replace_roles(message.author)
        await bot.send_message(message.author, 'You are being banned from {0} in 50 seconds. Hope you have a good evening.'.format(message.server.name))
        await asyncio.sleep(50)
        await bot.ban(message.author)
        await bot.send_message(message.channel, '{} has been banned.'.format(member))
    await bot.process_commands(message)

'''@client.command(pass_context=True)
async def save(self):
    setArchive()

def setArchive():
    fileName = "ARCHIVE-" + str(random.randint(100000000,9999999999)) + ".txt"
    print(fileName)
    archiveFile = open(fileName, "w")
   
    stuff = archiveFile
    for message in stuff:
        archiveFile.write(message)

    archiveFile = []

    archiveFile.close()'''



log("Attempting to connect to Discord...")
client.run(authDeets.token)


'''
scheduler = BlockingScheduler()
scheduler.add_job(setArchive, 'interval', hours=1)
scheduler.start()'''
