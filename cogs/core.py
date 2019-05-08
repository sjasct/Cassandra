import asyncio
import datetime
import re
import textwrap
from io import BytesIO
import sys
import json

import aiohttp
import discord

from utils import checks

DISCORD_INVITE = r'discord(?:app\.com|\.gg)[\/invite\/]?(?:(?!.*[Ii10OolL]).[a-zA-Z0-9]{5,6}|[a-zA-Z0-9\-]{2,32})'

INVITE_WHITELIST = [
    "https://discord.gg/CMnKYPA"
    "http://discord.gg/Sg3Wznq"
    "https://discord.gg/AJMHQCM"
    "https://discord.gg/atKZZ7y"
]

OPUS_LIBS = [
    'libopus-0.x86.dll',
    'libopus-o.x64.dll',
    'libopus-0.dll',
    'libopus.so.0',
    'libopus.0.dylib',
    'libopus.so'
]


class Core:
    def __init__(self, bot):
        self.bot = bot
        self.mod_log = None
        self.blacklist = []

    @staticmethod
    def get_invites(message):
        """Fetches all invites from message"""
        regex = re.match(DISCORD_INVITE, message.content)

        return regex

    def check_testing(self):
        if(len(sys.argv)>=2 and sys.argv[1] == "-test"):
            return True
        return False

    @staticmethod
    def load_opus_lib(opus_libs=OPUS_LIBS):
        """Loads LibOpus For `bot`."""
        if discord.opus.is_loaded():
            return True

        for opus_lib in opus_libs:
            try:
                discord.opus.load_opus(opus_lib)
                return True
            except OSError:
                pass

    @staticmethod
    async def filify(attachments):
        """Converts attachments of an instance of `discord.Message` to a list of instances of `discord.File`."""
        ret = []
        for file in attachments:
            byte = BytesIO()
            await file.save(byte)
            byte.seek(0)
            ret.append(discord.File(byte, filename=file.filename))
        return ret

    async def on_ready(self):
        """A `bot` event triggered when the bot authentication has been successful.
         Notifies console when `bot` is ready."""


        testvalue = self.check_testing()
        if(testvalue == True):
            testingservers = json.load(open('testingdata.json'))
            self.bot.main_server = self.bot.get_guild(testingservers["main_server"])
            self.bot.backup_server = self.bot.get_guild(testingservers["backup_server"]) 
        else:
            self.bot.main_server = self.bot.get_guild(212982046992105473)
            self.bot.backup_server = self.bot.get_guild(349652162948759555) 

        self.bot.whitelisted_servers = [
            self.bot.main_server, 
            self.bot.get_guild(173152280634327040), #avinchtest
            self.bot.get_guild(338732924893659137) #cassbotpy
        ]
        self.mod_log = discord.utils.get(self.bot.main_server.channels, name="mod-log")
        self.bot.session = aiohttp.ClientSession()
        print(textwrap.dedent(f"""
        =====================================
        discord.py Version: {discord.__version__}
        Python Version: {sys.version}
        Bot Username: {self.bot.user.name}
        Bot User ID: {self.bot.user.id}
        Started: {datetime.datetime.utcnow()} UTC
        Opus: {'Loaded' if self.load_opus_lib() else 'Failed'}
        ====================================="""))
    
    async def on_message(self, message):
        """A `bot` event triggered when a message is sent."""
        ping_role = discord.utils.get(message.guild.roles, name="ping")
        gamenight_role = discord.utils.get(message.guild.roles, name="gamenight")

        if (message.content.find("leveled up") != -1) and message.author.id == "172002275412279296":
            await message.channel.send("<:ding:230664475554873344>")

        # Bot Checker
        if message.author.bot:
            return
        # Main Server Checker
        if message.guild not in self.bot.whitelisted_servers:
            return
        # Non-Mod Checker
        if not checks.is_mod(message.guild, message.author):
            # Non-Mod Ping Mention Checker
            if ping_role.id in message.raw_role_mentions or gamenight_role.id in message.raw_role_mentions:
                msg = f"**Do not abuse pingable roles!** {message.author.mention}"
                # Ping Mention Consequence
                await message.channel.send(msg)
                await message.delete()
                await message.author.edit(roles=[], reason="Pingable Role Mention")
                # Ping Mention Mod Log Embed
                alert_embed = discord.Embed(
                    title="Pingable Role Mention",
                    description=f'User: **{message.author.name}** \nChannel: {message.channel.name}',
                    color=discord.Color.red()
                )
                alert_embed.add_field(
                    name="User:",
                    value=message.author.name
                )
                alert_embed.add_field(
                    name="Channel",
                    value=f"{message.channel.name}({message.channel.id})"
                )
                alert_embed.set_thumbnail(url=message.author.avatar_url)
                alert_embed.set_footer(text='Abuse Notification')
                await discord.utils.get(message.guild.channels, name="mod-log").send(embed=alert_embed)
            # Non-Mod Invite Checker
            if self.get_invites(message):
                msg = f"**Do not send invites!** {message.author.mention}"
                await message.channel.send(msg)
                await message.delete()
        member_voice = message.author.voice
        # Lower-Case System;Start 1
        if str(message.content).lower() in ["cassandra can you hear me", "cassandra, can you hear me?", "cassandra can you hear me?", "cassandra, can you hear me"] : # todo: replace with regex
            if member_voice:
                vc = await message.author.voice.channel.connect()
                source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('audio/ss1.mp3'))
                vc.play(source)
                await asyncio.sleep(4)
                await vc.disconnect()
            else:
                await message.channel.send("Yes.")
        # Lower-Case System;Start 2
        elif str(message.content).lower() in ["cassandra are you ready to begin", "are you ready to begin", "cassandra, are you ready to begin", "cassandra are you ready to begin?", "cassandra, are you ready to begin?"]: # todo: replace with regex
            if member_voice:
                vc = await message.author.voice.channel.connect()
                source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('audio/ss2.mp3'))
                vc.play(source)
                await asyncio.sleep(5)
                await vc.disconnect()
            else:
                await message.channel.send("Yes,")
                await asyncio.sleep(1)
                await message.channel.send("I'm ready.")
        # Archiver
        if message.author.id in self.blacklist:
            await message.channel.send(f'Thank you for your time at {message.guild.name}. Understandable, have a nice day, {message.author.mention}.')
            await message.author.edit(roles=[], reason='r/Area11Banned Special')
            await message.author.send(f'You have been banned from {message.guild.name}. Hope you have a good evening.')
            await message.author.ban(reason='r/Area11Banned Special')


def setup(bot):
    bot.add_cog(Core(bot))
