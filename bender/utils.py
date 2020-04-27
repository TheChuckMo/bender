import requests
import click
import configparser
import os

# read configuration file
config = configparser.ConfigParser()
config_file = os.path.join(click.get_app_dir('bender'), 'config.ini')
config.read(config_file)
# print('config file: {}'.format(config_fi


def connect(username, password):
    req = requests.session()
    req.headers.update({'Content-Type': 'application/json'})
    # req.auth = (username, password)
    return req