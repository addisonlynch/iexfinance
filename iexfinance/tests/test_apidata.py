import pandas as pd

from iexfinance.apidata import get_api_status


class TestAPIData(object):

    def test_api_status_json(self):
        data = get_api_status()

        assert isinstance(data, dict)

    def test_api_status_pandas(self):
        data = get_api_status(output_format='pandas')

        assert isinstance(data, pd.DataFrame)
