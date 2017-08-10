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

startup_extensions = ["Plugins.Admin", "Plugins.Bot", "Plugins.Dev"]
description = '''Cassandra Help'''
client = commands.Bot(command_prefix='-', description=description)
bot = client

@client.event
async def on_ready():
    print("Logged in as: {0}, with the ID of: {1}".format(client.user, client.user.id))
    await client.change_presence(
        game=discord.Game(name='in a Digital Haunt', url="https://twitch.tv/ghostofsparkles", type=1))
    print("--")
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
    joinEmbed = discord.Embed(title="{} has joined the server.".format(member),
                              description='Join Date: {} UTC'.format(member.joined_at), color=discord.Color.green())
    joinEmbed.set_footer(text='User Joined')
    joinEmbed.set_thumbnail(url=member.avatar_url)
    await bot.send_message(discord.utils.get(member.server.channels, name='joinleave'), embed=joinEmbed)
    await bot.add_roles(member, discord.utils.get(member.server.roles, name="Elevens [Users]"))
    logMsg = "{0} ({0.id}) has just joined {1}. Added the 'Elevens [User]' Role to {0}.".format(member, server)
    log(logMsg)


@client.event
async def on_member_remove(member):
    server = member.server
    leaveEmbed = discord.Embed(title="{} has left the server.".format(member),
                               description='Leave Date: {} UTC'.format(datetime.utcnow()), color=discord.Color.red())
    leaveEmbed.set_footer(text='User Left')
    leaveEmbed.set_thumbnail(url=member.avatar_url)
    await bot.send_message(discord.utils.get(member.server.channels, name='joinleave'), embed=leaveEmbed)
    logMsg = "{0} ({0.id}) has just left {1}.".format(member, server)
    log(logMsg)


@client.event
async def on_message(message):
    # Ping warning
    # Change last 2 conditionals to single if have mod role but cba atm
    if ("301392743840874497" in message.content) and message.author.id != client.user.id and message.author.id != "227187657715875841" and message.author.id != "108875988967882752":
        warningPing = "**Do not abuse the ping role!** {}".format(message.author.mention)
        await client.send_message(message.channel, warningPing)
        await client.delete_message(message)
        logMsg = "!! PING ABUSE !! {0} ({1})".format(message.author, message.author.id)
        log(logMsg)
        await bot.remove_roles(message.author, discord.utils.get(message.server.roles, name="Elevens [Users]"))
        await bot.remove_roles(message.author, discord.utils.get(message.server.roles, name="GO!! Fappers [Regulars]"))
        await bot.remove_roles(message.author, discord.utils.get(message.server.roles, name="News Contributors"))
        await bot.remove_roles(message.author, discord.utils.get(message.server.roles, name="Developers"))

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
            time.sleep(4)
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
            time.sleep(5)
            await voice.disconnect()
            logMsg = "{} asked Cassandra if she was ready to begin (voice)".format(message.author)
            log(logMsg)
    await bot.process_commands(message)


@bot.command(pass_context=True)
async def id(ctx, type: str, request: str):
    message = "The id of the " + type + " `" + request + "` is "
    accept_type = ["channel", "user", "member", "server", "role"]

    log(ctx.message.author.name + " requested the ID of the " + type + " " + request)

    if (type in accept_type):

        object = get(ctx, type, request)

        if object == None:
            await client.send_message(ctx.message.channel,
                                      "**Error!** A " + type + " named " + request + " could not be found! You must enter the exact name (including caps)")
        else:
            await client.send_message(ctx.message.channel, message + get(ctx, type, request).id)

    else:

        await client.send_message(ctx.message.channel, type + " does not have an ID!")


def log(message):
    print(datetime.now(), "||", message)


def get(ctx, type, name):
    if (type == "channel"):
        get = ctx.message.server.channels
    elif (type == "user" or type == "member"):
        get = ctx.message.server.members
    elif (type == "role"):
        get = ctx.message.server.roles

    try:
        fin = discord.utils.get(get, name=name)
    except:
        print("failed")
    finally:
        return fin

client.run(authDeets.token)

