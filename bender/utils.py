import base64
import configparser
import json
import os
import pickle
from urllib.parse import urljoin
from requests.exceptions import ConnectionError
from json.decoder import JSONDecodeError

import click
import requests
import yaml
import json

from bender import APP_NAME

"""configuration"""
config_defaults = {
    'jira': {
        'server': 'http://localhost:8080',
        'cookie_store': f'{os.path.join(click.get_app_dir(APP_NAME), ".jira.cookies")}'
    },
    'confluence': {
        'server': 'http://localhost:8000',
        'cookie_store': f'{os.path.join(click.get_app_dir(APP_NAME), ".confluence.cookies")}'
    },
    'crowd': {
        'server': 'http://localhost:8095',
        'cookie_store': f'{os.path.join(click.get_app_dir(APP_NAME), ".crowd.cookies")}'
    },
    'DEFAULTS': {
        'cookie_store': f'{os.path.join(click.get_app_dir(APP_NAME), ".cookies")}'
    },
    'output': {
        'json_indent': '2',
        'json_sort_keys': 'True',
        'yaml_flow_style': 'False',
        'default_output': 'yaml'
    }
}
config = configparser.ConfigParser()
config_file = os.path.join(click.get_app_dir(APP_NAME), 'config.ini')
config.read_dict(config_defaults)
config.read(config_file)


def write_out(data: [dict, list], output: str = None):
    """write data to screen"""
    if not output:
        output = config['output']['default_output']

    if output is 'raw':
        click.echo(data)

    if output is 'json':
        click.echo(json.dumps(data, indent=config['output'].getint('json_indent'),
                              sort_keys=config['output'].getboolean('json_sort_keys')))
    elif output is 'yaml':
        click.echo(yaml.dump(data, default_flow_style=config['output'].getboolean('yaml_flow_style')))


class AppConnect:
    """App Connection"""
    server: str
    username: str
    _password: str
    session: requests.session
    _response: requests
    cookie_store: os.path = f'{os.path.join(click.get_app_dir(APP_NAME), ".cookies.dat")}'

    json_headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    form_headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Atlassian-Token': 'no-check'
    }
    no_check_headers = {
        'X-Atlassian-Token': 'no-check'
    }

    def __init__(self, server: str, username: str = None, password: str = None, cookie_store: os.path = None,
                 session: requests.session = None, headers: dict = None):
        self.server = server

        if session:
            self.session = session
        else:
            self.session = requests.session()

        if username:
            self.username = username

        if password:
            self.password = password

        if cookie_store:
            self.cookie_store = cookie_store

        if username and password:
            self.session.auth = (username, password)

        if headers:
            self.session.headers.update(headers)

        self.reload_cookies()

    @property
    def password(self):
        return base64.decodebytes(self._password).decode()

    @password.setter
    def password(self, password: str):
        self._password = base64.encodebytes(password.encode())

    def delete(self, api, headers: dict = None, **kwargs):
        url = urljoin(self.server, api)

        self.session.headers.update(self.no_check_headers)

        try:
            self._response = self.session.delete(url, headers=headers, **kwargs)
        except ConnectionError:
            return {'error': f'failure connecting to {self.server}.'}

        if self._response.ok:
            self.cache_cookies()
        resp = {
            'status_code': self._response.status_code,
            'url': self._response.url,
            'reason': self._response.reason
        }

        return resp

    # def get_form(self, api, params: dict = None, data: dict = None, **kwargs):
    #     url = urljoin(self.server, api)
    #     resp: dict = {}
    #
    #     self.session.headers.update(self.form_headers)
    #
    #     try:
    #         self._response = self.session.get(url, params=params, data=data, **kwargs)
    #     except ConnectionError:
    #         return {'error': f'failure connecting to {self.server}.'}
    #
    #     if self._response.ok:
    #         self.cache_cookies()
    #         resp = self._response.text
    #     else:
    #         resp = {
    #             'status_code': self._response.status_code,
    #             'url': self._response.url,
    #             'reason': self._response.reason
    #         }
    #
    #     return resp

    def get_json(self, api, params: dict = None, data: dict = None, headers: dict = None, **kwargs):
        url = urljoin(self.server, api)
        resp: dict = {}

        try:
            self._response = self.session.get(url, params=params, data=data, headers=headers, **kwargs)
        except ConnectionError:
            return {'error': f'failure connecting to {self.server}.'}

        if self._response.ok:
            self.cache_cookies()
            resp = self._response.json()
        else:
            resp = {
                'status_code': self._response.status_code,
                'url': self._response.url,
                'reason': self._response.reason
            }

        return resp

    # def put_json(self, api: str, params: dict = None, data: dict = None, headers: dict = None, **kwargs):
    #     url = urljoin(self.server, api)
    #     resp: dict = {}
    #     self.session.headers.update(self.json_headers)
    #
    #     try:
    #         self._response = self.session.post(url, params=params, data=data, headers=headers, **kwargs)
    #     except ConnectionError:
    #         return {'error': f'failure connecting to {self.server}.'}
    #
    #     if self._response.ok:
    #         self.cache_cookies()
    #         resp = self._response.json()
    #     else:
    #         resp = {
    #             'status_code': self._response.status_code,
    #             'url': self._response.url,
    #             'reason': self._response.reason,
    #         }
    #
    #     return resp

    # def post_form(self, api: str, params: dict = None, data: dict = None, **kwargs):
    #     url = urljoin(self.server, api)
    #     resp: dict = {}
    #     self.session.headers.update(self.form_headers)
    #
    #     try:
    #         self._response = self.session.post(url, params=params, data=data, **kwargs)
    #     except ConnectionError:
    #         return {'error': f'failure connecting to {self.server}.'}
    #
    #     if self._response.ok:
    #         self.cache_cookies()
    #         resp = {
    #             'status_code': self._response.status_code,
    #             'url': self._response.url,
    #             'reason': self._response.reason,
    #             'text': self._response.text
    #         }
    #     else:
    #         resp = {
    #             'status_code': self._response.status_code,
    #             'url': self._response.url,
    #             'reason': self._response.reason
    #         }
    #
    #     return resp

    def post(self, api: str, params: dict = None, data: dict = None, json: dict = None, headers: dict = None, **kwargs):
        url = urljoin(self.server, api)
        resp: dict = {}

        try:
            self._response = self.session.post(url, params=params, data=data, json=json, headers=headers, **kwargs)
        except ConnectionError:
            return {'error': f'failure connecting to {self.server}.'}

        if self._response.ok:
            self.cache_cookies()

            try:
                resp = self._response.json()
            except JSONDecodeError:
                pass

        if not resp:
            resp = {
                'status_code': self._response.status_code,
                'url': self._response.url,
                'reason': self._response.reason
            }

        return resp

    def cache_cookies(self):
        """cache cookies to file"""
        if self.session.cookies:
            with open(self.cookie_store, 'wb') as f:
                pickle.dump(self.session.cookies, f)

    def reload_cookies(self):
        """reload cookies from file"""
        if os.path.isfile(self.cookie_store):
            with open(self.cookie_store, 'rb') as f:
                self.session.cookies = pickle.load(f)
