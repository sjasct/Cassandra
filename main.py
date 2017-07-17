import discord
import asyncio
import websockets
import authDeets
import datetime
import time


client = discord.Client()

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
    if "cassandra can you hear me" in message.content.lower():

        #NOT WORKING ATM
        #if message.author.voice.voice_channel == None:

        if 1 == 1:

            await client.send_message(message.channel, "Yes.")

            logMsg = message.author.name + " asked Cassandra if she could hear them (text)"
            log(logMsg)

        '''else:

            vc = discord.utils.get(message.server.channels, id=message.author.voice.voice_channel.id)
            voice = await client.join_voice_channel(vc)
            player = voice.create_ffmpeg_player('ss1.mp3')
            player.start()
            time.sleep(4)
            await voice.disconnect()

            logMsg = message.author.name + " asked Cassandra if she could hear them (voice)"
            log(logMsg)'''

    # System;Start #2
    if "cassandra are you ready to begin" in message.content.lower():

        # NOT WORKING ATM
        #if message.author.voice.voice_channel == None:

        if 1 == 1:
            await client.send_message(message.channel, "Yes,")
            time.sleep(1)
            await client.send_message(message.channel, "I'm ready.")

            logMsg = message.author.name + " asked Cassandra if she was ready to begin (text)"
            log(logMsg)

        '''else:

            vc = discord.utils.get(message.server.channels, id=message.author.voice.voice_channel.id)
            voice = await client.join_voice_channel(vc)
            player = voice.create_ffmpeg_player('ss2.mp3')
            player.start()
            time.sleep(5)
            await voice.disconnect()

            logMsg = message.author.name + " asked Cassandra if she was ready to begin (voice)"
            log(logMsg)'''

    # role addition/removal
    if message.content.startswith("-role"):

        acceptableRoles = ["battlenet", "ping"]
        acceptableTypes = ["add", "remove", "+", "-"]

        command = message.content.split(" ")

        if(command[1] in acceptableTypes and command[2] in acceptableRoles):

            if command[1] == "add" or command[1] == "+":

                try:

                    await client.add_roles(message.author, discord.utils.get(message.server.roles, name=command[2]))

                except:

                    await client.send_message(message.channel, "Failed to add `" + command[2] + "` role to " + message.author.name)

                    logMsg = message.author.name + " failed to add the " + command[2] + "role to themselves"
                    log(logMsg)

                finally:

                    await client.send_message(message.channel, "Successfully added `" + command[2] + " ` role to " + message.author.name)

                    logMsg = message.author.name + " added the " + command[2] + "role to themselves"
                    log(logMsg)

            else:

                try:

                    await client.remove_roles(message.author, discord.utils.get(message.server.roles, name=command[2]))

                except:

                    await client.send_message(message.channel, "Failed to remove `" + command[2] + "` role from " + message.author.name)

                    logMsg = message.author.name + " failed to remove the " + command[2] + "role from themselves"
                    log(logMsg)

                finally:

                    await client.send_message(message.channel, "Successfully removed `" + command[2] + " ` role from " + message.author.name)

                    logMsg = message.author.name + " removed the " + command[2] + "role from themselves"
                    log(logMsg)

        elif command[1] not in acceptableTypes:

            await client.send_message(message.channel, "Invalid parameter!")

        elif command[1] in acceptableTypes and command[2] not in acceptableRoles:

            await client.send_message(message.channel, "Invalid role!")

    if message.content.startswith("-about"):

        aboutEmbed = discord.Embed(title='About Cassandra', description="Custom Discord Bot", url="https://github.com/Avinch/CassBotPy", color=discord.Color.gold())
        aboutEmbed.set_footer(text="version 1.0")
        aboutEmbed.set_thumbnail(url=client.user.avatar_url)
        await client.send_message(message.channel, embed=aboutEmbed)


def log(message):
    print(datetime.datetime.now(), message)

client.run(authDeets.token)
