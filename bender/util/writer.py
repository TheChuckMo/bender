import json
from pprint import pformat

import click
import yaml
from click import File
from jsonpath_ng.ext import parse

from bender import config


class AppWriter:
    """App Writer"""
    FORMATS: list = ['pretty', 'json', 'yaml', 'raw']
    output: str = config['output'].get('default_output')
    file: File = None
    section: str = 'output'
    _json_filter: str = None
    _data: [list, dict] = None

    def __init__(self, output: str = None, config_section: str = None):
        if output:
            self.output = output

        if config_section:
            self.section = config_section

    def out(self, data: [dict, list], output: str = None, json_filter: str = None, file=None):
        """write out."""
        if data:
            self.data = data

        if json_filter:
            self.json_filter = json_filter

        if output:
            self.output = output

        if file:
            self.file = file

        if self.output is 'pretty':
            click.echo(self.pretty, file=file)

        if self.output is 'json':
            click.echo(self.json, file=file)

        if self.output is 'yaml':
            click.echo(self.yaml, file=file)

        if self.output is 'raw':
            click.echo(self.data, file=file)

    @property
    def json_filter(self):
        """Data filter for output."""
        if self._json_filter:
            return parse(self._json_filter)

        return False

    @json_filter.setter
    def json_filter(self, json_filter: str):
        self._json_filter = json_filter

    @property
    def data(self):
        """Data to write."""
        if self.json_filter:
            _data = self.json_filter.find(self._data)
            return _data

        return self._data

    @data.setter
    def data(self, data: [list, dict] = None):
        self._data = data

    @property
    def pretty(self):
        """data as pretty"""
        return pformat(self.data, indent=config[self.section].getint('pprint_indent'),
                       depth=config[self.section].getint('pprint_depth'))

    @property
    def json(self):
        """data as json"""
        return json.dumps(self.data, indent=config[self.section].getint('json_indent'),
                          sort_keys=config[self.section].getboolean('json_sort_keys'))

    @property
    def yaml(self):
        """data as yaml"""
        return yaml.dump(self.data, default_flow_style=config[self.section].getboolean('yaml_flow_style'))