import pandas as pd

from iexfinance.stocks import get_sector_performance


class TestSectorPerformance(object):
    def test_sector_performance(self):
        data = get_sector_performance()

        assert isinstance(data, pd.DataFrame)
        assert "type" in data.columns
