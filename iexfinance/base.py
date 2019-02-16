import os
import time

import requests

from iexfinance.utils import _init_session
from iexfinance.utils.exceptions import IEXQueryError
from iexfinance.utils.exceptions import IEXAuthenticationError as auth_error

# Data provided for free by IEX
# See https://iextrading.com/api-exhibit-a/ for additional information
# and conditions of use


class _IEXBase(object):
    """
    Base class for retrieving equities information from IEX Cloud.
    Conducts query operations including preparing and executing queries from
    the API.

    Attributes
    ----------
    retry_count: int, default 3, optional
        Desired number of retries if a request fails
    pause: float default 0.5, optional
        Pause time between retry attempts
    session: requests_cache.session, default None, optional
        A cached requests-cache session
    json_parse_int: datatype, default int, optional
        Desired integer parsing datatype
    json_parse_float: datatype, default float, optional
        Desired floating point parsing datatype
    output_format: str, default "json", optional
        Desired output format (json or pandas DataFrame). This can also be
        set using the environment variable ``IEX_OUTPUT_FORMAT``.
    token: str, optional
        Authentication token (reuqired for use with IEX Cloud)
    """
    _URLS = {
        "v1": "https://api.iextrading.com/1.0/",
        "iexcloud-beta": "https://cloud.iexapis.com/beta/",
        "iexcloud-v1": "https://cloud.iexapis.com/v1/"
    }

    _VALID_FORMATS = ('json', 'pandas')
    _VALID_CLOUD_VERSIONS = ("iexcloud-beta", "iexcloud-v1")

    def __init__(self, **kwargs):

        self.retry_count = kwargs.get("retry_count", 3)
        self.pause = kwargs.get("pause", 0.5)
        self.session = _init_session(kwargs.get("session"))
        self.json_parse_int = kwargs.get("json_parse_int")
        self.json_parse_float = kwargs.get("json_parse_float")
        self.output_format = kwargs.get("output_format",
                                        os.getenv("IEX_OUTPUT_FORMAT", 'json'))
        if self.output_format not in self._VALID_FORMATS:
            raise ValueError("Please enter a valid output format ('json' "
                             "or 'pandas').")
        self.token = kwargs.get("token")

        # Get desired API version from environment variables
        # Defaults to v1 API
        self.version = os.getenv("IEX_API_VERSION")
        if self.version in self._VALID_CLOUD_VERSIONS:
            if self.token is None:
                self.token = os.getenv('IEX_TOKEN')
            if not self.token or not isinstance(self.token, str):
                raise auth_error('The IEX Cloud API key must be provided '
                                 'either through the token variable or '
                                 'through the environmental variable '
                                 'IEX_TOKEN.')
        else:
            self.version = 'v1'

    @property
    def params(self):
        return {}

    @property
    def url(self):
        raise NotImplementedError

    def _validate_response(self, response):
        """ Ensures response from IEX server is valid.

        Parameters
        ----------
        response: requests.response
            A requests.response object

        Returns
        -------
        response: Parsed JSON
            A json-formatted response

        Raises
        ------
        ValueError
            If a single Share symbol is invalid
        IEXQueryError
            If the JSON response is empty or throws an error

        """
        if response.text == "Unknown symbol":
            raise IEXQueryError()
        try:
            json_response = response.json(
                parse_int=self.json_parse_int,
                parse_float=self.json_parse_float)
            if "Error Message" in json_response:
                raise IEXQueryError()
        except ValueError:
            raise IEXQueryError()
        return json_response

    def _execute_iex_query(self, url):
        """ Executes HTTP Request
        Given a URL, execute HTTP request from IEX server. If request is
        unsuccessful, attempt is made self.retry_count times with pause of
        self.pause in between.

        Parameters
        ----------
        url: str
            A properly-formatted url

        Returns
        -------
        response: requests.response
            Sends requests.response object to validator

        Raises
        ------
        IEXQueryError
            If problems arise when making the query
        """
        params = self.params
        params['token'] = self.token
        for i in range(self.retry_count+1):
            response = self.session.get(url=url, params=params)
            if response.status_code == requests.codes.ok:
                return self._validate_response(response)
            time.sleep(self.pause)
        return self._handle_error(response)

    def _handle_error(self, response):
        """
        Handles all responses which return an error status code
        """
        auth_msg = "The query could not be completed. Invalid auth token."

        status_code = response.status_code
        if 400 <= status_code < 500:
            if status_code == 400:
                raise auth_error(auth_msg)
            else:
                raise auth_error("The query could not be completed. "
                                 "There was a client-side error with your "
                                 "request.")
        elif 500 <= status_code < 600:
            raise auth_error("The query could not be completed. "
                             "There was a server-side error with "
                             "your request.")
        else:
            raise auth_error("The query could not be completed.")

    def _prepare_query(self):
        """ Prepares the query URL

        Returns
        -------
        url: str
            A formatted URL
        """
        return "%s%s" % (self._URLS[self.version], self.url)

    def fetch(self, fmt_p=None, fmt_j=None):
        """Fetches latest data

        Prepares the query URL based on self.params and executes the request

        Returns
        -------
        response: requests.response
            A response object
        """
        url = self._prepare_query()
        data = self._execute_iex_query(url)
        return self._output_format(data, fmt_j=fmt_j, fmt_p=fmt_p)

    def _convert_output(self, out):
        import pandas as pd
        return pd.DataFrame(out)

    def _output_format(self, out, fmt_j=None, fmt_p=None):
        """
        Output formatting handler
        """
        if self.output_format == 'pandas':
            if fmt_p is not None:
                return fmt_p(out)
            else:
                return self._convert_output(out)
        if fmt_j:
            return fmt_j(out)
        return out
