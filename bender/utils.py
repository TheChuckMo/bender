import base64
import configparser
import json
import os
import pickle
from json.decoder import JSONDecodeError

import click
import requests
import yaml
from requests.auth import HTTPBasicAuth
from requests.exceptions import ConnectionError
from requests_toolbelt.sessions import BaseUrlSession

from bender import APP_DIR, APP_CURRENT_DIR

"""configuration"""
config_defaults = {
    'cookie_store': f'{os.path.join(APP_DIR, ".cookies")}'
}
config_default_dict = {
    'jira': {
        'server': 'http://localhost:8080/',
        'cookie_store': f'{os.path.join(APP_DIR, ".jira.cookies")}'
    },
    'confluence': {
        'server': 'http://localhost:8000/',
        'cookie_store': f'{os.path.join(APP_DIR, ".confluence.cookies")}'
    },
    'crowd': {
        'server': 'http://localhost:8095/crowd/',
        'cookie_store': f'{os.path.join(APP_DIR, ".crowd.cookies")}'
    },
    'output': {
        'json_indent': '2',
        'json_sort_keys': 'True',
        'yaml_flow_style': 'False',
        'default_output': 'yaml'
    }
}
config_file = os.path.join(APP_DIR, 'bender.cfg')
local_config_file = os.path.join(APP_CURRENT_DIR, 'bender.cfg')

config = configparser.ConfigParser()
config.read_dict(config_default_dict)
config.read(config_file)
if os.path.isfile(local_config_file):
    config.read(local_config_file)

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


def write_out(data: [dict, list], output: str = None):
    """write formatted data to screen.

    Parameters
    ----------
    data:        dict or list to print.
    output:      format to print.
    """
    if output is None:
        output = config['output']['default_output']

    if output is 'raw':
        click.echo(data)

    if output is 'json':
        click.echo(json.dumps(data, indent=config['output'].getint('json_indent'),
                              sort_keys=config['output'].getboolean('json_sort_keys')))
    elif output is 'yaml':
        click.echo(yaml.dump(data, default_flow_style=config['output'].getboolean('yaml_flow_style')))


class AppConnect:
    """App Connection

    A wrapper for requests BaseUrlSession to hold Atlassian keys across command runs.

    Parameters
    ----------
    server:          base url of app server.
    username:        username for connection.
    password:        password for connection.
    cookie_store:    path to file for cookie_store.
    session_headers: default headers added to every call.
    """
    _server: str
    username: str
    _password: str
    session: BaseUrlSession = None
    auth: HTTPBasicAuth = None
    _response: requests = None
    cookie_store: os.path = None

    def __init__(self, server: str, username: str = None, password: str = None, cookie_store: os.path = None,
                 session_headers: dict = None) -> None:
        self.server = server
        self.session = BaseUrlSession(base_url=server)

        if username:
            self.username = username

        if password:
            self.password = password

        if cookie_store:
            self.cookie_store = cookie_store

        if username and password:
            self.auth = HTTPBasicAuth(self.username, self.password)

        if session_headers:
            self.session.headers.update(session_headers)

        self.reload_cookies()

    @property
    def server(self):
        return self._server

    @server.setter
    def server(self, server: str):
        self._server = server
        if self.session:
            self.session.base_url = server

    @property
    def password(self):
        return base64.decodebytes(self._password).decode()

    @password.setter
    def password(self, password: str):
        self._password = base64.encodebytes(password.encode())

    def get(self, api, headers: dict = None, params: dict = None, data: dict = None, auth: bool = False,
            allow_redirects=True):
        # url = urljoin(self.server, api)
        url = api

        try:
            self._response = self.session.get(url, headers=headers, params=params, data=data,
                                              auth=self.auth if auth else None, allow_redirects=allow_redirects)
            self._response.raise_for_status()
        except requests.exceptions.ConnectionError as err:
            raise SystemExit(err)
        except requests.exceptions.Timeout as err:
            raise SystemExit(err)
        except requests.exceptions.TooManyRedirects as err:
            raise SystemExit(err)
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        return self.json_response(self._response)

    def delete(self, api, headers: dict = None, params=None, auth: bool = False):
        # url = urljoin(self.server, api)
        url = api

        try:
            self._response = self.session.delete(url, headers=headers, params=params, auth=self.auth if auth else None)
            self._response.raise_for_status()
        except requests.exceptions.ConnectionError as err:
            raise SystemExit(err)
        except requests.exceptions.Timeout as err:
            raise SystemExit(err)
        except requests.exceptions.TooManyRedirects as err:
            raise SystemExit(err)
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        return self.json_response(self._response)

    def post(self, api: str, headers: dict = None, params: dict = None, data: dict = None, auth: bool = False,
             allow_redirects: bool = True):
        # url = urljoin(self.server, api)
        url = api

        try:
            self._response = self.session.post(url, headers=headers, params=params, data=data,
                                               auth=self.auth if auth else None, allow_redirects=allow_redirects)
            # self._response.raise_for_status()
        except requests.exceptions.ConnectionError as err:
            raise SystemExit(err)
        except requests.exceptions.Timeout as err:
            raise SystemExit(err)
        except requests.exceptions.TooManyRedirects as err:
            raise SystemExit(err)
        # except requests.exceptions.HTTPError as err:
        #     raise SystemExit(err)

        return self.json_response(self._response)

    def put(self, api: str, headers: dict = None, params: dict = None, data: dict = None, auth: bool = False):
        # url = urljoin(self.server, api)
        url = api

        try:
            self._response = self.session.put(url, headers=headers, params=params, data=data,
                                              auth=self.auth if auth else None)
            self._response.raise_for_status()
        except requests.exceptions.ConnectionError as err:
            raise SystemExit(err)
        except requests.exceptions.Timeout as err:
            raise SystemExit(err)
        except requests.exceptions.TooManyRedirects as err:
            raise SystemExit(err)
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        return self.json_response(self._response)

    def json_response(self, res: requests):
        _json = None

        if res.ok:
            if res.cookies:
                self.session.cookies.update(res.cookies)
            self.cache_cookies()

            try:
                _json = res.json()
            except JSONDecodeError as err:
                SystemExit()

        if not _json:
            if res.ok:
                _json = {
                    'ok': self._response.ok,
                    'status-code': self._response.status_code
                }
            else:
                _json = {
                    'ok': self._response.ok,
                    'status_code': self._response.status_code,
                    'reason': self._response.text,
                    'request-url': self._response.request.url,
                    'request-method': self._response.request.method,
                    'text': self._response.text,
                    'redirect': self._response.is_redirect,
                    'elapsed': self._response.elapsed.seconds
                }

        return _json

    def update_cookies(self, cookies: dict = None):
        """add cookie(s) to cookie jar."""
        self.session.cookies.update(cookies)
        self.cache_cookies()

    def cache_cookies(self):
        """cache cookies to file."""
        if self.session.cookies:
            with open(self.cookie_store, 'wb') as f:
                pickle.dump(self.session.cookies, f)

    def reload_cookies(self):
        """reload cookies from file."""
        if os.path.isfile(self.cookie_store):
            with open(self.cookie_store, 'rb') as f:
                self.session.cookies.update(pickle.load(f))
