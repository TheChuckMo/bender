import base64
import json
import os
import pickle
from json.decoder import JSONDecodeError

import requests
from requests.auth import HTTPBasicAuth
from requests_toolbelt.sessions import BaseUrlSession


class AppConnect:
    """App connection object.

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