import discord
from bs4 import BeautifulSoup
import asyncio
import datetime
from io import BytesIO


class Archiver:

    def __init__(self, bot):
        self.bot = bot
                
    async def on_message(self, message):
        await self.archive_message(message)

    async def on_message_edit(self, before, after):
        await self.archive_message(after, True, before)

    async def archive_message(self, message, edit: bool = False, before=None):
        
        # if message not in whitelisted server
        if message.guild not in (self.bot.whitelisted_servers if self.bot.whitelisted_servers else []): # (or bot still booting up)
            return

        # if the message is in an archive channel, ignore
        if(await self.is_in_archive_channel(message)):
            return

        # sending an message with an embed somehow triggers on_message_edit - this should prevent double messages 
        if(len(message.embeds) > 0 and edit):
            return

        # generate archive channel name
        archive_channel_name = f"ar-{message.channel.name}"

        # if generated channel doesn't exist in either server, default to ar-other
        if(discord.utils.get(self.bot.backup_server.channels, name=archive_channel_name) == None or discord.utils.get(self.bot.main_server.channels, name=archive_channel_name) == None):
            archive_channel_name = "ar-other"

        # get channels for both main and backup servers
        mainserver_archive_channel = discord.utils.get(self.bot.main_server.channels, name=archive_channel_name)
        backupserver_archive_channel = discord.utils.get(self.bot.backup_server.channels, name=archive_channel_name)

        text = None

        # if the message has an embed anyway (likely bot), send that instead 
        if(len(message.embeds) > 0):
            archive_embed = message.embeds[0]
            text = f"{message.author.name}#{message.author.discriminator} sent the following embed at {self.format_time(message.created_at)}:"
        # else send the message in an embed
        else:
            if(len(message.clean_content) > 0):
                archive_embed = await self.generate_archive_embed(message, edit, before)
            # if message is empty (likely attachment only), send no embed
            else:
                archive_embed = None
        
        # if message text is empty, add extra message
        if(len(message.attachments) > 0):
            if(len(message.clean_content) == 0):
                text = f"{message.author.name}#{message.author.discriminator} sent the following attachment(s) at {self.format_time(message.created_at)}:"
            else:
                text = "\n---\nAttachments:"

        # send messages to both servers
        await mainserver_archive_channel.send(content=text, embed=archive_embed, files=(await self.filify(message.attachments) if message.attachments else None))
        await backupserver_archive_channel.send(content=text, embed=archive_embed, files=(await self.filify(message.attachments) if message.attachments else None))

    # checks if a message is sent in an archive channel
    async def is_in_archive_channel(self, message):
        if(message.channel.name.startswith("ar-")):
            return True
        return False

    async def generate_archive_embed(self, message, edit: bool = False, before = None):
        embed = discord.Embed()
        embed.set_author(name=f"{message.author.name}#{message.author.discriminator}", icon_url=message.author.avatar_url)
        
        footer_text = f"#{message.channel.name} | Sent: {self.format_time(message.created_at)}"
        
        if(edit):
            embed.title = "Edited message"
            embed.add_field(
                name="Before",
                value=before.clean_content
            )
            embed.add_field(
                name="After",
                value=message.clean_content
            )

            footer_text += f" | Edited: {self.format_time(message.edited_at)}"

        else:
            embed.add_field(
                name="Message",
                value=message.clean_content
            )

        if(len(message.attachments) > 0):
            embed.add_field(
                name="Attachments included",
                value="See above"
            )

        embed.set_footer(text=footer_text)

        return embed

    def format_time(self, time):
        return time.strftime("%Y-%m-%d %H:%M:%S")

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
