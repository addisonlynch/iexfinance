from datetime import datetime

import pytest
from pandas import DataFrame

from iexfinance.iexdata import (get_tops, get_last, get_deep, get_deep_book,
                                get_stats_intraday, get_stats_recent,
                                get_stats_records, get_stats_daily,
                                get_stats_summary)


class TestMarketData(object):

    def setup_class(self):
        self.bad = ["AAPL", "TSLA", "MSFT", "F", "GOOGL", "STM", "DAL",
                    "UVXY", "SPY", "DIA", "SVXY", "CMG", "LUV"]

    @pytest.mark.xfail(reason="Market data only available during market open")
    def test_last_json_default(self):
        ls = get_last()

        assert isinstance(ls, list) and len(ls) > 7500

    @pytest.mark.xfail(reason="Market data only available during market open")
    def test_last_json_syms(self):
        ls = get_last("AAPL")
        ls2 = get_last(["AAPL", "TSLA"])

        assert isinstance(ls, list) and len(ls) == 1
        assert isinstance(ls2, list) and len(ls2) == 2

    @pytest.mark.xfail(reason="Market data only available during market open")
    def test_last_pandas(self):
        df = get_last(output_format='pandas')
        df2 = get_last("AAPL", output_format='pandas')
        df3 = get_last(["AAPL", "TSLA"], output_format='pandas')

        assert isinstance(df, DataFrame)
        assert isinstance(df2, DataFrame)
        assert isinstance(df3, DataFrame)

    def test_last_too_many_symbols(self):
        with pytest.raises(ValueError):
            get_last(self.bad)

    @pytest.mark.xfail(reason="Market data only available during market open")
    def test_TOPS_json_default(self):
        ls = get_tops()

        assert isinstance(ls, list) and len(ls) > 7500

    @pytest.mark.xfail(reason="Market data only available during market open")
    def test_TOPS_json_syms(self):
        ls = get_tops("AAPL")
        ls2 = get_tops(["AAPL", "TSLA"])

        assert isinstance(ls, list) and len(ls) == 1
        assert isinstance(ls2, list) and len(ls2) == 2

    def test_TOPS_too_many_symbols(self):
        with pytest.raises(ValueError):
            get_tops(self.bad)

    @pytest.mark.xfail(reason="Market data only available during market open")
    def test_TOPS_pandas(self):
        df = get_tops("AAPL", output_format='pandas')
        df2 = get_tops(["AAPL", "TSLA"], output_format='pandas')

        assert isinstance(df, DataFrame)
        assert isinstance(df2, DataFrame)

    @pytest.mark.xfail(reason="Market data only available during market open")
    def test_DEEP_json_default(self):
        with pytest.raises(ValueError):
            get_deep()

    @pytest.mark.xfail(reason="Market data only available during market open")
    def test_DEEP_json_syms(self):
        js = get_deep("AAPL")

        assert isinstance(js, dict)

    @pytest.mark.xfail(reason="Market data only available during market open")
    def test_DEEP_pandas(self):
        with pytest.raises(ValueError):
            get_deep("AAPL", output_format='pandas')

    def test_DEEP_too_many_syms(self):
        with pytest.raises(ValueError):
            get_deep(["AAPL", "TSLA"])

    @pytest.mark.xfail(reason="Market data only available during market open")
    def test_Book_json_default(self):
        with pytest.raises(ValueError):
            get_deep_book()

    @pytest.mark.xfail(reason="Market data only available during market open")
    def test_Book_json_syms(self):
        js = get_deep_book("AAPL")
        js2 = get_deep_book(["AAPL", "TSLA"])

        assert isinstance(js, dict) and len(js) == 1
        assert isinstance(js2, dict) and len(js2) == 2

    def test_Book_too_many_symbols(self):
        with pytest.raises(ValueError):
            get_deep_book(self.bad)


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
        assert len(ls) == 5

    def test_daily_last_pandas(self):
        df = get_stats_daily(last=5, output_format='pandas')
        assert isinstance(df, DataFrame)
        assert len(df) == 5

    def test_daily_dates_json(self):
        ls = get_stats_daily(start=datetime(2017, 1, 1),
                             end=datetime(2017, 2, 1))
        assert isinstance(ls, list)
        assert len(ls) == 31

    def test_daily_dates_pandas(self):
        df = get_stats_daily(start=datetime(2017, 1, 1),
                             end=datetime(2017, 2, 1), output_format='pandas')
        assert isinstance(df, DataFrame)
        assert len(df) == 20

    def test_daily_invalid_last(self):
        with pytest.raises(ValueError):
            get_stats_daily(last=120)

    def test_daily_invalid_start_date(self):
        with pytest.raises(ValueError):
            get_stats_daily(start=datetime(2011, 1, 1))

        with pytest.raises(ValueError):
            get_stats_daily(start=datetime(2022, 1, 1))

    def test_daily_invalid_end_date(self):
        with pytest.raises(ValueError):
            get_stats_daily(start=datetime(2017, 1, 1), end=datetime(2016, 1,
                            1))

        with pytest.raises(ValueError):
            get_stats_daily(start=datetime(2017, 1, 1), end=datetime(2028, 1,
                            1))


class TestStatsSummary(object):

    def test_summary_json(self):
        ls = get_stats_summary(start=datetime(2017, 1, 1),
                               end=datetime(2017, 2, 1))
        assert isinstance(ls, list)
        assert len(ls) == 1

    def test_summary_pandas(self):
        df = get_stats_summary(start=datetime(2017, 1, 1),
                               end=datetime(2017, 3, 1),
                               output_format='pandas')
        assert isinstance(df, DataFrame)
        assert len(df) == 2

    def test_summary_fails_no_params(self):
        with pytest.raises(ValueError):
            get_stats_summary()

        with pytest.raises(ValueError):
            get_stats_summary(end=datetime(2017, 1, 1))

    def test_summary_invalid_start_date(self):
        with pytest.raises(ValueError):
            get_stats_summary(start=datetime(2011, 1, 1))

        with pytest.raises(ValueError):
            get_stats_summary(start=datetime(2022, 1, 1))

    def test_summary_invalid_end_date(self):
        with pytest.raises(ValueError):
            get_stats_summary(start=datetime(2017, 1, 1))

        with pytest.raises(ValueError):
            get_stats_summary(start=datetime(2017, 1, 1), end=datetime(2016, 1,
                              1))

        with pytest.raises(ValueError):
            get_stats_summary(start=datetime(2017, 1, 1), end=datetime(2028, 1,
                              1))
