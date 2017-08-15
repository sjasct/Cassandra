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

def log(message):
    botPlg.log(message)

startup_extensions = ["Plugins.Admin", "Plugins.Bot", "Plugins.Dev"]
description = '''Cassandra Help'''
client = commands.Bot(command_prefix='-', description=description)
bot = client

def log(message):
    botPlg.log(message)

@client.event
async def on_ready():
    print("================")
    log("Connect Successful")
    logMsg = "Logged in as: {0}, with the ID of: {1}".format(client.user, client.user.id)
    log(logMsg)
    print("================")
    await client.change_presence(
        game=discord.Game(name='in a Digital Haunt', url="https://twitch.tv/ghostofsparkles", type=1))
    if __name__ == "__main__":
        for extension in startup_extensions:
            try:
                bot.load_extension(extension)
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load extension {}\n{}'.format(extension, exc))

@client.event
async def on_member_join(member):
    server = member.server
    joinEmbed = discord.Embed(title="{} has joined the server.".format(member), description= 'Join Date: {} UTC'.format(member.joined_at), color=discord.Color.green())
    joinEmbed.set_footer(text='User Joined')
    joinEmbed.set_thumbnail(url=member.avatar_url)
    await bot.send_message(discord.utils.get(member.server.channels, name='joinleave'), embed=joinEmbed)
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
async def on_message(message):
    
    # Ping mention abuse
    if ((discord.utils.get(message.server.roles, name="ping").id) in message.content) and message.author.id != client.user.id and discord.utils.get(message.server.roles, name="Mods") not in message.author.roles:
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

    if ("discord.gg/" in message.clean_content or "discordapp.com/invite" in message.clean_content and message.author.id != client.user.id and discord.utils.get(message.server.roles, name="Mods") not in message.author.roles):

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
    if message.author.id == "301449773200834561":
        member = message.author.mention
        await bot.send_message(message.channel, 'Thank you for your time at {0}. Understandable, have a nice day, {1}.'.format(message.server.name, message.author.mention))
        await asyncio.sleep(10)
        await bot.replace_roles(message.author)
        await bot.send_message(message.author, 'You are being banned from {0} in 50 seconds. Hope you have a good evening.'.format(message.server.name))
        await asyncio.sleep(50)
        await bot.ban(message.author)
        await bot.send_message(message.channel, '{} has been banned.'.format(member))
    await bot.process_commands(message)

log("Attempting to connect to Discord...")
client.run(authDeets.token)
