from datetime import datetime

import pytest

from iexfinance import (get_available_symbols, get_iex_corporate_actions,
                        get_iex_dividends, get_iex_next_day_ex_date,
                        get_iex_listed_symbol_dir)


class TestRef(object):

    def setup_class(self):
        self.keys = {"RecordID", "DailyListTimestamp", "CompanyName"}
        self.start = datetime(2017, 5, 4)

    def test_get_available_symbols(self):
        d = get_available_symbols()
        assert isinstance(d, list)
        assert isinstance(d[0], dict)

    @pytest.mark.xfail(reason="New reference datapoints are not operational "
                       "yet as of 1/31/18.")
    def test_get_iex_corporate_actions(self):
        d = get_iex_corporate_actions()
        assert isinstance(d, list)
        assert self.keys.issubset(set(d[0]))

    @pytest.mark.xfail(reason="New reference datapoints are not operational "
                       "yet as of 1/31/18.")
    def test_get_iex_dividends(self):
        d = get_iex_dividends()
        assert isinstance(d, list)
        assert self.keys.issubset(set(d[0]))

    @pytest.mark.xfail(reason="New reference datapoints are not operational "
                       "yet as of 1/31/18.")
    def test_iex_next_day_ex_date(self):
        d = get_iex_next_day_ex_date()
        assert isinstance(d, list)
        assert self.keys.issubset(set(d[0]))

    @pytest.mark.xfail(reason="New reference datapoints are not operational "
                       "yet as of 1/31/18.")
    def test_iex_listed_symbol_dir(self):
        d = get_iex_listed_symbol_dir()
        assert isinstance(d, list)
        assert self.keys.issubset(set(d[0]))

    @pytest.mark.xfail(reason="New reference datapoints are not operational "
                       "yet as of 1/31/18.")
    def test_get_iex_corporate_actions_dates(self):
        d = get_iex_corporate_actions(start=self.start)
        assert isinstance(d, list)
        assert self.keys.issubset(set(d[0]))

    @pytest.mark.xfail(reason="New reference datapoints are not operational "
                       "yet as of 1/31/18.")
    def test_get_iex_dividends_dates(self):
        d = get_iex_dividends(start=self.start)
        assert isinstance(d, list)
        assert self.keys.issubset(set(d[0]))

    @pytest.mark.xfail(reason="New reference datapoints are not operational "
                       "yet as of 1/31/18.")
    def test_iex_next_day_ex_date_dates(self):
        d = get_iex_next_day_ex_date(start=self.start)
        assert isinstance(d, list)
        assert self.keys.issubset(set(d[0]))

    @pytest.mark.xfail(reason="New reference datapoints are not operational "
                       "yet as of 1/31/18.")
    def test_iex_listed_symbol_dir_dates(self):
        d = get_iex_listed_symbol_dir(start=self.start)
        assert isinstance(d, list)
        assert self.keys.issubset(set(d[0]))


class TestCloudRef(object):

    def test_symbols(self):
        pass
