from datetime import datetime

import pytest

from iexfinance.refdata import (get_symbols, get_iex_symbols,
                                get_iex_corporate_actions, get_iex_dividends,
                                get_iex_next_day_ex_date,
                                get_iex_listed_symbol_dir)


IEX_MSG = "These functions return data for IEX listed symbols only. There is "\
          "only 1 listed IEX symbol."


class TestRef(object):

    def setup_class(self):
        self.keys = {"RecordID", "DailyListTimestamp", "CompanyName"}
        self.start = datetime(2017, 5, 4)

    def test_get_symbols(self):
        d = get_symbols()
        assert isinstance(d, list)
        assert isinstance(d[0], dict)

    @pytest.mark.cloud
    def test_get_iex_symbols(self):
        d = get_iex_symbols()

        assert isinstance(d, list)
        assert isinstance(d[0], dict)

    @pytest.mark.xfail(reason=IEX_MSG)
    @pytest.mark.legacy
    def test_get_iex_corporate_actions(self):
        d = get_iex_corporate_actions()
        assert isinstance(d, list)
        assert self.keys.issubset(set(d[0]))

    @pytest.mark.legacy
    @pytest.mark.xfail(reason=IEX_MSG)
    def test_get_iex_dividends(self):
        d = get_iex_dividends()
        assert isinstance(d, list)
        assert self.keys.issubset(set(d[0]))

    @pytest.mark.legacy
    @pytest.mark.xfail(reason=IEX_MSG)
    def test_iex_next_day_ex_date(self):
        d = get_iex_next_day_ex_date()
        assert isinstance(d, list)
        assert self.keys.issubset(set(d[0]))

    @pytest.mark.legacy
    def test_iex_listed_symbol_dir(self):
        d = get_iex_listed_symbol_dir()
        assert isinstance(d, list)
        assert self.keys.issubset(set(d[0]))

    @pytest.mark.legacy
    @pytest.mark.xfail(reason=IEX_MSG)
    def test_get_iex_corporate_actions_dates(self):
        d = get_iex_corporate_actions(start=self.start)
        assert isinstance(d, list)
        assert self.keys.issubset(set(d[0]))

    @pytest.mark.legacy
    @pytest.mark.xfail(reason=IEX_MSG)
    def test_get_iex_dividends_dates(self):
        d = get_iex_dividends(start=self.start)
        assert isinstance(d, list)
        assert self.keys.issubset(set(d[0]))

    @pytest.mark.legacy
    @pytest.mark.xfail(reason=IEX_MSG)
    def test_iex_next_day_ex_date_dates(self):
        d = get_iex_next_day_ex_date(start=self.start)
        assert isinstance(d, list)
        assert self.keys.issubset(set(d[0]))

    @pytest.mark.legacy
    @pytest.mark.xfail(reason=IEX_MSG)
    def test_iex_listed_symbol_dir_dates(self):
        d = get_iex_listed_symbol_dir(start=self.start)
        assert isinstance(d, list)
        assert self.keys.issubset(set(d[0]))
