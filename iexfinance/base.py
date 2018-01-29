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
    """ IEX Base Class
    Base class for retrieving equities information from the IEX Finance API.
    Inherited by Stock and Market Readers, and conducts query operations
    including preparing and executing queries from the API.

    Attributes
    ----------
    retry_count: int
        Desired number of retries if a request fails
    pause: float
        Pause time between retry attempts
    session: requests.session
        A cached requests-cache session

    Methods
    -------
    fetch()
        Retrieve data from IEX API
    """
    # Base URL
    _IEX_API_URL = "https://api.iextrading.com/1.0/"

    def __init__(self, retry_count=3, pause=0.001,
                 session=None):
        """ Initialize the class

        Parameters
        ----------
        retry_count: int
            Desired number of retries if a request fails
        pause: float
            Pause time between retry attempts
        session: requests.session
            A cached requests-cache session

        """
        self.retry_count = retry_count
        self.pause = pause
        self.session = _init_session(session)

    @property
    def url(self):
        # Must be overridden in subclass
        raise NotImplementedError

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
        response: JSON
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

            response = self.session.get(url=url)
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
        params = "?" + "&".join(
            "{}={}".format(*i) for i in self.params.items())
        url = self._IEX_API_URL + self.url + params
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
        response = self._execute_iex_query(url)
        return response
