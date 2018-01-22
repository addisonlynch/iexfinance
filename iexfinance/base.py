import sys

import requests

from iexfinance.utils.exceptions import (IEXSymbolError, IEXQueryError)

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

    def __init__(self, *args, **kwargs):
        """ Initialize the class

        Keyword Arguments:
            session: A cached requests session
        """
        self.session = kwargs.pop("session", requests.Session())

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
        Given a URL, execute HTTP request from IEX server. Raises
        various exceptions if problems arise

        Positional Arguments:
            url: A properly-formatted url

        """
        try:
            r = self.session.get(url=url)
            r.raise_for_status()
        except requests.exceptions.Timeout:
            # setup for retry loop
            pass
        except requests.exceptions.TooManyRedirects:
            # tell user bad url
            pass
        except requests.exceptions.ConnectionError:
            raise IEXQueryError()
        except requests.exceptions.RequestException:
            raise IEXSymbolError(self.symbolList[0])
        except requests.exceptions.HTTPError:
            raise IEXSymbolError(self.symbolList[0])
        return self._validate_response(r)

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
