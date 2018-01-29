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


class TestStatsDaily(object):

    def test_daily_last_json(self):
        ls = get_stats_daily(last=5)
        assert isinstance(ls, list)
        assert len(ls) is 5

    def test_daily_last_pandas(self):
        df = get_stats_daily(last=5, output_format='pandas')
        assert isinstance(df, DataFrame)
        assert len(df) is 5

    def test_daily_dates_json(self):
        ls = get_stats_daily(start=datetime(2017, 1, 1),
                             end=datetime(2017, 2, 1))
        assert isinstance(ls, list)
        assert len(ls) is 31

    def test_daily_dates_pandas(self):
        df = get_stats_daily(start=datetime(2017, 1, 1),
                             end=datetime(2017, 2, 1), output_format='pandas')
        assert isinstance(df, DataFrame)
        assert len(df) is 31

    def test_daily_invalid_last(self):
        with pytest.raises(ValueError):
            get_stats_daily(last=120)

    def test_daily_fails_no_params(self):
        with pytest.raises(ValueError):
            get_stats_daily()

        with pytest.raises(ValueError):
            get_stats_daily(end=datetime(2017, 1, 1))

    def test_daily_invalid_start_date(self):
        with pytest.raises(ValueError):
            get_stats_daily(start=datetime(2011, 1, 1))

        with pytest.raises(ValueError):
            get_stats_daily(start=datetime(2022, 1, 1))

    def test_daily_invalid_end_date(self):
        with pytest.raises(ValueError):
            get_stats_daily(start=datetime(2017, 1, 1))

        with pytest.raises(ValueError):
            get_stats_daily(start=datetime(2017, 1, 1), end=datetime(2016, 1,
                            1))

        with pytest.raises(ValueError):
            get_stats_daily(start=datetime(2017, 1, 1), end=datetime(2028, 1,
                            1))


class TestStatsMonthly(object):

    def test_monthly_json(self):
        ls = get_stats_monthly(start=datetime(2017, 1, 1),
                               end=datetime(2017, 2, 1))
        assert isinstance(ls, list)
        assert len(ls) is 1

    def test_monthly_pandas(self):
        df = get_stats_monthly(start=datetime(2017, 1, 1),
                               end=datetime(2017, 3, 1),
                               output_format='pandas')
        assert isinstance(df, DataFrame)
        assert len(df) is 2

    def test_monthly_fails_no_params(self):
        with pytest.raises(ValueError):
            get_stats_monthly()

        with pytest.raises(ValueError):
            get_stats_monthly(end=datetime(2017, 1, 1))

    def test_monthly_invalid_start_date(self):
        with pytest.raises(ValueError):
            get_stats_monthly(start=datetime(2011, 1, 1))

        with pytest.raises(ValueError):
            get_stats_monthly(start=datetime(2022, 1, 1))

    def test_monthly_invalid_end_date(self):
        with pytest.raises(ValueError):
            get_stats_monthly(start=datetime(2017, 1, 1))

        with pytest.raises(ValueError):
            get_stats_monthly(start=datetime(2017, 1, 1), end=datetime(2016, 1,
                              1))

        with pytest.raises(ValueError):
            get_stats_monthly(start=datetime(2017, 1, 1), end=datetime(2028, 1,
                              1))
