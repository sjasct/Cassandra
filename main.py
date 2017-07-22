import discord
import asyncio
import websockets
import authDeets
import datetime
import time
from discord.ext import commands
import random
import logging
import youtube_dl

description = '''Cassandra Help'''
client = commands.Bot(command_prefix='-', description=description)
bot = client
version = 'version 1.1'

@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    await client.change_presence(game=discord.Game(name='in a Digital Haunt'))
    print("--")

@client.event
async def on_message(message):
    # Ping warning
    # change last 2 conditionals to single if have mod role but cba atm
    if ("301392743840874497" in message.content) and message.author.id != client.user.id and message.author.id != "227187657715875841" and message.author.id != "108875988967882752":
        print(message.author.id)
        warningPing = "**Do not abuse the ping role!** " + message.author.mention
        await client.send_message(message.channel, warningPing)
        await client.delete_message(message)
        logMsg = "!! PING ABUSE !! " + message.author.name + "#" + message.author.discriminator
        log(logMsg)

    # System;Start #1
    if message.content.lower() == "cassandra can you hear me":
        if message.author.voice.voice_channel == None:
            if True:
                await bot.send_message(message.channel, "Yes.")
                logMsg = message.author.name + " asked Cassandra if she could hear them (text)"
                log(logMsg)
        else:
            vc = discord.utils.get(message.server.channels, id=message.author.voice.voice_channel.id)
            voice = await client.join_voice_channel(vc)
            player = voice.create_ffmpeg_player('ss1.mp3')
            player.start()
            time.sleep(4)
            await voice.disconnect()
            logMsg = message.author.name + " asked Cassandra if she could hear them (voice)"
            log(logMsg)
    # System;Start #2
    if message.content.lower() == "cassandra are you ready to begin" or message.content.lower() == "are you ready to begin":
        if message.author.voice.voice_channel == None:
            if True:
                await bot.send_message(message.channel, "Yes,")
                time.sleep(1)
                await bot.send_message(message.channel, "I'm ready.")
                logMsg = message.author.name + " asked Cassandra if she was ready to begin (text)"
                log(logMsg)
        else:
            vc = discord.utils.get(message.server.channels, id=message.author.voice.voice_channel.id)
            voice = await client.join_voice_channel(vc)
            player = voice.create_ffmpeg_player('ss2.mp3')
            player.start()
            time.sleep(5)
            await voice.disconnect()
            logMsg = message.author.name + " asked Cassandra if she was ready to begin (voice)"
            log(logMsg)
    await bot.process_commands(message)

    #Commands
#Ping Command
@bot.command(pass_context = True)
async def role(ctx, action : str, role : str):
    """Adds roles that you are eligible for."""
    acceptableRoles = ["battlenet", "ping"]
    acceptableTypes = ["add", "remove", "+", "-"]

    if(action in acceptableTypes and role in acceptableRoles):
        if action is "add" or action is "+":
            try:
                await bot.add_roles(ctx.message.author, discord.utils.get(ctx.message.server.roles, name=role))
            except:
                await say(contextChannel, "Failed to add `" + role + "` role to " + ctx.message.author.name)
                logMsg = ctx.message.author.name + " failed to add the " + role + " role to themselves"
                log(logMsg)
            finally:
                await bot.send_message(ctx.message.channel, "Successfully added `" + role + " ` role to " + ctx.message.author.name)
                logMsg = ctx.message.author.name + " added the " + role + " role to themselves"
                log(logMsg)
        else:
            try:
                await bot.remove_roles(ctx.message.author, discord.utils.get(ctx.message.server.roles, name=role))
            except:
                await bot.send_message(ctx.message.channel, "Failed to remove `" + role + "` role from " + ctx.message.author.name)
                logMsg = ctx.message.author.name + " failed to remove the " + role + " role from themselves"
                log(logMsg)
            finally:
                await bot.send_message(ctx.message.channel, "Successfully removed `" + role + " ` role from " + ctx.message.author.name)
                logMsg = ctx.message.author.name + " removed the " + role + " role from themselves"
                log(logMsg)
    elif action not in acceptableTypes:
        await bot.send_message(ctx.message.channel, "Invalid parameter!")
    elif action in acceptableTypes and role not in acceptableRoles:
        await bot.send_message(ctx.message.channel, "Invalid role!")
