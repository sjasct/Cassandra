import os
import sys
import json


def get_appdata():
    if sys.platform != 'win32':
        raise OSError('This only works on Windows.')
    else:
        return os.getenv('APPDATA')


def get_api_keys():
    appdata = get_appdata()
    directory = appdata + '\\cassandra'
    json_config = directory + '\\api_keys.json'
    if os.path.exists(directory):
        with open(json_config) as file:
            config = json.load(file)
        return config
    else:
        raise OSError('Cannot run on this PC.')


def setup(bot):
    bot.api_keys = get_api_keys()