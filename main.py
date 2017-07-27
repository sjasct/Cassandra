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

@client.event
async def on_member_join(member):
    await bot.add_roles(member, discord.utils.get(member.server.roles, name="Elevens [Users]"))

@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    await client.change_presence(game=discord.Game(name='in a Digital Haunt'))
    print("--")

    if not discord.opus.is_loaded():
        # the 'opus' library here is opus.dll on windows
        # or libopus.so on linux in the current directory
        # you should replace this with the location the
        # opus library is located in and with the proper filename.
        # note that on windows this DLL is automatically provided for you
        discord.opus.load_opus('opus')

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
    if message.content.lower().startswith("cassandra can you hear me"):
        if message.author.voice.voice_channel == None:
            if True:
                await client.send_message(message.channel, "Yes.")
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
    if message.content.lower().startswith("cassandra are you ready to begin"):
        if message.author.voice.voice_channel == None:
            if True:
                await client.send_message(message.channel, "Yes,")
                time.sleep(1)
                await client.send_message(message.channel, "I'm ready.")
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
        if action == "add" or action == "+":
            try:
                await bot.add_roles(ctx.message.author, discord.utils.get(ctx.message.server.roles, name=role))
            except:
                await bot.send_message(ctx.message.channel, "Failed to add `" + role + "` role to " + ctx.message.author.name)
                logMsg = ctx.message.author.name + " failed to add the " + role + " role to themselves"
                print(logMsg)
            finally:
                await bot.send_message(ctx.message.channel, "Successfully added `" + role + " ` role to " + ctx.message.author.name)
                logMsg = ctx.message.author.name + " added the " + role + " role to themselves"
                print(logMsg)
        else:
            try:
                await bot.remove_roles(ctx.message.author, discord.utils.get(ctx.message.server.roles, name=role))
            except:
                await bot.send_message(ctx.message.channel, "Failed to remove `" + role + "` role from " + ctx.message.author.name)
                logMsg = ctx.message.author.name + " failed to remove the " + role + " role from themselves"
                print(logMsg)
            finally:
                await bot.send_message(ctx.message.channel, "Successfully removed `" + role + " ` role from " + ctx.message.author.name)
                logMsg = ctx.message.author.name + " removed the " + role + " role from themselves"
                print(logMsg)
    elif action not in acceptableTypes:
        await bot.send_message(ctx.message.channel, "Invalid parameter!")
    elif action in acceptableTypes and role not in acceptableRoles:
        await bot.send_message(ctx.message.channel, "Invalid role!")
'''@bot.command(pass_context = True)
async def playlist(ctx, playlist : str):
    if playlist == None:
        bot.send_message(ctx.message.channel, 'You have not chosen a playlist. The playlists are: ATLITS, MS, Blackline, Underline, LIR')
    else:
        if ctx.message.author.voice.voice_channel == None:
            await bot.send_message(ctx.message.channel, 'You are not in a voice channel.')
        else:
            vc = discord.utils.get(message.server.channels, id=message.author.voice.voice_channel.id)
            voice = await client.join_voice_channel(vc)
            player = voice.create_ffmpeg_player('ss2.mp3')
            player.start()
            time.sleep(5)
            await voice.disconnect()
            logMsg = message.author.name + " asked Cassandra if she was ready to begin (voice)"
            log(logMsg)
@bot.command(pass_context = True)
async def stop_voice(ctx):
    if bot.voice.voice_channel == None:
        await bot.send_message(ctx.message.channel, 'I am not in a voice channel.')
    else:
        await bot.send_message(ctx.message.channel, 'Stopping...')
        await voice.disconnect()
        await bot.send_message(ctx.message.channel, 'Left' + voice_channel.name)'''
    #About Command
@bot.command(pass_context = True)
async def about(ctx):
    """Tells you about this bot."""
    aboutEmbed = discord.Embed(title='About Cassandra', description="Custom Discord Bot", url="https://github.com/Avinch/CassBotPy", color=discord.Color.gold())
    aboutEmbed.set_footer(text="version 1.1 testing")
    aboutEmbed.set_thumbnail(url=bot.user.avatar_url) #aboutEmbed.set_thumbnail(url=client.user.avatar_url)
    await bot.send_message(ctx.message.channel, embed=aboutEmbed) #await client.send_message(message.channel, embed=aboutEmbed)

@bot.command(pass_context = True)
async def ping(ctx):
    msgTimeSent = ctx.message.timestamp
    msgNow = datetime.datetime.now()
    await bot.send_message(ctx.message.channel, "The message was sent at: " + str(msgNow - msgTimeSent))

def log(message):
    print(datetime.datetime.now(), message)

client.run(authDeets.token)
