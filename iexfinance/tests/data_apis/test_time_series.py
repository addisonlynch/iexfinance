import pandas as pd

from iexfinance.data_apis import get_time_series


class TestTimeSeries(object):
    def test_all_series_default(self):
        data = get_time_series()
        assert isinstance(data, pd.DataFrame)

    def test_all_series_json(self):
        data = get_time_series(output_format="json")

        assert isinstance(data, list)

    def test_params(self):
        data = get_time_series("REPORTED_FINANCIALS", "AAPL", last=1)

        assert isinstance(data, pd.DataFrame)
        assert isinstance(data.columns, pd.DatetimeIndex)
