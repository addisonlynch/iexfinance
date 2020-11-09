import pandas as pd

from iexfinance.apidata import get_api_status


class TestAPIData(object):
    def test_api_status(self):
        data = get_api_status()

        assert isinstance(data, pd.DataFrame)
