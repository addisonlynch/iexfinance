from datetime import datetime, timedelta

import pandas as pd

from .base import _IEXBase

# Data provided for free by IEX
# See https://iextrading.com/api-exhibit-a/ for additional information
# and conditions of use


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
                raise ValueError("start: retrieval period must begin from "
                                 + str(now.year - 4) + " until now")
            # Ensure end date (if specified is between start and now)
            if isinstance(end, datetime):
                if end > now or end < start:
                    raise ValueError("end: retrieval period must end"
                                     "between start and the current date")

                return
            else:
                raise ValueError("end: Please enter a valid end date")
        else:
            raise ValueError("Please specify a valid date range or last value")


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
    start: datetime.datetime
        Desired start of summary period
    end: datetime.datetime
        Desired end of summary period (if omitted, start
        month will be returned)
    last: int
        Period between 1 and 90 days, overrides dates
    output_format: str, default 'json', optional
        Desired output format (json or pandas)
    kwargs:
        Additional request parameters (see base class)


    Reference
    ---------
    https://iextrading.com/developer/docs/#historical-daily

    """

    def __init__(self, start=None, end=None, last=None, **kwargs):
        import warnings
        warnings.warn('Daily statistics is not working due to issues with the '
                      'IEX API')
        self.curr_date = start
        self.last = last
        self.start = start
        self.end = end
        self.json_parse_int = kwargs.pop("json_parse_int", None)
        self.json_parse_float = kwargs.pop("json_parse_float", None)
        self._validate_params()
        super(DailySummaryReader, self).__init__(**kwargs)

    def _validate_params(self):
        if self.last is not None:
            if not isinstance(self.last, int) or not (0 < self.last < 90):
                raise ValueError("last: lease enter an integer value from 1 to"
                                 " 90")
            return
        else:
            self._validate_dates(self.start, self.end)
            return
        raise ValueError("Please enter a date range or number of days for "
                         "retrieval period.")

    def _validate_response(self, response):
        return response.json(
            parse_int=self.json_parse_int,
            parse_float=self.json_parse_float)

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
            p['date'] = self.curr_date.strftime('%Y%m%d')
        else:
            p['last'] = self.last
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
        if self.output_format == 'pandas':
            data.set_index('date', inplace=True)
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
        if self.output_format == 'pandas':
            return pd.concat(dfs)
        else:
            return dfs


class MonthlySummaryReader(Stats):
    """
    Class for obtaining data from the Historical Summary endpoint of IEX Stats

    Attributes
    ----------
    start: datetime.datetime
        Desired start of summary period
    end: datetime.datetime
        Desired end of summary period (if omitted, start
        month will be returned)
    output_format: str, default 'json', optional
        Desired output format (json or pandas)
    kwargs:
        Additional request parameters (see base class)


    Reference
    ---------
    https://iextrading.com/developer/docs/#historical-summary

    """

    def __init__(self, start=None, end=None, **kwargs):
        self.curr_date = start
        self.date_format = '%Y%m'
        self.start = start
        self.end = end
        self._validate_dates(self.start, self.end)
        super(MonthlySummaryReader, self).__init__(**kwargs)

    @property
    def url(self):
        return "stats/historical"

    @property
    def params(self):
        p = {}
        if self.curr_date is not None:
            p['date'] = self.curr_date.strftime(self.date_format)
        return p

    def fetch(self):
        """Unfortunately, IEX's API can only retrieve data one day or one month
         at a time. Rather than specifying a date range, we will have to run
         the read function for each date provided.

        :return: DataFrame
        """
        tlen = self.end - self.start
        dfs = []

        # Build list of all dates within the given range
        lrange = [x for x in (self.start + timedelta(n)
                              for n in range(tlen.days))]

        mrange = []
        for dt in lrange:
            if datetime(dt.year, dt.month, 1) not in mrange:
                mrange.append(datetime(dt.year, dt.month, 1))
        lrange = mrange

        for date in lrange:
            self.curr_date = date
            tdf = super(MonthlySummaryReader, self).fetch()

            # We may not return data if this was a weekend/holiday:
            if self.output_format == 'pandas':
                if not tdf.empty:
                    tdf['date'] = date.strftime(self.date_format)
            dfs.append(tdf)

        # We may not return any data if we failed to specify useful parameters:
        if self.output_format == 'pandas':
            result = pd.concat(dfs) if len(dfs) > 0 else pd.DataFrame()
            return result.set_index('date')
        else:
            return dfs
