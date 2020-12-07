import pandas as pd
import pytest

from iexfinance.stocks import Stock


class TestStockResearch(object):
    def setup_class(self):
        self.a = Stock("AAPL")
        self.b = Stock(["AAPL", "TSLA"])

    def test_advanced_stats(self):
        data = self.a.get_advanced_stats()

        assert isinstance(data, pd.DataFrame)

    def test_estimates(self):
        data = self.a.get_estimates()

        assert isinstance(data, pd.DataFrame)

        data2 = self.b.get_estimates()

        assert isinstance(data2, pd.DataFrame)
        assert isinstance(data2.index, pd.MultiIndex)
        assert "AAPL" in data2.index
        assert "TSLA" in data2.index

    def test_fund_ownership(self):
        data = self.a.get_fund_ownership()

        assert isinstance(data, pd.DataFrame)

        data2 = self.b.get_fund_ownership()

        assert isinstance(data2, pd.DataFrame)
        assert isinstance(data2.index, pd.MultiIndex)
        assert "AAPL" in data2.index
        assert "TSLA" in data2.index

    def test_institutional_ownership(self):
        data = self.a.get_institutional_ownership()

        assert isinstance(data, pd.DataFrame)

        data2 = self.b.get_institutional_ownership()

        assert isinstance(data2, pd.DataFrame)
        assert isinstance(data2.index, pd.MultiIndex)
        assert "AAPL" in data2.index
        assert "TSLA" in data2.index

    def test_key_stats(self):
        data = self.a.get_key_stats()

        assert isinstance(data, pd.DataFrame)

    @pytest.mark.xfail(reason="Requires special permission to access.")
    def test_price_target(self):
        data = self.a.get_price_target()

        assert isinstance(data, pd.DataFrame)

        data2 = self.b.get_price_target()

        assert isinstance(data2, pd.DataFrame)
        assert "AAPL" in data2.index
        assert "TSLA" in data2.index
