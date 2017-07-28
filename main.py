import discord
import asyncio
import websockets
import authDeets
import time
from discord.ext import commands
import random
import youtube_dl
import csv
from datetime import datetime

description = '''Cassandra Help'''
client = commands.Bot(command_prefix='-', description=description)
bot = client
version = 'Version: 1.2' 

@client.event
async def on_member_join(member):
    await bot.add_roles(member, discord.utils.get(member.server.roles, name="Elevens [Users]"))

    joinEmbed = discord.Embed(title='{}'.format(member) + " has joined the server.",
                             description='Join Date: {} UTC'.format(member.joined_at), color=discord.Color.green())
    joinEmbed.set_footer(text="User Joined")
    joinEmbed.set_thumbnail(url=member.avatar_url)
    await bot.send_message(discord.utils.get(member.server.channels, name='joinleave'), embed=joinEmbed)

@client.event
async def on_member_remove(member):
    server = member.server
    leaveEmbed = discord.Embed(title='{}'.format(member) +  " has left the server.", description= 'Leave Date: {} UTC'.format(datetime.datetime.now()), color=discord.Color.red())
    leaveEmbed.set_footer(text=datetime.datetime.now())
    leaveEmbed.set_thumbnail(url=member.avatar_url)
    await bot.send_message(discord.utils.get(member.server.channels, name='joinleave'), embed=leaveEmbed)


@client.event
async def on_ready():
    print("Logged in as: {0}, with the ID of: {1}".format(client.user, client.user.id))
    await client.change_presence(game=discord.Game(name='in a Digital Haunt', url="https://twitch.tv/ghostofsparkles", type=1))
    print("--")

    if not discord.opus.is_loaded():
        # the 'opus' library here is opus.dll on windows
        # or libopus.so on linux in the current directory
        # you should replace this with the location the
        # opus library is located in and with the proper filename.
        # note that on windows this DLL is automatically provided for you
        discord.opus.load_opus('opus')

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
    # Ping warning
    # Change last 2 conditionals to single if have mod role but cba atm
    if ("301392743840874497" in message.content) and message.author.id != client.user.id and message.author.id != "227187657715875841" and message.author.id != "108875988967882752":
        log( 'Ping-Warn ID:' + message.author.id)
        warningPing = "**Do not abuse the ping role!** {}".format(message.author.mention)
        await client.send_message(message.channel, warningPing)
        await client.delete_message(message)
        logMsg = "!! PING ABUSE !! {0} ({1})".format(message.author, message.author.id)
        log(logMsg)

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

    # Commands
    # Role Command
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
                await bot.send_message(ctx.message.channel, "Failed to add `{0}` role to {1}".format(role, ctx.message.author.name))
                logMsg = "{1} failed to add the {0} role to themselves".format(role, ctx.message.author.name)
                log(logMsg
            finally:
                await bot.send_message(ctx.message.channel, "Successfully added `{0}` role to {1}".format(role, ctx.message.author.name))
                logMsg = "{1} added the {0} role to themselves".format(role, ctx.message.author.name)
                log(logMsg)
        else:
            try:
                await bot.remove_roles(ctx.message.author, discord.utils.get(ctx.message.server.roles, name=role))
            except:
                await bot.send_message(ctx.message.channel, "Failed to remove `{0}` role from {1}".format(role, ctx.message.author.name))
                logMsg = "{1} failed to remove the {0} role from themselves".format(role, ctx.message.author.name)
                log(logMsg)
            finally:
                await bot.send_message(ctx.message.channel, "Successfully removed `{0}` role from {1}".format(role, ctx.message.author.name))
                logMsg = "{} removed the {} role from themselves".format(role, ctx.message.author.name)
                log(logMsg)
    elif action not in acceptableTypes:
        await bot.send_message(ctx.message.channel, "Invalid parameter!")
    elif action in acceptableTypes and role not in acceptableRoles:
        await bot.send_message(ctx.message.channel, "Invalid role!")
        
    # Who am I Command
@bot.command(pass_context = True)
async def whoami(ctx):
    """Tells you your identity"""
    whoamiEmbed = discord.Embed(title="{}'s Information".format(ctx.message.author.name), description='Join Date: {0.joined_at} \n User ID: {0.id} \n Discriminator: {0.discriminator}'.format(ctx.message.author), color=discord.Color.gold())
    whoamiEmbed.set_footer(text=version)
    whoamiEmbed.set_thumbnail(url=ctx.message.author.avatar_url)
    await bot.send_message(ctx.message.channel, embed=whoamiEmbed)

    # About Command
@bot.command(pass_context = True)
async def about(ctx):
    """Tells you about this bot."""
    aboutEmbed = discord.Embed(title='About Cassandra', description="Custom Discord Bot", url="https://github.com/Avinch/CassBotPy", color=discord.Color.gold())
    aboutEmbed.set_footer(text=version)
    aboutEmbed.set_thumbnail(url=bot.user.avatar_url)
    await bot.send_message(ctx.message.channel, embed=aboutEmbed)

    # User Info Command
@bot.command()
async def userinfo(member : discord.Member):
    """Says when a member joined."""
    await bot.say('{0.name} joined in {0.joined_at}'.format(member))
    
    # Ping Command
@bot.command(pass_context = True)
async def ping(ctx):
    """Pong!"""
    msgTimeSent = ctx.message.timestamp
    msgNow = datetime.now()
    await bot.send_message(ctx.message.channel, "The message was sent at: " + str(msgNow - msgTimeSent))
    
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
        self.audio_player = self.bot.loop.create_task(self.audio_player_task())

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False

        player = self.current.player
        return not player.is_done()

    @property
    def player(self):
        return self.current.player

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
        """Plays a song."""
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
    async def playing(self, ctx):
        """Shows info about the currently played song."""

        state = self.get_voice_state(ctx.message.server)
        if state.current is None:
            await self.bot.say('Not playing anything.')
bot.add_cog(Music(bot))

warn_channel = "modlog"
mod_watch_list = []
async def mod_watch_write(ctx, bot):
    mod_watch_list.append(ctx.message.author.id)
    if mod_watch_list.count(ctx.message.author.id) == 1:
        logMsg = ctx.message.author.id + '(`' + ctx.message.author.mention + '`) has been added to the mod watch list.'
        log(logMsg)
        await ping_warn(ctx, logMsg)
    if mod_watch_list.count(ctx.message.author.id) == 2:
        logMsg = ctx.message.author.id + '(`' + ctx.message.author.mention + '`) has been found twice on the list!'
        log(logMsg)
        await ping_warn(ctx, logMsg)
    if mod_watch_list.count(ctx.message.author.id) >= 3:
        id_occurances = mod_watch_list.count(ctx.message.author.id)
        logMsg = ctx.message.author.id + '(`' + ctx.message.author.mention + '`) has been found more than twice on the list! Action must be taken imminently!'
        log(logMsg)
        await ping_warn(ctx, logMsg)

async def ping_warn(ctx, message):
    mod_watch_warn_embed = discord.Embed(title='Ping Warning!', description=message, color=discord.Color.red())
    mod_watch_warn_embed.set_footer(text='WARNING')
    mod_watch_warn_embed.set_thumbnail(url=ctx.message.author.avatar_url)
    await client.send_message(client.get_channel(warn_channel), embed=mod_watch_warn_embed)

def log(message):
    print(datetime.now(), message)

client.run(authDeets.token)
