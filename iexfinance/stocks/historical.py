import datetime
import pandas as pd

from iexfinance.stocks.base import StockReader
from iexfinance.utils.exceptions import IEXSymbolError


class HistoricalReader(StockReader):
    """
    A class to download historical data from the chart endpoint

    Parameters
    ----------
    symbol: str or list-like
        A symbol or list of symbols
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
            if symbol not in out:
                raise IEXSymbolError("Data for %s could not be found." %
                                     symbol)
            d = out.pop(symbol)["chart"]
            df = pd.DataFrame(d)
            df.set_index("date", inplace=True)
            values = ["open", "high", "low", "close", "volume"]
            df = df[values]
            sstart = self.start.strftime('%Y-%m-%d')
            send = self.end.strftime('%Y-%m-%d')
            df = df.loc[sstart:send]
            result.update({symbol: df})
        if self.output_format is "pandas":
            if len(result) > 1:
                result = pd.concat(result.values(), keys=result.keys(), axis=1)
        else:
            for sym in list(result):
                result[sym] = result[sym].to_dict('index')
        return result[self.symbols[0]] if self.n_symbols == 1 else result
