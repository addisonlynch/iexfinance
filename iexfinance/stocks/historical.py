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
        self.cost = 0
        super(HistoricalReader, self).__init__(symbols, **kwargs)

    def __del__(self):
        print('this operation costs: %d' % self.cost)

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

    def _validate_response(self, response):
        self.cost += int(response.headers['iexcloud-messages-used'])
        json_response = super(HistoricalReader, self)._validate_response(response)
        # json_response['iexcloud-messages-used'] = response.headers['iexcloud-messages-used']
        return json_response

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


class HistoricalReaderCostOptimized(Stock):
    """
    A class to download historical data from the chart endpoint but with optimized costs

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
        self.cost = 0
        self.current_date = None
        super(HistoricalReaderCostOptimized, self).__init__(symbols, **kwargs)

    def __del__(self):
        print('this operation costs: %d' % self.cost)

    @property
    def params(self):
        syms = ",".join(self.symbols)
        params = {
            "symbols": syms,
            "types":   "chart",
            "range":   "date",
            'chartByDay': True,
            'exactDate': self.current_date
        }
        return params

    def _output_format(self, out, fmt_j=None, fmt_p=None):
        result = {}
        for symbol in self.symbols:
            if symbol not in out or out[symbol]["chart"] == None:  # don't remove the None. it's ok to get empty list here(e.g Saturday)
                raise IEXSymbolError(symbol)
            d = out.pop(symbol)["chart"]
            df = pd.DataFrame(d)
            if d:  # we may get empty data for non calendar days
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

    def _validate_response(self, response):
        json_response = super(HistoricalReaderCostOptimized, self)._validate_response(response)
        # json_response['iexcloud-messages-used'] = response.headers['iexcloud-messages-used']
        # print('this operation costs: %s' %response.headers['iexcloud-messages-used'])
        self.cost += int(response.headers['iexcloud-messages-used'])
        return json_response

    def fetch(self, **kwargs):
        """
        this fetch is cost optimized. IEX charges for the range we request so querying for 1y when all we need
        is a couple of days costs a lot!
        we will request 1 day every time and do it for every day in range. so if we want 1 week of data
        we will request 1 week of data and not 1 year. making it much more cost effective
        Returns
        -------
        response: requests.response
            A response object
        """
        if self.output_format == 'pandas':
            result = pd.DataFrame([])
            is_pandas = True
        else:
            result = {}
            is_pandas = False
        day_count = 0
        while self.start + datetime.timedelta(days=day_count) <= self.end:
            self.current_date = self.start + datetime.timedelta(days=day_count)
            # using the parent fetch() method but with optimized params
            ohlcv = super(HistoricalReaderCostOptimized, self).fetch(**kwargs)
            if len(self.symbols) > 1:
                if is_pandas:
                    result = result.append(ohlcv)
                else:
                    for symbol in self.symbols:
                        if symbol in result:
                            if ohlcv[symbol]:
                                result[symbol].update(ohlcv[symbol])
                        else:
                            result[symbol] = ohlcv[symbol]
            else:
                if is_pandas:
                    if not ohlcv.empty:
                        result = result.append(ohlcv)
                else:
                    if ohlcv:
                        result.update(ohlcv)
            day_count += 1
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
        self.cost = 0
        super(IntradayReader, self).__init__(**kwargs)

    def __del__(self):
        print('this operation costs: %d' % self.cost)

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

    def _validate_response(self, response):
        self.cost += int(response.headers['iexcloud-messages-used'])
        json_response = super(IntradayReader, self)._validate_response(response)
        return json_response
