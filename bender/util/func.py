import os

import yaml
from click.utils import open_file

_data_dir = '/data'
_local_env_file = os.path.join(_data_dir, '.smoenv.yml')
_site_env_file = os.path.join(_data_dir, '.smo_sites.yml')


def get_local_env_data(file: str = _local_env_file) -> dict:
    """get local env data from file."""
    _data: dict = {}
    if os.path.isfile(file):
        with open_file(file, 'r') as fh:
            _data = yaml.safe_load(fh.read())

    return _data


def get_site_env_data(file: str = _site_env_file) -> dict:
    """get site env data from file."""
    _data: dict = {}
    if os.path.isfile(file):
        with open_file(file, 'r') as fh:
            _data = yaml.safe_load(fh.read())

    return _data