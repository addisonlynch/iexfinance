import datetime
import pandas as pd

from iexfinance.base import _IEXBase
from iexfinance.stocks.base import Stock
from iexfinance.utils import _sanitize_dates


class HistoricalReader(Stock):
    """
    Base class to download historical data from the chart endpoint

    Reference: https://iextrading.com/developer/docs/#chart
    """

    def __init__(self, symbols, start=None, end=None, close_only=False, **kwargs):
        start = start or datetime.datetime.today() - datetime.timedelta(days=365)
        self.start, self.end = _sanitize_dates(start, end)
        self.close_only = close_only
        super(HistoricalReader, self).__init__(symbols, **kwargs)

    @property
    def single_day(self):
        return True if self.end is None else False

    @property
    def chart_range(self):
        """Calculates the chart range from start and end"""
        # TODO: rewrite to account for leap years

        delta_days = (datetime.datetime.now() - self.start).days
        if 0 <= delta_days < 6:
            return "5d"
        elif 6 <= delta_days < 28:
            return "1m"
        elif 28 <= delta_days < 84:
            return "3m"
        elif 84 <= delta_days < 168:
            return "6m"
        elif 168 <= delta_days < 365:
            return "1y"
        elif 365 <= delta_days < 730:
            return "2y"
        elif 730 <= delta_days < 1826:
            return "5y"
        elif 1826 <= delta_days < 5478:
            return "max"
        else:
            raise ValueError("Invalid date specified. " "Must be within past 15 years.")

    @property
    def params(self):
        syms = ",".join(self.symbols)
        params = {
            "symbols": syms,
            "types": "chart",
            "range": self.chart_range,
            "chartByDay": self.single_day,
            "chartCloseOnly": self.close_only,
        }
        if self.single_day:
            try:
                params["exactDate"] = self.start.strftime("%Y%m%d")
            except AttributeError:
                params["exactDate"] = self.start
        return params

    def _format_output(self, out, format=None):
        if self.output_format == "json":
            return out
        if len(self.symbols) > 1:
            out = {
                (symbol, day["date"]): day
                for symbol in out
                for day in out[symbol]["chart"]
            }
            result = pd.DataFrame.from_dict(out, orient="columns").drop("date").T
            result.index = result.index.set_levels(
                [result.index.levels[0], pd.to_datetime(result.index.levels[1])]
            )
            idx = pd.IndexSlice
            result = result.loc[idx[:, self.start : self.end], :]
        else:
            out = {entr["date"]: entr for entr in out[self.symbols[0]]["chart"]}
            result = pd.DataFrame.from_dict(out, orient="columns").drop("date").T
            result.index = pd.to_datetime(result.index)
            result = result.loc[self.start : self.end, :]
        if self.close_only is True:
            result = result.loc[:, ["close", "volume"]]
        return result


class IntradayReader(_IEXBase):
    """
    Base class for intraday historical data
    """

    def __init__(self, symbol, date=None, **kwargs):
        try:
            self.date = date.strftime("%Y%m%d")
        except AttributeError:
            self.date = date

        if not isinstance(symbol, str):
            raise ValueError("Please enter a valid single symbol.")

        self.symbol = symbol
        super(IntradayReader, self).__init__(**kwargs)

    @property
    def params(self):
        return {}

    @property
    def url(self):
        if self.date is None:
            return "stock/%s/chart/1d" % self.symbol
        else:
            return "stock/%s/chart/date/%s" % (self.symbol, self.date)

    def _convert_output(self, out):
        if out:
            df = pd.DataFrame(out).set_index("minute")
            df.index = df.date + " " + df.index
            df.index = pd.DatetimeIndex([pd.to_datetime(x) for x in df.index])
            return df
        else:
            return pd.DataFrame()
