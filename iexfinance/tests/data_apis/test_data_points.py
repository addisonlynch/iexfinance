import pandas as pd
import pytest

from iexfinance.data_apis import get_data_points


class TestDataPoints(object):
    def test_no_symbol_fails(self):
        with pytest.raises(TypeError):
            get_data_points()

    def test_all_data_points(self):
        data = get_data_points("AAPL")
        assert isinstance(data, pd.DataFrame)
        assert "key" in data.columns

    def test_get_one_data_point(self):
        data = get_data_points("AAPL", "ZIP")
        assert isinstance(data, str)

    def test_get_one_data_point2(self):
        data = get_data_points("AAPL", "ZIP", output_format="pandas")
        assert isinstance(data, str)
