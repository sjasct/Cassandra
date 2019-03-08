import discord
from bs4 import BeautifulSoup
from enum import Enum
import asyncio
import datetime
from github import Github
import sys
import json
from io import BytesIO


class Archiver:

    
    def __init__(self, bot):
        self.bot = bot
        
    async def archive(self, message, edit: bool, before=None):
        """Archives messages"""
        if message.author.bot:
            return
        if message.guild not in self.bot.whitelisted_servers:
            return
        if edit:
            edit = '**EDIT** '
        else:
            edit = ''
        channel_name = f"ar-{message.channel.name}"
        if before:
            before = f"Before: {before.clean_content} "
        if discord.utils.get(self.bot.backup_server.channels, name=channel_name):
            ar_msg = [
                f"{edit}**Author** - `{message.author}` (`{message.author.id}`)"
                
                f" **Message ID** - `{message.id}`"
                f" {before if edit else ''}**Message** - \"{message.clean_content}\""
            ]
        else:
            channel_name = "ar-other"
            ar_msg = [
                f"{edit}**Author** - `{message.author}` (`{message.author.id}`)"
                f" **Channel** - `{message.channel.name}` (`{message.channel.id}`)"
                f" **Message ID** - `{message.id}`"
                f" {before if edit else ''}**Message** - \"{message.clean_content}\""
            ]
        ar_msg = ' '.join(parts for parts in ar_msg)
        self.bot.archive_file.append(ar_msg)
        ar_channel_1 = discord.utils.get(self.bot.main_server.channels, name=channel_name)
        ar_channel_2 = discord.utils.get(self.bot.backup_server.channels, name=channel_name)
        await ar_channel_1.send(ar_msg, files=(await self.filify(message.attachments) if message.attachments else None))
        await ar_channel_2.send(ar_msg, files=(await self.filify(message.attachments) if message.attachments else None))
    
    async def on_message(self, message):
        await self.archive(message, False)

    async def on_message_edit(self, before, after):
        """A `bot` event triggered when a message is edited."""
        # Archiver
        await self.archive(after, True, before)

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

def setup(bot):
    bot.add_cog(Archiver(bot))
