from .base import _IEXBase
from iexfinance.utils.exceptions import IEXQueryError
import pandas as pd
from datetime import datetime, timedelta

# Data provided for free by IEX
# Data is furnished in compliance with the guidelines promulgated in the IEX
# API terms of service and manual
# See https://iextrading.com/api-exhibit-a/ for additional information
# and conditions of use


class Stats(_IEXBase):
    """
    Base class for obtaining date from the IEX Stats endpoints
    of IEX. Subclass of _IEXBase, subclassed by various.

    Reference: https://iextrading.com/developer/docs/#iex-stats
    """

    def __init__(self, outputFormat='json', retry_count=3, pause=0.001,
                 session=None):
        super(Stats, self).__init__(symbolList=None, retry_count=retry_count,
                                    pause=pause, session=session)
        self.outputFormat = outputFormat

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

    @property
    def acc_pandas(self):
        return True

    @property
    def url(self):
        return "stats"

    def fetch(self):
        return self._output_format(super(Stats, self).fetch())


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

    Reference: https://iextrading.com/developer/docs/#historical-daily
    """

    def __init__(self, start=None, end=None, last=None,
                 outputFormat='json', retry_count=3, pause=0.001,
                 session=None):
        import warnings
        warnings.warn('Daily statistics is not working due to issues with the '
                      'IEX API')
        self.curr_date = start
        self.last = last
        self.start = start
        self.end = end
        super(DailySummaryReader, self).__init__(outputFormat=outputFormat,
                                                 retry_count=retry_count,
                                                 pause=pause, session=session)

    @staticmethod
    def _validate_response(response):
        return response.json()

    @property
    def url(self):
        return "stats/historical/daily"

    @property
    def islast(self):
        return self.last is not None and 1 < self.last < 91

    @property
    def params(self):
        p = {}
        if self.last is not None:
            if self.last > 90:
                raise ValueError("'last' must be an integer up to 90.")
            else:
                p['last'] = self.last
                return p
        elif self.curr_date is not None:
            p['date'] = self.curr_date.strftime('%Y%m%d')
            return p
        else:
            raise ValueError("Must specify either a date range or number"
                             " of days (last).")

    def fetch(self):
        """Unfortunately, IEX's API can only retrieve data one day or one month
        at a time. Rather than specifying a date range, we will have to run
        the read function for each date provided.

        :return: DataFrame
        """
        if self.islast:
            data = super(DailySummaryReader, self).fetch()
        else:
            data = self._fetch_dates()
        if self.outputFormat == 'pandas':
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
        if self.outputFormat == 'pandas':
            return pd.concat(dfs)
        else:
            return dfs


class MonthlySummaryReader(Stats):
    """
    Class for obtaining data from the Historical Summary endpoint of IEX Stats

    Reference: https://iextrading.com/developer/docs/#historical-summary
    """

    def __init__(self, start=None, end=None,
                 outputFormat='json', retry_count=3, pause=0.001,
                 session=None):
        self.curr_date = start
        self.date_format = '%Y%m'
        self.start = start
        self.end = end

        super(MonthlySummaryReader, self).__init__(outputFormat=outputFormat,
                                                   retry_count=retry_count,
                                                   pause=pause,
                                                   session=session)

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
            if self.outputFormat == 'pandas':
                if not tdf.empty:
                    tdf['date'] = date.strftime(self.date_format)
            dfs.append(tdf)

        # We may not return any data if we failed to specify useful parameters:
        if self.outputFormat == 'pandas':
            result = pd.concat(dfs) if len(dfs) > 0 else pd.DataFrame()
            return result.set_index('date')
        else:
            return dfs
