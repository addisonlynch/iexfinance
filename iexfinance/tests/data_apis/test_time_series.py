import pandas as pd
import pytest

from iexfinance.data_apis import get_time_series
from iexfinance.utils.exceptions import IEXQueryError


class TestTimeSeries(object):

    def test_all_series(self):
        data = get_time_series()

        assert isinstance(data, list)

    def test_all_series_pandas(self):
        data = get_time_series(output_format='pandas')

        assert isinstance(data, pd.DataFrame)

    def test_no_key_fails(self):
        with pytest.raises(IEXQueryError):
            get_time_series("REPORTED_FINANCIALS")

    def test_id_key(self):
        data = get_time_series("REPORTED_FINANCIALS", "AAPL")

        assert isinstance(data, list)
        assert "subkey" in data[1]

    def test_id_key_subkey(self):
        data = get_time_series("REPORTED_FINANCIALS", "AAPL", "10-K")

        assert isinstance(data, list)
        assert len(data) == 10
        assert "dateFiled" in data[1]

        # IEX returns last 10 years of financials

    def test_params(self):
        data = get_time_series("REPORTED_FINANCIALS", "AAPL", last=1)

        assert isinstance(data, list) and len(data) == 1

    def test_pandas_params(self):
        data = get_time_series("REPORTED_FINANCIALS", "AAPL", last=1,
                               output_format='pandas')

        assert isinstance(data, pd.DataFrame)
        assert isinstance(data.columns, pd.DatetimeIndex)
