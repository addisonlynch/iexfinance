from datetime import datetime

import pytest

from iexfinance.iexdata import (
    get_tops,
    get_last,
    get_deep,
    get_deep_book,
    get_stats_intraday,
    get_stats_recent,
    get_stats_records,
    get_stats_daily,
    get_stats_summary,
)


class TestMarketData(object):
    def setup_class(self):
        self.bad = [
            "AAPL",
            "TSLA",
            "MSFT",
            "F",
            "GOOGL",
            "STM",
            "DAL",
            "UVXY",
            "SPY",
            "DIA",
            "SVXY",
            "CMG",
            "LUV",
        ]

    @pytest.mark.xfail(reason="Market data only available during market open")
    def test_last_json_default(self):
        ls = get_last()

        assert isinstance(ls, list) and len(ls) > 7500

    @pytest.mark.xfail(reason="Market data only available during market open")
    def test_last_syms(self):
        ls = get_last("AAPL")
        ls2 = get_last(["AAPL", "TSLA"])

        assert isinstance(ls, list) and len(ls) == 1
        assert isinstance(ls2, list) and len(ls2) == 2

    def test_last_too_many_symbols(self):
        with pytest.raises(ValueError):
            get_last(self.bad)

    @pytest.mark.xfail(reason="Market data only available during market open")
    def test_TOPS_json_default(self):
        ls = get_tops()

        assert isinstance(ls, list) and len(ls) > 7500

    @pytest.mark.xfail(reason="Market data only available during market open")
    def test_TOPS_syms(self):
        ls = get_tops("AAPL")
        ls2 = get_tops(["AAPL", "TSLA"])

        assert isinstance(ls, list) and len(ls) == 1
        assert isinstance(ls2, list) and len(ls2) == 2

    def test_TOPS_too_many_symbols(self):
        with pytest.raises(ValueError):
            get_tops(self.bad)

    @pytest.mark.xfail(reason="Market data only available during market open")
    def test_DEEP_default(self):
        with pytest.raises(ValueError):
            get_deep()

    @pytest.mark.xfail(reason="Market data only available during market open")
    def test_DEEP_syms(self):
        js = get_deep("AAPL")

        assert isinstance(js, dict)

    def test_DEEP_too_many_syms(self):
        with pytest.raises(ValueError):
            get_deep(["AAPL", "TSLA"])

    def test_Book_default(self):
        with pytest.raises(ValueError):
            get_deep_book()

    @pytest.mark.xfail(reason="Market data only available during market open")
    def test_Book_syms(self):
        js = get_deep_book("AAPL")
        js2 = get_deep_book(["AAPL", "TSLA"])

        assert isinstance(js, dict) and len(js) == 1
        assert isinstance(js2, dict) and len(js2) == 2

    def test_Book_too_many_symbols(self):
        with pytest.raises(ValueError):
            get_deep_book(self.bad)


class TestStats(object):
    def test_intraday(self):
        js = get_stats_intraday()
        assert isinstance(js, dict)

    @pytest.mark.xfail(reason="IEX recent API endpoint unstable.")
    def test_recent(self):
        ls = get_stats_recent()
        assert isinstance(ls, list)

    def test_records(self):
        js = get_stats_records()
        assert isinstance(js, dict)


@pytest.mark.xfail(reason="Endpoint in development by provider.")
class TestStatsDaily(object):
    def test_daily_last(self):
        ls = get_stats_daily(last=5)
        assert isinstance(ls, list)
        assert len(ls) == 5

    def test_daily_dates(self):
        ls = get_stats_daily(start=datetime(2017, 1, 1), end=datetime(2017, 2, 1))
        assert isinstance(ls, list)
        assert len(ls) == 31

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
            get_stats_daily(start=datetime(2017, 1, 1), end=datetime(2016, 1, 1))

        with pytest.raises(ValueError):
            get_stats_daily(start=datetime(2017, 1, 1), end=datetime(2028, 1, 1))


class TestStatsSummary(object):
    def test_summary(self):
        ls = get_stats_summary(start=datetime(2017, 1, 1), end=datetime(2017, 2, 1))
        assert isinstance(ls, list)
        assert len(ls) == 1

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
            get_stats_summary(start=datetime(2017, 1, 1), end=datetime(2016, 1, 1))

        with pytest.raises(ValueError):
            get_stats_summary(start=datetime(2017, 1, 1), end=datetime(2028, 1, 1))
