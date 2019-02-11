import datetime
import pandas as pd

from iexfinance.base import _IEXBase
from iexfinance.stocks.base import Stock
from iexfinance.utils.exceptions import IEXSymbolError


class HistoricalReader(Stock):
    """
    A class to download historical data from the chart endpoint

    Parameters
    ----------
    symbols : string, array-like object (list, tuple, Series), or DataFrame
        Desired symbols for retrieval
    start: datetime.datetime
        The desired start date (defaults to 1/1/2015)
    end: datetime.datetime
        The desired end date (defaults to today's date)
    output_format: str, default 'json', optional
        Desired output format.

    Reference: https://iextrading.com/developer/docs/#chart
    """

    def __init__(self, symbols, start, end, **kwargs):
        self.start = start
        self.end = end
        super(HistoricalReader, self).__init__(symbols, **kwargs)

    @property
    def chart_range(self):
        """ Calculates the chart range from start and end. Downloads larger
        datasets (5y and 2y) when necessary, but defaults to 1y for performance
        reasons
        """
        delta = datetime.datetime.now().year - self.start.year
        if 2 <= delta <= 5:
            return "5y"
        elif 1 <= delta <= 2:
            return "2y"
        elif 0 <= delta < 1:
            return "1y"
        else:
            raise ValueError(
                "Invalid date specified. Must be within past 5 years.")

    @property
    def params(self):
        syms = ",".join(self.symbols)
        params = {
            "symbols": syms,
            "types": "chart",
            "range": self.chart_range
        }
        return params

    def _output_format(self, out, fmt_j=None, fmt_p=None):
        result = {}
        for symbol in self.symbols:
            if symbol not in out or not out[symbol]["chart"]:
                raise IEXSymbolError(symbol)
            d = out.pop(symbol)["chart"]
            df = pd.DataFrame(d)
            if self.output_format == 'pandas':
                df["date"] = pd.DatetimeIndex(df["date"])
            df = df.set_index(df["date"])
            values = ["open", "high", "low", "close", "volume"]
            df = df[values]
            sstart = self.start.strftime('%Y-%m-%d')
            send = self.end.strftime('%Y-%m-%d')
            df = df.loc[sstart:send]
            result.update({symbol: df})
        if self.output_format == "pandas":
            if len(result) > 1:
                result = pd.concat(result.values(), keys=result.keys(), axis=1)
        else:
            for sym in list(result):
                result[sym] = result[sym].to_dict('index')
        return result[self.symbols[0]] if self.n_symbols == 1 else result


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
            return 'stock/%s/chart/1d' % self.symbol
        else:
            return 'stock/%s/chart/date/%s' % (self.symbol, self.date)

    def _convert_output(self, out):
        if out:
            df = pd.DataFrame(out).set_index("minute")
            df.index = df.date + " " + df.index
            df.index = pd.DatetimeIndex([pd.to_datetime(x) for x in
                                         df.index])
            return df
        else:
            return pd.DataFrame()
