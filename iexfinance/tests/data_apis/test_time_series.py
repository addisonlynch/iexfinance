import pandas as pd
import pytest

from iexfinance.data_apis import get_time_series


class TestTimeSeries(object):
    @pytest.mark.xfail(reason="Endpoint not working in sandbox environment")
    def test_all_series(self):
        data = get_time_series()

        assert isinstance(data, list)

    @pytest.mark.xfail(reason="Endpoint not working in sandbox environment")
    def test_all_series_pandas(self):
        data = get_time_series(output_format="pandas")

        assert isinstance(data, pd.DataFrame)

    def test_params(self):
        data = get_time_series("REPORTED_FINANCIALS", "AAPL", last=1)

        assert isinstance(data, pd.DataFrame)
        assert isinstance(data.columns, pd.DatetimeIndex)
