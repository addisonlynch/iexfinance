from .base import _IEXBase
from iexfinance.utils import _handle_lists

# Data provided for free by IEX
# See https://iextrading.com/api-exhibit-a/ for additional information
# and conditions of use


class Market(_IEXBase):
    """
    Base class for obtaining data from the market endpoints
    of IEX.
    """
    def __init__(self, symbols=None, **kwargs):
        """ Initialize the class

        Parameters
        ----------
        symbols : string, array-like object (list, tuple, Series), or DataFrame
            Desired symbols for retrieval
        output_format: str, default 'json', optional
            Desired output format (json or pandas)
        kwargs:
            Additional request options (see base class)
        """
        if symbols:
            self.symbols = _handle_lists(symbols)
            if len(self.symbols) > self.symbol_limit:
                raise ValueError("At most " + str(self.symbol_limit) +
                                 "symbols may be entered at once.")
        else:
            if self.symbol_required:
                raise ValueError("Please input a symbol or list of symbols.")
            self.symbols = []
        super(Market, self).__init__(**kwargs)

    @property
    def params(self):
        if self.symbols:
            return {"symbols": ",".join(self.symbols)}
        else:
            return {}

    @property
    def symbol_required(self):
        """Property to determine if given endpoint requires a symbol list as
        a parameter
        """
        return False

    @property
    def symbol_limit(self):
        raise NotImplementedError


class TOPS(Market):
    """ Class to retrieve IEX TOPS data

    Near-real time aggregated bid and offer positions. IEX's aggregated best
    quoted bid and offer position for all securities on IEX's displayed limit
    order book.

    Reference
    ---------
    https://iextrading.com/developer/docs/#TOPS
    """
    @property
    def url(self):
        return "tops"

    @property
    def symbol_limit(self):
        return 10


class Last(Market):
    """ Class to retrieve Last quote data

    Last provides trade data for executions on IEX. Provides last sale price,
    size and time.

    Reference
    ---------
    https://iextrading.com/developer/docs/#Last
    """
    @property
    def url(self):
        return "tops/last"

    @property
    def symbol_limit(self):
        return 10


class DEEP(Market):
    """ Class to retrieve DEEP order book data


    Real-time depth of book quotations direct from IEX. Returns aggregated
    size of resting displayed orders at a price and side. Does not indicate
    the size or number of individual orders at any price level. Non-displayed
    orders and non-displayed portions of reserve orders are not counted.
    Also provides last trade price and size information. Routed executions
    are not reported.

    Reference
    ---------
    https://iextrading.com/developer/docs/#DEEP
    """
    @property
    def url(self):
        return "deep"

    def _convert_output(self, out):
        return out

    @property
    def symbol_required(self):
        return True

    @property
    def symbol_limit(self):
        return 1


class Book(Market):
    """ Class to retrieve IEX DEEP Book data

    Retrieve IEX's bids and asks for given symbols

    Reference
    ---------
    https://iextrading.com/developer/docs/#Book

    Notes
    -----
    Will return empty outside of trading hours
    """
    def _convert_output(self, out):
        return out

    @property
    def url(self):
        return "deep/book"

    @property
    def symbol_required(self):
        return True

    @property
    def symbol_limit(self):
        return 10
