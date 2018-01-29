from iexfinance import (get_stats_intraday, get_stats_recent,
                        get_stats_records, get_stats_daily,
                        get_stats_monthly)

import pytest
from pandas import DataFrame
from datetime import datetime


class TestStats(object):

    def test_intraday_json(self):
        js = get_stats_intraday()
        assert isinstance(js, dict)

    def test_intraday_pandas(self):
        df = get_stats_intraday(output_format='pandas')
        assert isinstance(df, DataFrame)

    @pytest.mark.xfail(reason='IEX recent API endpoint unstable.')
    def test_recent_json(self):
        ls = get_stats_recent()
        assert isinstance(ls, list)

    def test_recent_pandas(self):
        df = get_stats_recent(output_format='pandas')
        assert isinstance(df, DataFrame)

    def test_records_json(self):
        js = get_stats_records()
        assert isinstance(js, dict)

    def test_records_pandas(self):
        df = get_stats_records(output_format='pandas')
        assert isinstance(df, DataFrame)

    def test_daily_last_json(self):
        ls = get_stats_daily(last=5)
        assert isinstance(ls, list)

    def test_daily_last_pandas(self):
        df = get_stats_daily(last=5, output_format='pandas')
        assert isinstance(df, DataFrame)

    def test_daily_dates_json(self):
        ls = get_stats_daily(start=datetime(2017, 5, 4),
                             end=datetime(2017, 8, 7))
        assert isinstance(ls, list)

    def test_daily_dates_pandas(self):
        df = get_stats_daily(start=datetime(2017, 5, 4),
                             end=datetime(2017, 8, 7), output_format='pandas')
        assert isinstance(df, DataFrame)

    def test_monthly_json(self):
        ls = get_stats_monthly(start=datetime(2017, 5, 4),
                               end=datetime(2017, 8, 7))
        assert isinstance(ls, list)

    def test_monthly_pandas(self):
        df = get_stats_monthly(start=datetime(2017, 5, 4),
                               end=datetime(2017, 8, 7),
                               output_format='pandas')
        assert isinstance(df, DataFrame)
