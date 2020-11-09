import pandas as pd
import pytest

from iexfinance.stocks import Stock
from iexfinance.utils.exceptions import IEXQueryError


class TestStockPrices(object):
    def setup_class(self):
        self.a = Stock("AAPL")
        self.b = Stock(["AAPL", "TSLA"])
        self.c = Stock("SVXY")
        self.d = Stock(["AAPL", "SVXY"])
        self.e = Stock("BADSYMBOL")

    def test_bad_symbol(self):
        with pytest.raises(IEXQueryError):
            self.e.get_book()

    def test_book(self):
        data = self.a.get_book()

        assert isinstance(data, dict)

    def test_chart(self):
        data = self.a.get_chart()

        assert isinstance(data, pd.DataFrame)

    def test_delayed_quote(self):
        data = self.a.get_delayed_quote()

        assert isinstance(data, pd.DataFrame)
        assert "AAPL" in data.index

    def test_historical_prices(self):
        data = self.a.get_historical_prices()

        assert isinstance(data, pd.DataFrame)

        data2 = self.b.get_historical_prices()

        assert isinstance(data2, pd.DataFrame)
        assert isinstance(data2.index, pd.MultiIndex)
        assert "AAPL" in data2.index
        assert "TSLA" in data2.index

    def test_intraday_prices(self):
        data = self.a.get_intraday_prices()

        assert isinstance(data, pd.DataFrame)

        data2 = self.b.get_historical_prices()

        assert isinstance(data2, pd.DataFrame)
        assert isinstance(data2.index, pd.MultiIndex)
        assert "AAPL" in data2.index
        assert "TSLA" in data2.index

    def test_largest_trades(self):
        data = self.a.get_largest_trades()

        assert isinstance(data, pd.DataFrame)

    def test_open_close(self):
        data = self.a.get_open_close()

        assert isinstance(data, pd.DataFrame)

    def test_ohlc(self):
        data = self.a.get_ohlc()

        assert isinstance(data, pd.DataFrame)

    def test_previous_day_prices(self):
        data = self.a.get_previous_day_prices()

        assert isinstance(data, pd.DataFrame)

    def test_price(self):
        data = self.a.get_price()

        assert isinstance(data, pd.DataFrame)

    def test_quote(self):
        data = self.a.get_quote()

        assert isinstance(data, pd.DataFrame)

    def test_volume_by_venue(self):
        data = self.a.get_volume_by_venue()

        assert isinstance(data, pd.DataFrame)
