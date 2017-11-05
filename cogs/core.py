import asyncio
import datetime
import re
import textwrap
from io import BytesIO

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
    'libopus.0.dylib'
]


class Core:
    def __init__(self, bot):
        self.bot = bot
        self.main_server = None
        self.backup_server = None
        self.mod_log = None

    @staticmethod
    def get_invites(message):
        """Fetches all invites from message"""
        regex = re.match(DISCORD_INVITE, message.content)

        return regex

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
        self.main_server = self.bot.get_guild(338732924893659137)
        self.backup_server = self.bot.get_guild(338732924893659137)  # 349652162948759555
        self.mod_log = discord.utils.get(self.main_server.channels, name="mod-log")
        self.bot.session = aiohttp.ClientSession()
        print(textwrap.dedent(f"""
        =====================================
        Discord Version: {discord.__version__}
        Username: {self.bot.user.name}
        User ID: {self.bot.user.id}
        Started: {datetime.datetime.utcnow()} UTC
        Opus: {'Loaded' if self.load_opus_lib() else 'Failed'}
        ====================================="""))

    async def archive(self, message, edit: bool, before=None):
        """Archives messages"""
        if message.author.bot:
            return
        if message.guild != self.main_server:
            return
        if edit:
            edit = '**EDIT** '
        else:
            edit = ''
        channel_name = f"ar-{message.channel.name}"
        if before:
            before = f"Before: {before.clean_content} "
        if discord.utils.get(self.backup_server.channels, name=channel_name):
            ar_msg = [
                f"{edit}**Author** - `{message.author}` (`{message.author.id}`)"
                f" **Channel** - `{message.channel.name}` (`{message.channel.id}`)"
                f" **Message ID** - `{message.id}`"
                f" {before if edit else ''}**Message** - \"{message.clean_content}\""
            ]
        else:
            channel_name = "ar-other"
            ar_msg = [
                f"{edit}**Author** - `{message.author}` (`{message.author.id}`)"
                f" **Message ID** - `{message.id}`"
                f" {before if edit else ''}**Message** - \"{message.clean_content}\""
            ]
        ar_msg = ' '.join(parts for parts in ar_msg)
        self.bot.archive_file.append(ar_msg)
        ar_channel_1 = discord.utils.get(self.main_server.channels, name=channel_name)
        ar_channel_2 = discord.utils.get(self.backup_server.channels, name=channel_name)
        await ar_channel_1.send(ar_msg, files=(await self.filify(message.attachments) if message.attachments else None))
        await ar_channel_2.send(ar_msg, files=(await self.filify(message.attachments) if message.attachments else None))

    async def on_message_edit(self, before, after):
        """A `bot` event triggered when a message is edited."""
        # Archiver
        await self.archive(after, True, before)

    async def on_message(self, message):
        """A `bot` event triggered when a message is sent."""
        ping_role = discord.utils.get(message.guild.roles, name="ping")
        # Bot Checker
        if message.author.bot:
            return
        # Main Server Checker
        if message.guild != self.main_server:
            return
        # Non-Mod Checker
        if not checks.is_mod(message.guild, message.author):
            # Non-Mod Ping Mention Checker
            if ping_role.id in message.raw_role_mentions:
                msg = f"**Do not abuse the ping role!** {message.author.mention}"
                # Ping Mention Consequence
                await message.channel.send(msg)
                await message.delete()
                await message.author.edit(roles=[], reason="Ping Role Mention")
                # Ping Mention Mod Log Embed
                alert_embed = discord.Embed(
                    title="Ping Role Mention",
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
                await self.mod_log.send(embed=alert_embed)
            # Non-Mod Invite Checker
            if self.get_invites(message):
                msg = f"**Do not send invites!** {message.author.mention}"
                await message.channel.send(msg)
                await message.delete()
        # Lower-Case Message Checker
        if message.content.islower():
            member_voice = message.author.voice
            # Lower-Case System;Start 1
            if message.content == "cassandra can you hear me":
                if member_voice:
                    vc = await message.author.voice.channel.connect()
                    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('audio\/ss1.mp3'))
                    vc.play(source)
                    await asyncio.sleep(4)
                    await vc.disconnect()
                else:
                    await message.channel.send("Yes.")
            # Lower-Case System;Start 2
            elif message.content in ["cassandra are you ready to begin", "are you ready to begin"]:
                if member_voice:
                    vc = await message.author.voice.channel.connect()
                    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('audio\/ss2.mp3'))
                    vc.play(source)
                    await asyncio.sleep(5)
                    await vc.disconnect()
                else:
                    await message.channel.send("Yes,")
                    await asyncio.sleep(1)
                    await message.channel.send("I'm ready.")
        # Archiver
        await self.archive(message, False)


def setup(bot):
    bot.add_cog(Core(bot))
