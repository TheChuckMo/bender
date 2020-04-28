import requests
import pickle
import click
import configparser
import os
import base64
from urllib.parse import urljoin


# read configuration file
config = configparser.ConfigParser()
config_file = os.path.join(click.get_app_dir('bender'), 'config.ini')
config.read(config_file)
# print('config file: {}'.format(config_fi

cookie_store = config.get('settings', 'cookie_store', fallback=os.path.join(click.get_app_dir('bender'), '.cookie_store.pickle'))


class AppConnect():
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
        'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
        'X-Atlassian-Token': "no-check"
    }
    no_check_headers = {
        'X-Atlassian-Token': "no-check"
    }

    def __init__(self, server: str, username: str = None, password: str = None, session: requests.session = None):
        self.server = server
        self.username = username
        self.password = password

        if session is None:
            self.session = requests.session()

        if username and password:
            self.session.auth = (username, password)

    @property
    def password(self):
        return base64.decodebytes(self._password).decode()

    @password.setter
    def password(self, password: str):
        self._password = base64.encodebytes(password.encode())

    def get_json(self, api):
        url = urljoin(self.server, api)
        self.session.headers.update(self.json_headers)

        self._response = self.session.get(url)

        try:
            return self._response.json()
        except:
            self._response.raise_for_status()


def connect(username, password):
    req = requests.session()
    req.headers.update({'Content-Type': 'application/json'})
    # req.auth = (username, password)
    return req