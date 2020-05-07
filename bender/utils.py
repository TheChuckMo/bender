import base64
import configparser
import json
import os
import pickle
from json.decoder import JSONDecodeError
from pprint import pformat

import click
import requests
import yaml
from click import File
from requests.auth import HTTPBasicAuth
from requests.exceptions import ConnectionError
from requests_toolbelt.sessions import BaseUrlSession

from bender import APP_DIR, APP_CURRENT_DIR

"""configuration"""
config_defaults = {
    'cookie_store': f'{os.path.join(APP_DIR, ".cookies")}',
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
    'output': {}
}
config_file = os.path.join(APP_DIR, 'bender.cfg')
local_config_file = os.path.join(APP_CURRENT_DIR, 'bender.cfg')

config = configparser.ConfigParser(config_defaults)
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


class AppWriter:
    """App Writer"""

    output: str = config['output'].get('default_output')
    file: File = None
    section: str = 'output'
    _data: [list, dict] = None

    def __init__(self, output: str = None, section: str = None):
        if output:
            self.output = output

        if section:
            self.section = section

    def out(self, data: [dict, list], output: str = None, file=None):
        """write out."""
        if data:
            self.data = data

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
    def data(self):
        """Data to write"""
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
        """data as json"""
        return yaml.dump(self.data, default_flow_style=config[self.section].getboolean('yaml_flow_style'))


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
        """server baseUrl for connection"""
        return self._server

    @server.setter
    def server(self, server: str):
        self._server = server
        if self.session:
            self.session.base_url = server

    @property
    def password(self):
        """password for connection."""
        return base64.decodebytes(self._password).decode()

    @password.setter
    def password(self, password: str):
        self._password = base64.encodebytes(password.encode())

    def get(self, api, headers: dict = None, params: dict = None, data: dict = None, auth: bool = False,
            allow_redirects=True):
        """send http get request.

        Parameters
        ----------
        api:        str url path appended to baseUrl.
        headers:    dict of headers.
        params:     dict of url query parameters.
        data:       dict of data to send.
        auth:       bool(False) send BasicAuth.
        allow_redirects

        Returns
        -------

        """
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
        """send http delete request.

        Parameters
        ----------
        api:        str url path appended to baseUrl.
        headers:    dict of headers.
        params:     dict of url query parameters.
        auth:       bool(False) send BasicAuth.

        Returns
        -------
        ->json
        """
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
        """send http post request.

        Parameters
        ----------
        api:        str url path appended to baseUrl.
        headers:    dict of headers.
        params:     dict of url query parameters.
        data:       dict of data to send.
        auth:       bool(False) send BasicAuth.
        allow_redirects

        Returns
        -------
        ->json
        """
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
        """send http put request.

        Parameters
        ----------
        api:        str url path appended to baseUrl.
        headers:    dict of headers.
        params:     dict of url query parameters.
        data:       dict of data to send.
        auth:       bool(False) send BasicAuth.

        Returns
        -------
        ->json
        """
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
        """Always return a json response.

        Parameters
        ----------
        res:    requests response.

        Returns
        -------
        ->json
        """
        _json = None

        if res.ok:
            if res.cookies:
                self.session.cookies.update(res.cookies)
            self.cache_cookies()

            try:
                _json = res.json()
            except JSONDecodeError as err:
                SystemExit(err)

        if not _json:
            if res.ok:
                _json = json.dumps({
                    'success': self._response.ok,
                    'status code': self._response.status_code,
                    'elapsed seconds': self._response.elapsed.seconds
                })
            else:
                _json = json.dumps({
                    'ok': self._response.ok,
                    'status_code': self._response.status_code,
                    'reason': self._response.text,
                    'request-url': self._response.request.url,
                    'request-method': self._response.request.method,
                    'text': self._response.text,
                    'redirect': self._response.is_redirect,
                    'elapsed': self._response.elapsed.seconds
                })

        return _json

    def update_cookies(self, cookies: dict = None):
        """add cookie(s) to cookie jar.

        Parameters
        ----------
        cookies
        """
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

# def write_out(data: [dict, list], output: str = None):
#     """write formatted data to screen.
#
#     Parameters
#     ----------
#     data:        dict or list to print.
#     output:      format to print.
#        :pprint|yaml|json|raw:
#     """
#     if output is None:
#         output = config['output'].get('default_output')
#
#     if output is 'pretty':
#         pprint(json.dumps(data), indent=config['output'].getint('pprint_indent'),
#                depth=config['output'].getint('pprint_depth'), stream=None)
#
#     if output is 'raw':
#         click.echo(data)
#
#     if output is 'json':
#         click.echo(json.dumps(data, indent=config['output'].getint('json_indent'),
#                               sort_keys=config['output'].getboolean('json_sort_keys')))
#     elif output is 'yaml':
#         click.echo(yaml.dump(data, default_flow_style=config['output'].getboolean('yaml_flow_style')))
