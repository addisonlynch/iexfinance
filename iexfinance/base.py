import time

import requests

from iexfinance.utils import _init_session
from iexfinance.utils.exceptions import IEXQueryError

# Data provided for free by IEX
# See https://iextrading.com/api-exhibit-a/ for additional information
# and conditions of use


class _IEXBase(object):
    """
    Base class for retrieving equities information from the IEX Finance API.
    Inherited by Stock and Market Readers, and conducts query operations
    including preparing and executing queries from the API.
    """
    # Base URL
    _IEX_API_URL = "https://api.iextrading.com/1.0/"

    def __init__(self, **kwargs):
        """ Initialize the class

        Parameters
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
            Desired output format (json or pandas DataFrame)
        """
        self.retry_count = kwargs.get("retry_count", 3)
        self.pause = kwargs.get("pause", 0.5)
        self.session = _init_session(kwargs.get("session"))
        self.json_parse_int = kwargs.get("json_parse_int")
        self.json_parse_float = kwargs.get("json_parse_float")
        self.output_format = kwargs.get("output_format", 'json')

    @property
    def params(self):
        return {}

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
        for i in range(self.retry_count+1):
            response = self.session.get(url=url, params=self.params)
            if response.status_code == requests.codes.ok:
                return self._validate_response(response)
            time.sleep(self.pause)
        raise IEXQueryError()

    def _prepare_query(self):
        """ Prepares the query URL

        Returns
        -------
        url: str
            A formatted URL
        """
        return "%s%s" % (self._IEX_API_URL, self.url)

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
            if fmt_p:
                return fmt_p(out)
            else:
                return self._convert_output(out)
        if fmt_j:
            return fmt_j(out)
        return out
