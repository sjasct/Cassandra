import datetime
import json
import discord
import os
from discord.ext import commands
from discord.ext.commands.converter import *


class CassandraContext(commands.Context):
    def is_float(self, argument):
        """Checks if the argument is a float."""
        try:
            return float(argument)  # True if string is a number contains a dot
        except ValueError:  # String is not a number
            return False

    async def send(self, content=None, *args, **kwargs):
        """Override for send to add message filtering"""
        if content:
            if self.is_float(content) or content.isdigit():
                content = str(content)
            content.replace("@everyone", "@\u200beveryone").replace("@here", "@\u200bhere")
        sent_message = await super().send(content, *args, **kwargs)
        return sent_message

    @property
    def session(self):
        """Returns the aiohttp.ClientSession() instance in CassandraBase."""
        return self.bot.session


class CassandraBase(commands.Bot):
    """This is the class that initializes the bot."""
    def __init__(self):
        self.token = os.environ['TOKEN']
        self.presence = discord.Game(name='in a Digital Haunt...',
                                     url="https://www.twitch.tv/ghostofsparkles", type=1)
        self.archive_file = []

        def get_package_info():
            """Fetches `arg` in `package.json`."""
            with open("./package.json") as f:
                config = json.load(f)

            return config

        def get_prefix():
            """Fetches all known prefixes."""
            prefixes = ["-",
                        "Cassandra "]
            return commands.when_mentioned_or(*prefixes)

        def get_description():
            """Fetches description."""
            return f"{get_package_info()['name']}"

        def get_game():
            """Fetches game presence."""
            return self.presence

        super().__init__(command_prefix=get_prefix(), game=get_game(), description=get_description(), pm_help=None,
                         help_attrs=dict(hidden=True))

        startup_extensions = []
        for file in os.listdir("./cogs"):
            if file.endswith(".py"):
                startup_extensions.append(file.replace('.py', ''))
        print(startup_extensions)
        for extension in startup_extensions:
            try:
                print(f'cogs.{extension}')
                self.load_extension(f'cogs.{extension}')
                print(f'Loaded {extension}')
            except Exception as e:
                error = f'{extension}\n {type(e).__name__}: {e}'
                print(f'Failed to load extension {error}')

        self.session = None

    def run(self):
        """Runs the bot."""
        super().run(self.token)

    async def on_message(self, message):
        """An event triggered when a message is sent."""
        ctx = await self.get_context(message, cls=CassandraContext)
        await self.invoke(ctx)

    async def fetch(self, url: str, headers: dict = None, timeout: float = None,
                    return_type: str = None, **kwargs):
        """Fetches data from a url via aiohttp."""

        async with self.session.get(url, headers=headers, timeout=timeout, **kwargs) as resp:
            if return_type:
                cont = getattr(resp, return_type)
                return resp, await cont()
            else:
                return resp, None


class Cassandra(CassandraBase):
    pass


class ConvertError(Exception):
    pass


class Union(Converter):
    def __init__(self, *converters):
        self.converters = converters

    async def convert(self, ctx: CassandraContext, argument: str):
        """Converts an argument"""
        for converter in self.converters:
            try:
                return await ctx.command.do_conversion(ctx, converter, argument)
            except:
                raise ConvertError('Conversion Failed.')

