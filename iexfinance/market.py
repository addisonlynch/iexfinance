from .base import _IEXBase
from iexfinance.utils.exceptions import IEXQueryError

import pandas as pd

# Data provided for free by IEX
# Data is furnished in compliance with the guidelines promulgated in the IEX
# API terms of service and manual
# See https://iextrading.com/api-exhibit-a/ for additional information
# and conditions of use


class Market(_IEXBase):
    """
    Base class for obtaining date from the market endpoints
    of IEX. Subclass of _IEXBase, subclassed by various.
    """
    def __init__(self, symbolList=None, outputFormat='json', retry_count=3,
                 pause=0.001, session=None):
        """ Initializes the class

        Keyword Arguments:
            symbolList: A symbol or list of symbols
            outputFormat: Desired output format (json or pandas)
            retry_count: see base class
            pause: see base class
            session: see base class
        """
        if symbolList is None:
            if self.symbol_required:
                raise ValueError("Please input a symbol or list of symbols.")
            self.syms = False
        else:
            self.syms = True
            if isinstance(symbolList, str):
                self.symbolList = [symbolList]
            elif len(symbolList) in range(0, 10):
                self.symbolList = symbolList
        self.outputFormat = outputFormat
        super(Market, self).__init__(symbolList, retry_count, pause, session)

    @property
    def params(self):
        if self.syms is True:
            return {"symbols": ",".join(self.symbolList)}
        else:
            return {}

    def _output_format(self, response):
        if self.outputFormat == 'json':
            return response
        elif self.outputFormat == 'pandas' and self.acc_pandas:
            try:
                df = pd.DataFrame(response)
                return df
            except ValueError as e:
                raise IEXQueryError()
        elif self.acc_pandas is False:
            raise ValueError("Pandas not accepted for this function.")
        else:
            raise ValueError("Please input valid output format")

    def fetch(self):
        response = super(Market, self).fetch()
        return self._output_format(response)

    @property
    def acc_pandas(self):
        """Property to determine if given endpoint can be formatted as a
        dataframe
        """
        return True

    @property
    def symbol_required(self):
        """Property to determine if given endpoint requires a symbol list as
        a parameter
        """
        return False


class TOPS(Market):
    """
    Near-real time aggregated bid and offer positions

    Notes
    -----
    IEX's aggregated best quoted bid and offer position for all securities
    on IEX's displayed limit order book.
    """
    @property
    def url(self):
        return "tops"


class Last(Market):
    """
    Information of executions on IEX

    Notes
    -----
    Last provides trade data for executions on IEX. Provides last sale price,
    size and time.
    """
    @property
    def url(self):
        return "tops/last"


class DEEP(Market):
    """
    Retrieve order book data from IEX

    Notes
    -----
    Real-time depth of book quotations direct from IEX. Returns aggregated
    size of resting displayed orders at a price and side. Does not indicate
    the size or number of individual orders at any price level. Non-displayed
    orders and non-displayed portions of reserve orders are not counted.
    Also provides last trade price and size information. Routed executions
    are not reported.
    """
    @property
    def url(self):
        return "deep"

    @property
    def acc_pandas(self):
        return False

    @property
    def symbol_required(self):
        return True


class Book(Market):
    """
    Retrieve IEX's bids and asks for given symbols

    Notes
    -----
    Will return empty outside of trading hours
    """
    @property
    def url(self):
        return "deep/book"

    @property
    def symbol_required(self):
        return True
