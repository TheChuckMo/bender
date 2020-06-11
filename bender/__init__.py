import configparser
import os

import click
import pkg_resources

__VERSION__ = '0.7.3'

"""bender constants"""
__APP_NAME__ = 'bender'

__APP_DIR__ = click.get_app_dir(__APP_NAME__)
if not os.path.isdir(__APP_DIR__):
    os.mkdir(__APP_DIR__)

APP_CURRENT_DIR = os.getcwd()

APP_VERSION = pkg_resources.get_distribution(__APP_NAME__).version

"""default json headers"""
json_headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

form_headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

no_check_headers = {
    'X-Atlassian-Token': 'no-check'
}

"""bender configuration"""
config_defaults = {
    'cookie_store': f'{os.path.join(__APP_DIR__, ".cookies")}',
    'default_output': 'pretty',
    'json_indent': '2',
    'json_sort_keys': 'True',
    'pprint_indent': '2',
    'pprint_depth': '4',
    'yaml_flow_style': 'False'
}

config_default_dict = {
    'jira': {
        'server': 'http://localhost:8080/',
        'cookie_store': f'{os.path.join(__APP_DIR__, ".jira.cookies")}'
    },
    'confluence': {
        'server': 'http://localhost:8000/',
        'cookie_store': f'{os.path.join(__APP_DIR__, ".confluence.cookies")}'
    },
    'crowd': {
        'server': 'http://localhost:8095/crowd/',
        'cookie_store': f'{os.path.join(__APP_DIR__, ".crowd.cookies")}'
    },
    'output': {}
}

config_file = os.path.join(__APP_DIR__, 'bender.cfg')

local_config_file = os.path.join(APP_CURRENT_DIR, 'bender.cfg')

config = configparser.ConfigParser(config_defaults)
config.read_dict(config_default_dict)
config.read(config_file)

if os.path.isfile(local_config_file):
    config.read(local_config_file)