@bot.command(pass_context = True)
async def playlist(ctx, playlist : str):
    #youtube_dl.utils.DownloadError: ERROR: Unable to download webpage: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:645)> (caused by URLError(SSLError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:645)'),))
    #Are you getting the above error? https://github.com/rg3/youtube-dl/issues/11573#issuecomment-269896421
    playlistAlbums = ['ATLITS', 'MS', 'Blackline', 'Underline', 'LIR']
    if playlist not in playlistAlbums:
        bot.send_message(ctx.message.channel, 'You have not chosen a playlist. The playlists are: ATLITS, MS, Blackline, Underline, LIR')
    elif(playlist in playlistAlbums):
        if ctx.message.author.voice.voice_channel is None:
            await bot.send_message(ctx.message.channel, 'You are not in a voice channel.')
        else:
            await bot.send_message(ctx.message.channel, 'Please Wait...')
            if (playlist == "ATLITS"):
                thePlaylist = "https://www.youtube.com/watch?v=KyUYbAWjdx8"
                nowPlaying = "All The Lights In The Sky"
                bot.send_message(ctx.message.channel, 'Now playing the ' + nowPlaying + ' album by Area 11.')
                vc = ctx.message.author.voice.voice_channel
                voice = await client.join_voice_channel(vc)
                player = await voice.create_ytdl_player(thePlaylist)
                player.start()
                logMsg = ctx.message.author.name + " started the " + nowPlaying + " playlist in " + ctx.message.author.voice.voice_channel.name + " Voice Channel."
                log(logMsg)
                #await bot.send_message(ctx.message.channel, "**[WIP]** As of this update, an official playlist of all of the songs in **All The Lights In The Sky** has not been made. Hopefully by the next update, there will be a playlist of all of the songs in **All The Lights In The Sky**. " + ctx.message.author.mention)
            elif (playlist == "MS"):
                thePlaylist = "https://www.youtube.com/watch?v=mmiCnhC0Q-o&ab_channel=ViperFinn"
                nowPlaying = "Modern Synthesis"
                bot.send_message(ctx.message.channel, 'Now playing the ' + nowPlaying + ' album by Area 11.')
                vc = ctx.message.author.voice.voice_channel
                voice = await client.join_voice_channel(vc)
                player = await voice.create_ytdl_player(thePlaylist)
                player.start()
                logMsg = ctx.message.author.name + " started the " + nowPlaying + " playlist in " + ctx.message.author.voice.voice_channel.name + " Voice Channel." 
                log(logMsg)
            elif (playlist == "Blackline"):
                '''thePlaylist = "NULL"
                vc = ctx.message.author.voice.voice_channel
                voice = await client.join_voice_channel(vc)
                player = await voice.create_ytdl_player(thePlaylist)
                logMsg = ctx.message.author.name + " started the " + playlist + " playlist in " + ctx.message.author.voice.voice_channel.name + " Voice Channel." 
                log(logMsg)
                player.start()
                nowPlaying = "Blackline"'''
                await bot.send_message(ctx.message.channel, "**[WIP]** As of this update, an official playlist of all of the songs in **Blackline EP** has not been made. Hopefully by the next update, there will be a playlist of all of the songs in **Blackline EP**. " + ctx.message.author.mention)
            elif (playlist == "Underline"):
                '''thePlaylist = "NULL"
                vc = ctx.message.author.voice.voice_channel
                voice = await client.join_voice_channel(vc)
                player = await voice.create_ytdl_player(thePlaylist)
                logMsg = ctx.message.author.name + " started the " + playlist + " playlist in " + ctx.message.author.voice.voice_channel.name + " Voice Channel." 
                log(logMsg)
                player.start()
                nowPlaying = "Underline"'''
                await bot.send_message(ctx.message.channel, "**[WIP]** As of this update, an official playlist of all of the songs in **Underline** has not been made. Hopefully by the next update, there will be a playlist of all of the songs in **Underline**. " + ctx.message.author.mention)
            elif (playlist == "LIR"):
                '''thePlaylist = "NULL"
                vc = ctx.message.author.voice.voice_channel
                voice = await client.join_voice_channel(vc)
                player = await voice.create_ytdl_player(thePlaylist)
                logMsg = ctx.message.author.name + " started the " + playlist + " playlist in " + ctx.message.author.voice.voice_channel.name + " Voice Channel." 
                log(logMsg)
                player.start()
                nowPlaying = "Let It Resonate"'''
                await bot.send_message(ctx.message.channel, "**[WIP]** As of this update, an official playlist of all of the songs in **Let It Resonate** has not been made. Hopefully by the next update, there will be a playlist of all of the songs in **Let It Resonate**. " + ctx.message.author.mention)
#NOT WORKING ATM
'''@bot.command(pass_context = True)
async def stop_voice(ctx):
    if client.is_voice_connected(ctx.message.server) is False:
        await bot.send_message(ctx.message.channel, 'I am not in a voice channel.')
    else:
        await bot.send_message(ctx.message.channel, 'Stopping...')
        await client.voice.disconnect()
        await bot.send_message(ctx.message.channel, 'L' + stopVoiceChannelName)'''
    #About Command
@bot.command(pass_context = True)
async def about(ctx):
    """Tells you about this bot."""
    aboutEmbed = discord.Embed(title='About Cassandra', description="Custom Discord Bot", url="https://github.com/Avinch/CassBotPy", color=discord.Color.gold())
    aboutEmbed.set_footer(text=version)
    aboutEmbed.set_thumbnail(url=bot.user.avatar_url)
    await bot.send_message(ctx.message.channel, embed=aboutEmbed)

def log(message):
    print(datetime.datetime.now(), message)

client.run(authDeets.token)
