import requests

from iexfinance.utils import _init_session
from iexfinance.utils.exceptions import IEXQueryError
import time
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
    """
    # Base URL
    _IEX_API_URL = "https://api.iextrading.com/1.0/"

    def __init__(self, symbolList=None, retry_count=3, pause=0.001,
                 session=None):
        """ Initialize the class

        Keyword Arguments:
            symbolList: A symbol or list of symbols
            session: A cached requests session
            retry_count: Desired number of retries if a request fails
            pause: Pause time in between retry attempts
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

        Positional Arguments:
            response: A request object

        """
        if response.text == "Unknown symbol":
            raise ValueError("Invalid Symbol")
        json_response = response.json()
        if not json_response:
            raise IEXQueryError()
        elif "Error Message" in json_response:
            raise IEXQueryError()
        return json_response

    def _execute_iex_query(self, url):
        """
        Given a URL, execute HTTP request from IEX server. If request is
        unsuccessful, attempt is made self.retry_count times with pause of
        self.pause in between.

        Positional Arguments:
            url: A properly-formatted url

        """
        pause = self.pause
        for i in range(self.retry_count+1):

            response = self.session.get(url=url)
            if response.status_code == requests.codes.ok:
                return self._validate_response(response)
            time.sleep(pause)
        raise IEXQueryError()

    def _prepare_query(self):
        """
        Prepares the query URL
        """
        params = "?" + "&".join(
            "{}={}".format(*i) for i in self.params.items())
        url = self._IEX_API_URL + self.url + params
        return url

    def fetch(self):
        """
        Fetches latest data
        """
        url = self._prepare_query()
        response = self._execute_iex_query(url)
        return response
