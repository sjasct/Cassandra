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
        if True:
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
        if True:
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
                logMsg = message.author.name + " failed to add the " + role + " role to themselves"
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
    #About Command
@bot.command(pass_context = True)
async def about(ctx):
    """Tells you about this bot."""
    aboutEmbed = discord.Embed(title='About Cassandra', description="Custom Discord Bot", url="https://github.com/Avinch/CassBotPy", color=discord.Color.gold())
    aboutEmbed.set_footer(text="version 1.0")
    aboutEmbed.set_thumbnail(url=bot.user.avatar_url) #aboutEmbed.set_thumbnail(url=client.user.avatar_url)
    await bot.send_message(ctx.message.channel, embed=aboutEmbed) #await client.send_message(message.channel, embed=aboutEmbed)

'''if not discord.opus.is_loaded():
    # the 'opus' library here is opus.dll on windows
    # or libopus.so on linux in the current directory
    # you should replace this with the location the
    # opus library is located in and with the proper filename.
    # note that on windows this DLL is automatically provided for you
    discord.opus.load_opus('opus')

class VoiceEntry:
    def __init__(self, message, player):
        self.requester = message.author
        self.channel = message.channel
        self.player = player

    def __str__(self):
        fmt = '*{0.title}* uploaded by {0.uploader} and requested by {1.display_name}'
        duration = self.player.duration
        if duration:
            fmt = fmt + ' [length: {0[0]}m {0[1]}s]'.format(divmod(duration, 60))
        return fmt.format(self.player, self.requester)

class VoiceState:
    def __init__(self, bot):
        self.current = None
        self.voice = None
        self.bot = bot
        self.play_next_song = asyncio.Event()
        self.songs = asyncio.Queue()
        self.skip_votes = set() # a set of user_ids that voted
        self.audio_player = self.bot.loop.create_task(self.audio_player_task())

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False

        player = self.current.player
        return not player.is_done()

    @property
    def player(self):
        return self.current.player

    def skip(self):
        self.skip_votes.clear()
        if self.is_playing():
            self.player.stop()

    def toggle_next(self):
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

    async def audio_player_task(self):
        while True:
            self.play_next_song.clear()
            self.current = await self.songs.get()
            await self.bot.send_message(self.current.channel, 'Now playing ' + str(self.current))
            self.current.player.start()
            await self.play_next_song.wait()

class Music:
    """Voice related commands.
    Works in multiple servers at once.
    """
    def __init__(self, bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, server):
        state = self.voice_states.get(server.id)
        if state is None:
            state = VoiceState(self.bot)
            self.voice_states[server.id] = state

        return state

    async def create_voice_client(self, channel):
        voice = await self.bot.join_voice_channel(channel)
        state = self.get_voice_state(channel.server)
        state.voice = voice

    def __unload(self):
        for state in self.voice_states.values():
            try:
                state.audio_player.cancel()
                if state.voice:
                    self.bot.loop.create_task(state.voice.disconnect())
            except:
                pass

    @commands.command(pass_context=True, no_pm=True)
    async def join(self, ctx, *, channel : discord.Channel):
        """Joins a voice channel."""
        try:
            await self.create_voice_client(channel)
        except discord.ClientException:
            await self.bot.say('Already in a voice channel...')
        except discord.InvalidArgument:
            await self.bot.say('This is not a voice channel...')
        else:
            await self.bot.say('Ready to play audio in ' + channel.name)

    @commands.command(pass_context=True, no_pm=True)
    async def summon(self, ctx):
        """Summons the bot to join your voice channel."""
        summoned_channel = ctx.message.author.voice_channel
        if summoned_channel is None:
            await self.bot.say('You are not in a voice channel.')
            return False

        state = self.get_voice_state(ctx.message.server)
        if state.voice is None:
            state.voice = await self.bot.join_voice_channel(summoned_channel)
        else:
            await state.voice.move_to(summoned_channel)

        return True

    @commands.command(pass_context=True, no_pm=True)
    async def play(self, ctx, *, song : str):
        """Plays a song.
        If there is a song currently in the queue, then it is
        queued until the next song is done playing.
        This command automatically searches as well from YouTube.
        The list of supported sites can be found here:
        https://rg3.github.io/youtube-dl/supportedsites.html
        """
        state = self.get_voice_state(ctx.message.server)
        opts = {
            'default_search': 'auto',
            'quiet': True,
        }

        if state.voice is None:
            success = await ctx.invoke(self.summon)
            if not success:
                return

        try:
            player = await state.voice.create_ytdl_player(song, ytdl_options=opts, after=state.toggle_next)
        except Exception as e:
            fmt = 'An error occurred while processing this request: ```py\n{}: {}\n```'
            await self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
        else:
            player.volume = 0.6
            entry = VoiceEntry(ctx.message, player)
            await self.bot.say('Enqueued ' + str(entry))
            await state.songs.put(entry)

    @commands.command(pass_context=True, no_pm=True)
    async def volume(self, ctx, value : int):
        """Sets the volume of the currently playing song."""

        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.volume = value / 100
            await self.bot.say('Set the volume to {:.0%}'.format(player.volume))

    @commands.command(pass_context=True, no_pm=True)
    async def pause(self, ctx):
        """Pauses the currently played song."""
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.pause()

    @commands.command(pass_context=True, no_pm=True)
    async def resume(self, ctx):
        """Resumes the currently played song."""
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.resume()

    @commands.command(pass_context=True, no_pm=True)
    async def stop(self, ctx):
        """Stops playing audio and leaves the voice channel.
        This also clears the queue.
        """
        server = ctx.message.server
        state = self.get_voice_state(server)

        if state.is_playing():
            player = state.player
            player.stop()

        try:
            state.audio_player.cancel()
            del self.voice_states[server.id]
            await state.voice.disconnect()
        except:
            pass

    @commands.command(pass_context=True, no_pm=True)
    async def skip(self, ctx):
        """Vote to skip a song. The song requester can automatically skip.
        3 skip votes are needed for the song to be skipped.
        """

        state = self.get_voice_state(ctx.message.server)
        if not state.is_playing():
            await self.bot.say('Not playing any music right now...')
            return

        voter = ctx.message.author
        if voter == state.current.requester:
            await self.bot.say('Requester requested skipping song...')
            state.skip()
        elif voter.id not in state.skip_votes:
            state.skip_votes.add(voter.id)
            total_votes = len(state.skip_votes)
            if total_votes >= 3:
                await self.bot.say('Skip vote passed, skipping song...')
                state.skip()
            else:
                await self.bot.say('Skip vote added, currently at [{}/3]'.format(total_votes))
        else:
            await self.bot.say('You have already voted to skip this song.')

    @commands.command(pass_context=True, no_pm=True)
    async def playing(self, ctx):
        """Shows info about the currently played song."""

        state = self.get_voice_state(ctx.message.server)
        if state.current is None:
            await self.bot.say('Not playing anything.')
        else:
            skip_count = len(state.skip_votes)
            await self.bot.say('Now playing {} [skips: {}/3]'.format(state.current, skip_count))
bot.add_cog(Music(bot))'''

def log(message):
    print(datetime.datetime.now(), message)

client.run(authDeets.token)
