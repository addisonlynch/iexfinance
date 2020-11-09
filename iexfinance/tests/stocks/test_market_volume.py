import pandas as pd

from iexfinance.stocks import get_market_volume


class TestMarketVolume(object):
    def test_market_volume(self):
        data = get_market_volume()

        assert isinstance(data, pd.DataFrame)
        assert "venueName" in data.columns
