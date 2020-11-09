import datetime as dt
from datetime import datetime, timedelta

from iexfinance.base import _IEXBase
from iexfinance.utils import _handle_lists, _sanitize_dates


class Market(_IEXBase):
    """
    Base class for obtaining data from the market endpoints
    of IEX.
    """

    def __init__(self, symbols=None, **kwargs):
        """
        Parameters
        ----------
        symbols : string, array-like object (list, tuple, Series), or DataFrame
            Desired symbols for retrieval
        kwargs:
            Additional request options (see base class)
        """
        if symbols:
            self.symbols = _handle_lists(symbols)
            if len(self.symbols) > self.symbol_limit:
                raise ValueError(
                    "At most "
                    + str(self.symbol_limit)
                    + "symbols may be entered at once."
                )
        else:
            if self.symbol_required:
                raise ValueError("Please input a symbol or list of symbols.")
            self.symbols = []
        super(Market, self).__init__(**kwargs)

    @property
    def output_format(self):
        return "json"

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
    """Class to retrieve IEX TOPS data

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
    """Class to retrieve Last quote data

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
    """Class to retrieve DEEP order book data


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
    """Class to retrieve IEX DEEP Book data

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


class Stats(_IEXBase):
    """
    Base class for obtaining date from the IEX Stats endpoints
    of IEX.

    Reference: https://iextrading.com/developer/docs/#iex-stats
    """

    @property
    def url(self):
        return "stats"

    @staticmethod
    def _validate_dates(start, end):
        now = datetime.now()
        if isinstance(start, datetime):
            # Ensure start range is within 4 years
            if start.year < (now.year - 4) or start > now:
                raise ValueError(
                    "start: retrieval period must begin from "
                    + str(now.year - 4)
                    + " until now"
                )

    @property
    def output_format(self):
        return "json"


class IntradayReader(Stats):
    """
    Class for obtaining data from the Intraday endpoint of IEX Stats

    Reference: https://iextrading.com/developer/docs/#intraday
    """

    @property
    def url(self):
        return "stats/intraday"


class RecentReader(Stats):
    """
    Class for obtaining data from the Recent endpoint of IEX Stats

    Reference: https://iextrading.com/developer/docs/#recent
    """

    @property
    def url(self):
        return "stats/recent"


class RecordsReader(Stats):
    """
    Class for obtaining data from the Records endpoint of IEX Stats

    Reference: https://iextrading.com/developer/docs/#records
    """

    @property
    def url(self):
        return "stats/records"


class DailySummaryReader(Stats):
    """
    Class for obtaining data from the Historical Daily endpoint of IEX Stats

    Attributes
    ----------
    start : string, int, date, datetime, Timestamp
        Starting date. Parses many different kind of date
        representations (e.g., 'JAN-01-2010', '1/1/10', 'Jan, 1, 1980').
        Defaults to 15 years before current date.
    end : string, int, date, datetime, Timestamp
        Ending date
    last: int
        Period between 1 and 90 days, overrides dates
    kwargs:
        Additional request parameters (see base class)


    Reference
    ---------
    https://iextrading.com/developer/docs/#historical-daily

    """

    def __init__(self, start=None, end=None, last=None, **kwargs):
        self.curr_date = start
        self.last = last
        # if no start specified, use 4 years from previous date to override
        # _sanitize_dates
        if start is None:
            start = dt.date.today() - timedelta(days=365 * 4)
        self.start, self.end = _sanitize_dates(start, end)
        self.json_parse_int = kwargs.pop("json_parse_int", None)
        self.json_parse_float = kwargs.pop("json_parse_float", None)
        self._validate_params()
        super(DailySummaryReader, self).__init__(**kwargs)

    def _validate_params(self):
        if self.last is not None:
            if not isinstance(self.last, int) or not (0 < self.last < 90):
                raise ValueError("last: lease enter an integer value from 1 to" " 90")
            return
        else:
            self._validate_dates(self.start, self.end)
            return
        raise ValueError(
            "Please enter a date range or number of days for " "retrieval period."
        )

    def _validate_response(self, response):
        return response.json(
            parse_int=self.json_parse_int, parse_float=self.json_parse_float
        )

    @property
    def url(self):
        return "stats/historical/daily"

    @property
    def islast(self):
        return self.last is not None and 1 < self.last < 91

    @property
    def params(self):
        p = {}
        if not self.islast:
            p["date"] = self.curr_date.strftime("%Y%m%d")
        else:
            p["last"] = self.last
        return p

    def fetch(self):
        """Unfortunately, IEX's API can only retrieve data one day or one month
        at a time. Rather than specifying a date range, we will have to run
        the read function for each date provided.

        :return: DataFrame
        """
        self._validate_params()
        if self.islast:
            data = super(DailySummaryReader, self).fetch()
        else:
            data = self._fetch_dates()
        if self.output_format == "pandas":
            data.set_index("date", inplace=True)
            return data
        else:
            return data

    def _fetch_dates(self):
        tlen = self.end - self.start
        dfs = []
        for date in (self.start + timedelta(n) for n in range(tlen.days)):
            self.curr_date = date
            tdf = super(DailySummaryReader, self).fetch()
            dfs.append(tdf)
        return dfs


class MonthlySummaryReader(Stats):
    """
    Class for obtaining data from the Historical Summary endpoint of IEX Stats

    Attributes
    ----------
    start : str, int, date, datetime, Timestamp
        Desired start date
    end : str, int, date, datetime, Timestamp
        Desired end date
    kwargs:
        Additional request parameters (see base class)


    Reference
    ---------
    https://iextrading.com/developer/docs/#historical-summary

    """

    def __init__(self, start=None, end=None, **kwargs):
        self.curr_date = start
        self.date_format = "%Y%m"
        self.start, self.end = _sanitize_dates(start, end)
        self._validate_dates(self.start, self.end)
        super(MonthlySummaryReader, self).__init__(**kwargs)

    @property
    def url(self):
        return "stats/historical"

    @property
    def params(self):
        p = {}
        if self.curr_date is not None:
            p["date"] = self.curr_date.strftime(self.date_format)
        return p

    def fetch(self):
        """Unfortunately, IEX's API can only retrieve data one day or one month
         at a time. Rather than specifying a date range, we will have to run
         the read function for each date provided.

        Returns:
        --------
        dataframes: pandas.DataFrame

        """
        tlen = self.end - self.start
        dfs = []

        # Build list of all dates within the given range
        lrange = [x for x in (self.start + timedelta(n) for n in range(tlen.days))]

        mrange = []
        for dtd in lrange:
            if datetime(dtd.year, dtd.month, 1) not in mrange:
                mrange.append(datetime(dtd.year, dtd.month, 1))
        lrange = mrange

        for date in lrange:
            self.curr_date = date
            tdf = super(MonthlySummaryReader, self).fetch()
            dfs.append(tdf)
        return dfs
