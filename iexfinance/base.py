import time

import requests

from iexfinance.utils import _init_session
from iexfinance.utils.exceptions import IEXQueryError

# Data provided for free by IEX
# Data is furnished in compliance with the guidelines promulgated in the IEX
# API terms of service and manual
# See https://iextrading.com/api-exhibit-a/ for additional information
# and conditions of use


class _IEXBase(object):
    """
    Base class for retrieving equities information from the IEX Finance API.
    Inherited by Stock and Market Readers, and conducts query operations
    including preparing and executing queries from the API.

    Attributes
    ----------
    retry_count: int, default 3, optional
        Desired number of retries if a request fails
    pause: float, default 0.001, optional
        Pause time between retry attempts
    session: requests_cache.session, default None, optional
        A cached requests-cache session
    """
    # Base URL
    _IEX_API_URL = "https://api.iextrading.com/1.0/"

    def __init__(self, *args, **kwargs):
        """ Initialize the class

        Parameters
        ----------
        retry_count: int
            Desired number of retries if a request fails
        pause: float default 0.001, optional
            Pause time between retry attempts
        session: requests_cache.session, default None, optional
            A cached requests-cache session
        """
        self.retry_count = kwargs.pop("retry_count", 3)
        self.pause = kwargs.pop("pause", 0.001)
        self.session = _init_session(kwargs.pop("session", None))

    @property
    def params(self):
        return {}

    @staticmethod
    def _validate_response(response):
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
        json_response = response.json()
        if "Error Message" in json_response:
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
        pause = self.pause
        for i in range(self.retry_count+1):
            response = self.session.get(url=url, params=self.params)
            if response.status_code == requests.codes.ok:
                return self._validate_response(response)
            time.sleep(pause)
        raise IEXQueryError()

    def _prepare_query(self):
        """ Prepares the query URL

        Returns
        -------
        url: str
            A formatted URL
        """
        url = self._IEX_API_URL + self.url
        return url

    def fetch(self):
        """Fetches latest data

        Prepares the query URL based on self.params and executes the request

        Returns
        -------
        response: requests.response
            A response object
        """
        url = self._prepare_query()
        return self._execute_iex_query(url)
