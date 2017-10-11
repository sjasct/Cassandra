from pathlib import Path
from discord.ext import commands
import discord
import logging
import json
import datetime
import authDeets

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


class Utils:
    def get_package_info(self, arg: str):
        """Fetches `arg` in `package.json`."""
        with open("package.json") as f:
            config = json.load(f)

        return config[arg]


class Bot(commands.Bot):
    """This is the class that initializes the bot."""
    def __init__(self):
        self.presence = discord.Game(name='in a Digital Haunt...'
                                     , url="https://www.twitch.tv/ghostofsparkles", type=1)
        self.up_time = datetime.datetime.utcnow()

        def get_prefix():
            """Fetches all known prefixes."""
            return ["-",
                    "Cassandra ",
                    "<@300007940679663618> "]

        def get_description():
            """Fetches description."""
            return f"{Utils().get_package_info('name')}"

        def get_game():
            """Fetches game presence."""
            return self.presence

        super().__init__(command_prefix=get_prefix(), game=get_game(), description=get_description(), pm_help=None,
                         help_attrs=dict(hidden=True))

        startup_extensions = [x.stem for x in Path('cogs').glob('*.py')]
        for extension in startup_extensions:
            try:
                self.load_extension(f'cogs.{extension}')
            except Exception as e:
                error = f'{extension}\n {type(e).__name__}: {e}'
                print(f'Failed to load extension {error}')


if __name__ == '__main__':
    bot = Bot()
    bot.run(authDeets.token)
