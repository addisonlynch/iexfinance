import datetime as dt
import pytest
import pandas as pd

from iexfinance.utils import _handle_lists, _sanitize_dates


@pytest.fixture(params=[1, "test"], ids=["int", "string"])
def single(request):
    return request.param


@pytest.fixture(
    params=[
        [1, 2, 3],
        (1, 2, 3),
        pd.DataFrame([], index=[1, 2, 3]),
        pd.Series([1, 2, 3]),
    ],
    ids=["list", "tuple", "DataFrame", "Series"],
)
def mult(request):
    return request.param


class TestUtils(object):
    def test_handle_lists_sing(self, single):
        assert _handle_lists(single, mult=False) == single
        assert _handle_lists(single) == [single]

    def test_handle_lists_mult(self, mult):
        assert _handle_lists(mult) == [1, 2, 3]

    def test_handle_lists_err(self, mult):
        with pytest.raises(ValueError):
            _handle_lists(mult, mult=False)

    @pytest.mark.parametrize(
        "input_date",
        [
            "2019-01-01",
            "JAN-01-2010",
            dt.datetime(2019, 1, 1),
            dt.date(2019, 1, 1),
            pd.Timestamp(2019, 1, 1),
        ],
    )
    def test_sanitize_dates(self, input_date):
        expected_start = pd.to_datetime(input_date)
        expected_end = pd.to_datetime(dt.date.today())
        result = _sanitize_dates(input_date, None)
        assert result == (expected_start, expected_end)

    def test_sanitize_dates_int(self):
        start_int = 2018
        end_int = 2019
        expected_start = pd.to_datetime(dt.datetime(start_int, 1, 1))
        expected_end = pd.to_datetime(dt.datetime(end_int, 1, 1))
        assert _sanitize_dates(start_int, end_int) == (expected_start, expected_end)

    def test_sanitize_invalid_dates(self):
        with pytest.raises(ValueError):
            _sanitize_dates(2019, 2018)

        with pytest.raises(ValueError):
            _sanitize_dates("2019-01-01", "2018-01-01")

        with pytest.raises(ValueError):
            _sanitize_dates("20199", None)

        with pytest.raises(ValueError):
            _sanitize_dates(2022, None)

        with pytest.raises(ValueError):
            _sanitize_dates(None, 2022)

    def test_sanitize_dates_defaults(self):
        start_raw = dt.date.today() - dt.timedelta(days=365 * 15)
        default_start = pd.to_datetime(start_raw)
        default_end = pd.to_datetime(dt.date.today())
        assert _sanitize_dates(None, None) == (default_start, default_end)
