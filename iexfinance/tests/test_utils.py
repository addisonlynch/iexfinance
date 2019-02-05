import datetime
import pytest
import pandas as pd

from iexfinance.utils import _handle_lists, _sanitize_dates


@pytest.fixture(params=[
    1,
    "test"
], ids=[
    "int",
    "string"
])
def single(request):
    return request.param


@pytest.fixture(params=[
    [1, 2, 3],
    (1, 2, 3),
    pd.DataFrame([], index=[1, 2, 3]),
    pd.Series([1, 2, 3]),
], ids=[
    "list",
    "tuple",
    "DataFrame",
    "Series"
])
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

    def test_sanitize_dates_years(self):
        expected = (datetime.datetime(2017, 1, 1),
                    datetime.datetime(2018, 1, 1))
        assert _sanitize_dates(2017, 2018) == expected

    def test_sanitize_dates_default(self):
        exp_start = datetime.datetime(2015, 1, 1, 0, 0)
        exp_end = datetime.datetime.today()
        start, end = _sanitize_dates(None, None)

        assert start == exp_start
        assert end.date() == exp_end.date()

    def test_sanitize_dates(self):
        start = datetime.datetime(2017, 3, 4)
        end = datetime.datetime(2018, 3, 9)

        assert _sanitize_dates(start, end) == (start, end)

    def test_sanitize_dates_error(self):
        start = datetime.datetime(2018, 1, 1)
        end = datetime.datetime(2017, 1, 1)

        with pytest.raises(ValueError):
            _sanitize_dates(start, end)
