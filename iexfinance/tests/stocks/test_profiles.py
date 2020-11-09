import pandas as pd

from iexfinance.stocks import Stock


class TestStockProfiles(object):
    def setup_class(self):
        self.a = Stock("AAPL")
        self.b = Stock(["AAPL", "TSLA"])

    def test_company(self):
        data = self.a.get_company()

        assert isinstance(data, pd.DataFrame)

    def test_insider_roster(self):
        data = self.a.get_insider_roster()

        assert isinstance(data, pd.DataFrame)

        data2 = self.b.get_insider_roster()

        assert isinstance(data2, pd.DataFrame)
        assert isinstance(data2.index, pd.MultiIndex)

    def test_insider_summary(self):
        data = self.a.get_insider_summary()

        assert isinstance(data, pd.DataFrame)

        data2 = self.b.get_insider_summary()

        assert isinstance(data2, pd.DataFrame)
        assert isinstance(data2.index, pd.MultiIndex)

    def test_insider_transactions(self):
        data = self.a.get_insider_transactions()

        assert isinstance(data, pd.DataFrame)

        data2 = self.b.get_insider_transactions()

        assert isinstance(data2, pd.DataFrame)
        assert isinstance(data2.index, pd.MultiIndex)

    def test_logo(self):
        data = self.a.get_logo()

        assert isinstance(data, pd.DataFrame)

    def test_peers(self):
        data = self.a.get_peers()

        assert isinstance(data, pd.DataFrame)
