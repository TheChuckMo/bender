import os

import click
import pkg_resources

APP_NAME = 'bender'

APP_DIR = click.get_app_dir(APP_NAME, force_posix=True)
if not os.path.isdir(APP_DIR):
    os.mkdir(APP_DIR)

APP_VERSION = pkg_resources.get_distribution(APP_NAME).version
