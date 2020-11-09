import pandas as pd

from iexfinance.stocks import Stock


class TestNews(object):
    def setup_class(self):
        self.a = Stock("AAPL")
        self.b = Stock(["AAPL", "TSLA"])

    def test_news(self):
        data = self.a.get_news()

        assert isinstance(data, pd.DataFrame)

        data2 = self.b.get_news()

        assert isinstance(data2, pd.DataFrame)
        assert isinstance(data2.index, pd.MultiIndex)
        assert "AAPL" in data2.index
        assert "TSLA" in data2.index
