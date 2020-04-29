import base64
import configparser
import json
import os
import pickle
from urllib.parse import urljoin

import click
import requests
import yaml

"""configuration"""
config = configparser.ConfigParser()
config_file = os.path.join(click.get_app_dir('bender'), 'config.ini')
config.read(config_file)

cookie_store = config.get('settings', 'cookie_store',
                          fallback=os.path.join(click.get_app_dir('bender'), '.cookies.dat'))


def write_out(data: [dict, list], output: str = 'yaml'):
    if output is 'json':
        print(json.dumps(data, indent=2, sort_keys=True))
    else:
        print(yaml.dump(data, default_flow_style=False))


class AppConnect:
    """App Connection"""
    server: str
    username: str
    _password: str
    session: requests.session
    _response: requests

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

    def __init__(self, server: str, username: str = None, password: str = None, session: requests.session = None):
        self.server = server
        self.username = username
        self.password = password

        if session is None:
            self.session = requests.session()

        if username and password:
            self.session.auth = (username, password)

        self.reload_cookies()

    @property
    def password(self):
        return base64.decodebytes(self._password).decode()

    @password.setter
    def password(self, password: str):
        self._password = base64.encodebytes(password.encode())

    def get_json(self, api, params: dict = None, **kwargs):
        url = urljoin(self.server, api)
        self.session.headers.update(self.json_headers)

        self._response = self.session.get(url, params=params, **kwargs)

        self.cache_cookies()

        try:
            return self._response.json()
        except:
            # TODO: capture known status codes!
            # TODO: move raise_for_status to a finally clause
            self._response.raise_for_status()

    def post(self, api: str, params: dict = None, data: dict = None, **kwargs):
        url = urljoin(self.server, api)
        self.session.headers.update(self.json_headers)

        self._response = self.session.post(url, params=params, data=data, **kwargs)

        self.cache_cookies()

        try:
            return self._response.json()
        except:
            # TODO: capture known status codes!
            # TODO: move raise_for_status to a finally clause
            self._response.raise_for_status()

    def cache_cookies(self):
        """cache cookies to file"""
        if self.session.cookies:
            with open(cookie_store, 'wb') as f:
                pickle.dump(self.session.cookies, f)

    def reload_cookies(self):
        """reload cookies from file"""
        if os.path.isfile(cookie_store):
            with open(cookie_store, 'rb') as f:
                self.session.cookies = pickle.load(f)


def connect(username, password):
    req = requests.session()
    req.headers.update({'Content-Type': 'application/json'})
    # req.auth = (username, password)
    return req
