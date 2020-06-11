"""bender config."""
import yaml
import os

from click.utils import open_file
from bender import __APP_NAME__, __APP_DIR__

_user_cfg_file: str = os.path.join(__APP_DIR__, f'{__APP_NAME__}.yml')
_local_cfg_file: str = os.path.join(__APP_DIR__, f'.{__APP_NAME__}.yml')


class BenderConfig:
    """Bender config class."""
    _user_file: str = _user_cfg_file
    _local_file: str = _local_cfg_file

    _user: dict = {}
    _local: dict = {}

    def __init__(self):
        self._load_user_cfg()
        self._load_local_cfg()

    def _load_user_cfg(self):
        if os.path.isfile(self._user_file):
            with open_file(self._user_file, 'r') as fh:
                self._user = yaml.safe_load(fh.read())

    def _write_user_cfg(self):
        with open_file(self._user_file, 'w') as fh:
            fh.write(yaml.safe_dump(self.user))

    def _load_local_cfg(self):
        if os.path.isfile(self._local_file):
            with open_file(self._local_file, 'r') as fh:
                self._user = yaml.safe_load(fh.read())

    def _write_local_cfg(self):
        with open_file(self._local_file, 'w') as fh:
            fh.write(yaml.safe_dump(self._local))

    @property
    def user(self):
        """global user config."""
        return self._user

    def local(self):
        """local config."""
        return self._local

