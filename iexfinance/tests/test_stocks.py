from datetime import datetime

import pytest
import pandas as pd
from pandas.util.testing import assert_index_equal

from decimal import Decimal

from iexfinance.stocks import (get_historical_data, get_market_gainers,
                               get_market_losers, get_market_most_active,
                               get_market_iex_volume, get_market_iex_percent,
                               get_market_in_focus, get_sector_performance,
                               get_collections, get_crypto_quotes,
                               get_todays_earnings, get_ipo_calendar,
                               get_historical_intraday, Stock)
from iexfinance.utils.exceptions import IEXSymbolError, IEXEndpointError

import six


class TestBase(object):

    def test_wrong_iex_input_type(self):
        with pytest.raises(ValueError):
            Stock(34)
        with pytest.raises(ValueError):
            Stock("")
        with pytest.raises(ValueError):
            ls = []
            Stock(ls)

    def test_symbol_list_too_long(self):
        with pytest.raises(ValueError):
            x = ["tsla"] * 102
            Stock(x)


class TestShareDefault(object):

    def setup_class(self):
        self.cshare = Stock("aapl")
        self.cshare2 = Stock("aapl", output_format='pandas')
        self.cshare3 = Stock("svxy")
        self.cshare4 = Stock("aapl",
                             json_parse_int=Decimal,
                             json_parse_float=Decimal)
        self.cshare5 = Stock("gig^")

    @pytest.mark.xfail(reason="Unstable.")
    @pytest.mark.legacy
    def test_invalid_symbol(self):
        data = Stock("BAD SYMBOL")
        with pytest.raises(IEXSymbolError):
            data.get_price()

    @pytest.mark.xfail(reason="Unstable")
    @pytest.mark.legacy
    def test_get_all_format(self):
        data = self.cshare.get_all()
        assert isinstance(data, dict)

    @pytest.mark.xfail(reason="Unstable.")
    @pytest.mark.legacy
    def test_get_all(self):
        data = self.cshare.get_all()
        assert len(data) == 20

    def test_get_endpoints(self):
        data = self.cshare.get_endpoints(["price"])
        assert list(data) == ["price"]

    def test_get_endpoints_bad_endpoint(self):
        with pytest.raises(IEXEndpointError):
            self.cshare.get_endpoints(["BAD ENDPOINT", "quote"])

        with pytest.raises(IEXEndpointError):
            self.cshare.get_endpoints("BAD ENDPOINT")

    @pytest.mark.cloudbroken
    def test_get_book_format(self):
        data = self.cshare.get_book()
        assert isinstance(data, dict)

        data2 = self.cshare2.get_book()
        assert isinstance(data2, pd.DataFrame)

    def test_get_chart_format(self):
        data = self.cshare.get_chart()
        assert isinstance(data, list)

        data2 = self.cshare2.get_chart()
        assert isinstance(data2, pd.DataFrame)

    def test_get_chart_params(self):
        data = self.cshare.get_chart()
        # Test chart ranges
        data2 = self.cshare.get_chart(range='1y')
        assert 15 < len(data) < 35
        assert 240 < len(data2) < 260

        # Test chartSimplify
        data4 = self.cshare.get_chart(chartSimplify=True)[0]
        assert "simplifyFactor" in list(data4)

        data5 = self.cshare.get_chart(range='1y', chartInterval=5)
        assert 45 < len(data5) < 55

    def test_get_chart_pandas(self):
        data = self.cshare2.get_chart()

        assert isinstance(data, pd.DataFrame)
        assert isinstance(data.index, pd.DatetimeIndex)
        assert "open" in data.columns

    @pytest.mark.xfail(reason="This test only runs correctly between 00:00 and"
                       "09:30 EST")
    def test_get_chart_reset(self):
        # Test chartReset
        data3 = self.cshare.get_chart(range='1d', chartReset=True)
        assert data3 == []

    def test_get_company_format(self):
        data = self.cshare.get_company()
        assert isinstance(data, dict)

        data2 = self.cshare2.get_company()
        assert isinstance(data2, pd.DataFrame)

    def test_get_delayed_quote_format(self):
        data = self.cshare.get_delayed_quote()
        assert isinstance(data, dict)

        data2 = self.cshare2.get_delayed_quote()
        assert isinstance(data2, pd.DataFrame)

    def test_get_dividends_format(self):
        data = self.cshare.get_dividends(range='1y')
        assert isinstance(data, list)

        data2 = self.cshare2.get_dividends(range='1y')
        assert isinstance(data2, pd.DataFrame)

    def test_get_dividends_params(self):
        data = self.cshare.get_dividends()
        data2 = self.cshare.get_dividends(range='2y')
        data3 = self.cshare.get_dividends(range='5y')
        assert len(data) < len(data2) < len(data3)

    def test_get_dividends_pandas(self):
        data = self.cshare2.get_dividends(range='5y')
        assert isinstance(data, pd.DataFrame)
        assert "amount" in data.columns
        assert "flag" in data.columns
        assert isinstance(data.index, pd.DatetimeIndex)

    @pytest.mark.highweight
    def test_get_earnings_format(self):
        # weight: 3000
        data = self.cshare.get_earnings()
        assert isinstance(data, list)

        data2 = self.cshare2.get_earnings()
        assert isinstance(data2, pd.DataFrame)

        # Ensure empty list is returned for symbol with no earnings
        data3 = self.cshare5.get_earnings()
        assert isinstance(data3, list)

    @pytest.mark.highweight
    def test_get_earnings_pandas(self):
        # weight: 1000
        data = self.cshare2.get_earnings()
        assert "actualEPS" in data.columns
        # 9 for iexcloud, 13 for v1
        assert len(data.columns) in (10, 12)

    def test_get_effective_spread_format(self):
        data = self.cshare.get_effective_spread()
        assert isinstance(data, list)

        data2 = self.cshare2.get_effective_spread()
        assert isinstance(data2, pd.DataFrame)

    @pytest.mark.highweight
    def test_get_financials_format(self):
        # weight: 15000
        data = self.cshare.get_financials()
        assert isinstance(data, list)

        data2 = self.cshare2.get_financials()
        assert isinstance(data2, pd.DataFrame)

        # Ensure empty list is returned even when ticker has no financials
        data3 = self.cshare5.get_financials()
        assert isinstance(data3, list)

    def test_get_key_stats_format(self):
        data = self.cshare.get_key_stats()
        assert isinstance(data, dict)

        data2 = self.cshare2.get_key_stats()
        assert isinstance(data2, pd.DataFrame)

    def test_get_largest_trades(self):
        data = self.cshare.get_largest_trades()
        assert isinstance(data, list)

        data2 = self.cshare2.get_largest_trades()
        assert isinstance(data2, pd.DataFrame)

    def test_get_logo_format(self):
        data = self.cshare.get_logo()
        assert isinstance(data, dict)

        data2 = self.cshare2.get_logo()
        assert isinstance(data2, pd.DataFrame)

    def test_get_news_format(self):
        data = self.cshare.get_news()
        assert isinstance(data, list)

    @pytest.mark.xfail(reason="Provider error. Awaiting patch.")
    def test_get_news_params(self):
        data = self.cshare.get_news(last=15)
        assert len(data) == 15

    def test_ohlc(self):
        data = self.cshare.get_ohlc()
        assert isinstance(data, dict)

        data2 = self.cshare2.get_ohlc()
        assert isinstance(data2, pd.DataFrame)

    def test_get_open_close_format(self):
        data = self.cshare.get_open_close()
        assert isinstance(data, dict)

        data2 = self.cshare2.get_open_close()
        assert isinstance(data2, pd.DataFrame)

    @pytest.mark.highweight
    def test_get_peers_format(self):
        # weight: 1000
        data = self.cshare.get_peers()
        assert isinstance(data, list)

        data2 = self.cshare2.get_peers()
        assert isinstance(data2, dict)

    def test_get_previous_format(self):
        data = self.cshare.get_previous()
        assert isinstance(data, dict)

        data2 = self.cshare2.get_previous()
        assert isinstance(data2, pd.DataFrame)

    def test_get_price_format(self):
        data = self.cshare.get_price()
        assert isinstance(data, (int, float))

        data2 = self.cshare2.get_price()
        assert isinstance(data2, pd.DataFrame)

        data4 = self.cshare4.get_price()
        assert isinstance(data4, Decimal)

    def test_get_quote_format(self):
        data = self.cshare.get_quote()
        assert isinstance(data, dict)

        data2 = self.cshare2.get_quote()
        assert isinstance(data2, pd.DataFrame)

    def test_get_quote_params(self):
        data = self.cshare.get_quote()
        data2 = self.cshare.get_quote(displayPercent=True)

        assert (abs(data2["ytdChange"]) >
                abs(data["ytdChange"]))

    @pytest.mark.highweight
    def test_get_relevant_format(self):
        # weight: 1000
        data = self.cshare.get_relevant()
        assert isinstance(data, dict)

        data2 = self.cshare2.get_relevant()
        assert isinstance(data2, pd.DataFrame)

    def test_get_splits_format(self):
        data = self.cshare3.get_splits()
        assert isinstance(data, list)

        data2 = self.cshare3.get_splits(range="1y")
        assert isinstance(data2, list)

    def test_get_splits_params(self):
        data = self.cshare3.get_splits(range="2y")
        data2 = self.cshare3.get_splits(range="5y")
        assert len(data2) > len(data)

    def test_get_time_series(self):
        data = self.cshare.get_time_series()
        data2 = self.cshare.get_chart()
        assert data == data2

    def test_get_volume_by_venue_format(self):
        data = self.cshare.get_volume_by_venue()
        assert isinstance(data, list)

        data2 = self.cshare2.get_volume_by_venue()
        assert isinstance(data2, pd.DataFrame)

    def test_filter(self):
        data = self.cshare.get_quote(filter_='ytdChange')
        assert isinstance(data, dict)
        assert isinstance(data["ytdChange"], (int, float))

        data4 = self.cshare4.get_quote(filter_='ytdChange')
        assert isinstance(data4, dict)
        assert isinstance(data4["ytdChange"], Decimal)


class TestBatchDefault(object):

    def setup_class(self):
        self.cbatch = Stock(["aapl", "tsla"])
        self.cbatch2 = Stock(["aapl", "tsla"], output_format='pandas')
        self.cbatch3 = Stock(["uvxy", "svxy"])

    def test_invalid_symbol_or_symbols(self):
        with pytest.raises(IEXSymbolError):
            a = Stock(["TSLA", "BAD SYMBOL", "BAD SYMBOL"])
            a.get_price()

    def test_get_endpoints(self):
        data = self.cbatch.get_endpoints(["price"])["AAPL"]
        assert list(data) == ["price"]

    def test_get_endpoints_bad_endpoint(self):
        with pytest.raises(IEXEndpointError):
            self.cbatch.get_endpoints(["BAD ENDPOINT", "quote"])

        with pytest.raises(IEXEndpointError):
            self.cbatch.get_endpoints("BAD ENDPOINT")

    @pytest.mark.legacy
    def test_get_all(self):
        data = self.cbatch.get_all()
        assert len(data) == 2
        assert len(data["AAPL"]) == 20

    @pytest.mark.legacy
    def test_get_all_format(self):
        data = self.cbatch.get_all()
        assert isinstance(data, dict)

        data2 = self.cbatch2.get_all()
        assert isinstance(data2["AAPL"], dict)

    @pytest.mark.cloudbroken
    def test_get_book_format(self):
        data = self.cbatch.get_book()
        assert isinstance(data, dict)

        data2 = self.cbatch2.get_book()
        assert isinstance(data2, pd.DataFrame)

    def test_get_chart_format(self):
        data = self.cbatch.get_chart()
        assert isinstance(data, dict)

        data2 = self.cbatch2.get_chart()
        assert isinstance(data2["AAPL"], pd.DataFrame)

    def test_get_chart_params(self):
        data = self.cbatch.get_chart()["AAPL"]
        # Test chart ranges
        data2 = self.cbatch.get_chart(range='1y')["AAPL"]
        assert 15 < len(data) < 35
        assert 240 < len(data2) < 260

        # Test chartSimplify
        data4 = self.cbatch.get_chart(chartSimplify=True)["AAPL"][0]
        assert "simplifyFactor" in list(data4)

        data5 = self.cbatch.get_chart(range='1y', chartInterval=5)["AAPL"]
        assert 45 < len(data5) < 55

    @pytest.mark.xfail(reason="This test only works overnight")
    def test_get_chart_reset(self):
        # Test chartReset
        data = self.cbatch.get_chart(range='1d', chartReset=True)
        assert data == []

    def test_get_company_format(self):
        data = self.cbatch.get_company()
        assert isinstance(data, dict)

        data2 = self.cbatch2.get_company()
        assert isinstance(data2, pd.DataFrame)

    def test_get_delayed_quote_format(self):
        data = self.cbatch.get_delayed_quote()
        assert isinstance(data, dict)

        data2 = self.cbatch2.get_delayed_quote()
        assert isinstance(data2, pd.DataFrame)

    def test_get_dividends_format(self):
        data = self.cbatch.get_dividends()
        assert isinstance(data, dict)

        data2 = self.cbatch2.get_dividends()
        assert isinstance(data2, dict)

    def test_get_dividends_params(self):
        data = self.cbatch.get_dividends()["AAPL"]
        data2 = self.cbatch.get_dividends(range='2y')["AAPL"]
        data3 = self.cbatch.get_dividends(range='5y')["AAPL"]
        assert len(data) < len(data2) < len(data3)

    @pytest.mark.highweight
    def test_get_earnings_format(self):
        # weight: 4000
        data = self.cbatch.get_earnings()
        assert isinstance(data, dict)

        data2 = self.cbatch2.get_earnings()
        assert isinstance(data2, dict)

    def test_get_effective_spread_format(self):
        data = self.cbatch.get_effective_spread()
        assert isinstance(data, dict)

        data2 = self.cbatch2.get_effective_spread()
        assert isinstance(data2, pd.DataFrame)

    @pytest.mark.highweight
    def test_get_financials_format(self):
        # weight: 10000
        data = self.cbatch.get_financials()
        assert isinstance(data, dict)

        data2 = self.cbatch2.get_financials()
        assert isinstance(data2, dict)

    def test_get_key_stats_format(self):
        data = self.cbatch.get_key_stats()
        assert isinstance(data, dict)

        data2 = self.cbatch2.get_key_stats()
        assert isinstance(data2, pd.DataFrame)

    def test_get_logo_format(self):
        data = self.cbatch.get_logo()
        assert isinstance(data, dict)

        data2 = self.cbatch2.get_logo()
        assert isinstance(data2, pd.DataFrame)

    def test_get_news_format(self):
        data = self.cbatch.get_news()
        assert isinstance(data, dict)

    def test_ohlc(self):
        data = self.cbatch.get_ohlc()
        assert isinstance(data, dict)

    def test_get_open_close_format(self):
        data = self.cbatch.get_open_close()
        assert isinstance(data, dict)

        data2 = self.cbatch2.get_open_close()
        assert isinstance(data2, pd.DataFrame)

    def test_get_peers_format(self):
        data = self.cbatch.get_peers()
        assert isinstance(data, dict)

        data2 = self.cbatch2.get_peers()
        assert isinstance(data2, dict)

    def test_get_previous_format(self):
        data = self.cbatch.get_previous()
        assert isinstance(data, dict)

        data2 = self.cbatch2.get_previous()
        assert isinstance(data2, pd.DataFrame)

    def test_get_price_format(self):
        data = self.cbatch.get_price()
        assert isinstance(data, dict)

        data2 = self.cbatch2.get_price()
        assert isinstance(data2, pd.DataFrame)

    def test_get_quote_format(self):
        data = self.cbatch.get_quote()
        assert isinstance(data, dict)

        data2 = self.cbatch2.get_quote()
        assert isinstance(data2, pd.DataFrame)

        data3 = self.cbatch.get_quote(displayPercent=True)
        assert (abs(data3["AAPL"]["ytdChange"]) >
                abs(data["AAPL"]["ytdChange"]))

    @pytest.mark.highweight
    def test_get_relevant_format(self):
        # weight: 1000
        data = self.cbatch.get_relevant()
        assert isinstance(data, dict)

        data2 = self.cbatch2.get_relevant()
        assert isinstance(data2, pd.DataFrame)

    def test_get_splits(self):
        data = self.cbatch.get_splits()
        assert isinstance(data, dict)

        data2 = self.cbatch2.get_splits()
        assert isinstance(data2, pd.DataFrame)

    def test_get_splits_params(self):
        data = self.cbatch3.get_splits(range="2y")["SVXY"]
        data2 = self.cbatch3.get_splits(range="5y")["SVXY"]
        assert len(data2) > len(data)

    def test_time_series(self):
        data = self.cbatch.get_time_series()
        data2 = self.cbatch.get_chart()
        assert data == data2

    def test_get_volume_by_venue_format(self):
        data = self.cbatch.get_volume_by_venue()
        assert isinstance(data, dict)

        data2 = self.cbatch2.get_volume_by_venue()
        assert isinstance(data2, pd.DataFrame)

    def test_get_select_ep_bad_params(self):
        with pytest.raises(IEXEndpointError):
            self.cbatch.get_endpoints()

        with pytest.raises(IEXEndpointError):
            self.cbatch.get_endpoints("BADENDPOINT")


class TestFieldMethodsShare(object):

    def setup_class(self):
        self.share = Stock("AAPL")
        self.share2 = Stock("AAPL", output_format='pandas')
        self.share4 = Stock("AAPL",
                            json_parse_int=Decimal,
                            json_parse_float=Decimal)
        self.share5 = Stock("TSLA")

    def test_get_company_name(self):
        data = self.share.get_company_name()

        assert isinstance(data, six.string_types)
        assert data == "Apple Inc."

        data2 = self.share2.get_company_name()
        assert isinstance(data2, pd.DataFrame)

    def test_get_primary_exchange(self):
        data = self.share.get_primary_exchange()
        assert isinstance(data, six.string_types)
        assert data == "Nasdaq Global Select"

        data2 = self.share2.get_primary_exchange()
        assert isinstance(data2, pd.DataFrame)

    def test_get_sector(self):
        data = self.share.get_sector()

        assert isinstance(data, six.string_types)
        assert data == "Technology"

        data2 = self.share2.get_sector()
        assert isinstance(data2, pd.DataFrame)

    def test_get_open(self):
        data = self.share.get_open()
        assert isinstance(data, (int, float))
        assert data > 0

        data2 = self.share2.get_open()
        assert isinstance(data2, pd.DataFrame)
        assert data2["AAPL"].iloc[0].dtype in ("int64", "float64")

        data4 = self.share4.get_open()
        assert isinstance(data4, Decimal)
        assert data4 > 0

    def test_get_close(self):
        data = self.share.get_close()
        assert isinstance(data, (int, float))
        assert data > 0

        data2 = self.share2.get_close()
        assert isinstance(data2, pd.DataFrame)
        assert data2["AAPL"].iloc[0].dtype in ("int64", "float64")

        data4 = self.share4.get_close()
        assert isinstance(data4, Decimal)
        assert data4 > 0

    def test_get_years_high(self):
        data = self.share.get_years_high()
        assert isinstance(data, (int, float))
        assert data > 0

        data2 = self.share2.get_years_high()
        assert isinstance(data2, pd.DataFrame)
        assert data2["AAPL"].iloc[0].dtype in ("int64", "float64")

        data4 = self.share4.get_years_high()
        assert isinstance(data4, Decimal)
        assert data4 > 0

    def test_get_years_low(self):
        data = self.share.get_years_low()
        assert isinstance(data, (int, float))
        assert data > 0

        data2 = self.share2.get_years_low()
        assert isinstance(data2, pd.DataFrame)
        assert data2["AAPL"].iloc[0].dtype in ("float64", "int64")

        data4 = self.share4.get_years_low()
        assert isinstance(data4, Decimal)
        assert data4 > 0

    def test_get_ytd_change(self):
        data = self.share.get_ytd_change()
        assert isinstance(data, (int, float))

        data2 = self.share2.get_ytd_change()
        assert isinstance(data2, pd.DataFrame)
        assert data2["AAPL"].iloc[0].dtype in ("int64", "float64")

        data4 = self.share4.get_ytd_change()
        assert isinstance(data4, Decimal)

    def test_get_volume(self):
        data = self.share.get_volume()
        assert isinstance(data, int)
        assert data > 1000

        data2 = self.share2.get_volume()
        assert isinstance(data2, pd.DataFrame)
        assert data2["AAPL"].iloc[0].dtype == "int64"

        data4 = self.share4.get_volume()
        assert isinstance(data4, Decimal)
        assert data4 > 1000

    def test_get_market_cap(self):
        data = self.share.get_market_cap()
        assert isinstance(data, int)

        data2 = self.share2.get_market_cap()
        assert isinstance(data2, pd.DataFrame)
        assert data2["AAPL"].iloc[0].dtype == "int64"

        data4 = self.share4.get_market_cap()
        assert isinstance(data4, Decimal)

    def test_get_beta(self):
        data = self.share.get_beta()
        assert isinstance(data, (int, float))

        data2 = self.share2.get_beta()
        assert isinstance(data2, pd.DataFrame)
        assert data2["AAPL"].iloc[0].dtype in ("int64", "float64")

        data4 = self.share4.get_beta()
        assert isinstance(data4, Decimal)

    @pytest.mark.xfail(reason="Not available outside of market open days.")
    def test_get_short_interest(self):
        data = self.share.get_short_interest()
        assert isinstance(data, int)

        data2 = self.share2.get_short_interest()
        assert isinstance(data2, pd.DataFrame)
        assert data2["AAPL"].iloc[0].dtype == "int64"

        data4 = self.share4.get_short_interest()
        assert isinstance(data4, Decimal)

    @pytest.mark.xfail(reason="Not available outside of market open days.")
    def test_get_short_ratio(self):
        data = self.share.get_short_ratio()
        assert isinstance(data, (int, float))

        data2 = self.share2.get_short_ratio()
        assert isinstance(data2, pd.DataFrame)
        assert data2["AAPL"].iloc[0].dtype in ("int64", "float64")

        data4 = self.share4.get_short_ratio()
        assert isinstance(data4, Decimal)

    def test_get_latest_eps(self):
        data = self.share5.get_latest_eps()
        assert isinstance(data, (int, float))

        data4 = self.share4.get_latest_eps()
        assert isinstance(data4, Decimal)

    def test_get_shares_outstanding(self):
        data = self.share.get_shares_outstanding()
        assert isinstance(data, int)

        data2 = self.share2.get_shares_outstanding()
        assert isinstance(data2, pd.DataFrame)
        assert data2["AAPL"].iloc[0].dtype == "int64"

        data4 = self.share4.get_shares_outstanding()
        assert isinstance(data4, Decimal)

    def test_get_float(self):
        data = self.share.get_float()
        assert isinstance(data, int)

        data2 = self.share2.get_float()
        assert isinstance(data2, pd.DataFrame)
        assert data2["AAPL"].iloc[0].dtype == "int64"

        data4 = self.share4.get_float()
        assert isinstance(data4, Decimal)

    def test_get_eps_consensus(self):
        data = self.share.get_eps_consensus()
        assert isinstance(data, (int, float))

        data2 = self.share2.get_eps_consensus()
        assert isinstance(data2, pd.DataFrame)
        assert data2["AAPL"].iloc[0].dtype in ("int64", "float64")

        data4 = self.share4.get_eps_consensus()
        assert isinstance(data4, Decimal)


class TestFieldMethodsBatch(object):

    def setup_class(self):
        self.batch = Stock(["AAPL", "TSLA"])
        self.batch2 = Stock(["AAPL", "TSLA"], output_format='pandas')
        self.batch4 = Stock(["AAPL", "TSLA"],
                            json_parse_int=Decimal,
                            json_parse_float=Decimal)

    def test_get_company_name(self):
        data = self.batch.get_company_name()
        assert isinstance(data, dict)
        assert data["AAPL"] == "Apple Inc."

        data2 = self.batch2.get_company_name()
        assert isinstance(data2, pd.DataFrame)
        assert_index_equal(data2.columns, pd.Index(self.batch2.symbols))

    def test_get_primary_exchange(self):
        data = self.batch.get_primary_exchange()
        assert isinstance(data, dict)
        assert data["AAPL"] == "Nasdaq Global Select"

        data2 = self.batch2.get_primary_exchange()
        assert isinstance(data2, pd.DataFrame)
        assert_index_equal(data2.columns, pd.Index(self.batch2.symbols))

    def test_get_sector(self):
        data = self.batch.get_sector()
        assert isinstance(data, dict)
        assert data["AAPL"] == "Technology"

        data2 = self.batch2.get_sector()
        assert isinstance(data2, pd.DataFrame)
        assert_index_equal(data2.columns, pd.Index(self.batch2.symbols))

    def test_get_open(self):
        data = self.batch.get_open()
        assert isinstance(data, dict)
        assert data["AAPL"] > 0

        data2 = self.batch2.get_open()
        assert isinstance(data2, pd.DataFrame)
        assert_index_equal(data2.columns, pd.Index(self.batch2.symbols))
        assert data2["AAPL"].iloc[0].dtype in ("int64", "float64")

    def test_get_close(self):
        data = self.batch.get_close()
        assert isinstance(data, dict)
        assert data["AAPL"] > 0

        data2 = self.batch2.get_close()
        assert isinstance(data2, pd.DataFrame)
        assert_index_equal(data2.columns, pd.Index(self.batch2.symbols))
        assert data2["AAPL"].iloc[0].dtype in ("int64", "float64")

    def test_get_years_high(self):
        data = self.batch.get_years_high()
        assert isinstance(data, dict)
        assert data["AAPL"] > 0

        data2 = self.batch2.get_years_high()
        assert isinstance(data2, pd.DataFrame)
        assert_index_equal(data2.columns, pd.Index(self.batch2.symbols))
        assert data2["AAPL"].iloc[0].dtype in ("int64", "float64")

    def test_get_years_low(self):
        data = self.batch.get_years_low()
        assert isinstance(data, dict)
        assert data["AAPL"] > 0

        data2 = self.batch2.get_years_low()
        assert isinstance(data2, pd.DataFrame)
        assert_index_equal(data2.columns, pd.Index(self.batch2.symbols))
        assert data2["AAPL"].iloc[0].dtype in ("int64", "float64")

    def test_get_ytd_change(self):
        data = self.batch.get_ytd_change()
        assert isinstance(data, dict)

        data2 = self.batch2.get_ytd_change()
        assert isinstance(data2, pd.DataFrame)
        assert_index_equal(data2.columns, pd.Index(self.batch2.symbols))
        assert data2["AAPL"].iloc[0].dtype in ("int64", "float64")

    def test_get_volume(self):
        data = self.batch.get_volume()
        assert isinstance(data, dict)
        assert data["AAPL"] > 50000

        data2 = self.batch2.get_volume()
        assert isinstance(data2, pd.DataFrame)
        assert_index_equal(data2.columns, pd.Index(self.batch2.symbols))
        assert data2["AAPL"].iloc[0].dtype == "int64"

    def test_get_market_cap(self):
        data = self.batch.get_market_cap()
        assert isinstance(data, dict)
        assert data["AAPL"] > 1000000

        data2 = self.batch2.get_market_cap()
        assert isinstance(data2, pd.DataFrame)
        assert_index_equal(data2.columns, pd.Index(self.batch2.symbols))
        assert data2["AAPL"].iloc[0].dtype == "int64"

    def test_get_beta(self):
        data = self.batch.get_beta()
        assert isinstance(data, dict)
        assert isinstance(data["AAPL"], (int, float))

        data2 = self.batch2.get_beta()
        assert isinstance(data2, pd.DataFrame)
        assert_index_equal(data2.columns, pd.Index(self.batch2.symbols))
        assert data2["AAPL"].iloc[0].dtype in ("int64", "float64")

        data4 = self.batch4.get_beta()
        assert isinstance(data4, dict)
        assert isinstance(data4["AAPL"], Decimal)

    @pytest.mark.xfail(reason="Not available outside of market open days.")
    def test_get_short_interest(self):
        data = self.batch.get_short_interest()
        assert isinstance(data, dict)
        assert data["AAPL"] > 50000

        data2 = self.batch2.get_short_interest()
        assert isinstance(data2, pd.DataFrame)
        assert_index_equal(data2.columns, pd.Index(self.batch2.symbols))
        assert data2["AAPL"].iloc[0].dtype == "int64"

    @pytest.mark.xfail(reason="Not available outside of market open days.")
    def test_get_short_ratio(self):
        data = self.batch.get_short_ratio()
        assert isinstance(data, dict)
        assert isinstance(data["AAPL"], (int, float))

        data2 = self.batch2.get_short_ratio()
        assert isinstance(data2, pd.DataFrame)
        assert_index_equal(data2.columns, pd.Index(self.batch2.symbols))
        assert data2["AAPL"].iloc[0].dtype in ("int64", "float64")

        data4 = self.batch4.get_short_ratio()
        assert isinstance(data4, dict)
        assert isinstance(data4["AAPL"], Decimal)

    def test_get_latest_eps(self):
        data = self.batch.get_latest_eps()
        assert isinstance(data, dict)
        assert isinstance(data["TSLA"], (int, float))

        data2 = self.batch2.get_latest_eps()
        assert isinstance(data2, pd.DataFrame)
        assert_index_equal(data2.columns, pd.Index(self.batch2.symbols))
        assert data2["TSLA"].dtype in ("int64", "float64")

        data4 = self.batch4.get_latest_eps()
        assert isinstance(data4, dict)
        assert isinstance(data4["AAPL"], Decimal)

    def test_get_shares_outstanding(self):
        data = self.batch.get_shares_outstanding()
        assert isinstance(data, dict)
        assert data["AAPL"] > 100000

        data2 = self.batch2.get_shares_outstanding()
        assert isinstance(data2, pd.DataFrame)
        assert_index_equal(data2.columns, pd.Index(self.batch2.symbols))
        assert data2["AAPL"].iloc[0].dtype == "int64"

    def test_get_float(self):
        data = self.batch.get_float()
        assert isinstance(data, dict)
        assert data["AAPL"] > 1000000

        data2 = self.batch2.get_float()
        assert isinstance(data2, pd.DataFrame)
        assert_index_equal(data2.columns, pd.Index(self.batch2.symbols))
        assert data2["AAPL"].iloc[0].dtype == "int64"

    def test_get_eps_consensus(self):
        data = self.batch.get_eps_consensus()
        assert isinstance(data, dict)
        assert isinstance(data["AAPL"], (int, float))

        data2 = self.batch2.get_eps_consensus()
        assert isinstance(data2, pd.DataFrame)
        assert_index_equal(data2.columns, pd.Index(self.batch2.symbols))
        assert data2["AAPL"].iloc[0].dtype in ("int64", "float64")

        data4 = self.batch4.get_eps_consensus()
        assert isinstance(data4, dict)
        assert isinstance(data4["AAPL"], Decimal)


class TestHistorical(object):

    def setup_class(self):
        self.good_start = datetime(2017, 2, 9)
        self.good_end = datetime(2017, 5, 24)

    def test_single_historical_json(self):

        f = get_historical_data("AMZN", self.good_start, self.good_end)
        assert isinstance(f, dict)
        assert len(f) == 73

        expected1 = f["2017-02-09"]
        assert expected1["close"] == pytest.approx(821.36, 3)
        assert expected1["high"] == pytest.approx(825.0, 3)

        expected2 = f["2017-05-24"]
        assert expected2["close"] == pytest.approx(980.35, 3)
        assert expected2["high"] == pytest.approx(981.0, 3)

    def test_single_historical_pandas(self):

        f = get_historical_data("AMZN", self.good_start, self.good_end,
                                output_format="pandas")

        assert isinstance(f, pd.DataFrame)
        assert isinstance(f.index, pd.DatetimeIndex)
        assert len(f) == 73

        expected1 = f.loc["2017-02-09"]
        assert expected1["close"] == pytest.approx(821.36, 3)
        assert expected1["high"] == pytest.approx(825.0, 3)

        expected2 = f.loc["2017-05-24"]
        assert expected2["close"] == pytest.approx(980.35, 3)
        assert expected2["high"] == pytest.approx(981.0, 3)

    def test_batch_historical_json(self):

        f = get_historical_data(["AMZN", "TSLA"], self.good_start,
                                self.good_end, output_format="json")

        assert isinstance(f, dict)
        assert len(f) == 2
        assert sorted(list(f)) == ["AMZN", "TSLA"]

        a = f["AMZN"]
        t = f["TSLA"]

        assert len(a) == 73
        assert len(t) == 73

        expected1 = a["2017-02-09"]
        assert expected1["close"] == pytest.approx(821.36, 3)
        assert expected1["high"] == pytest.approx(825.0, 3)

        expected2 = a["2017-05-24"]
        assert expected2["close"] == pytest.approx(980.35, 3)
        assert expected2["high"] == pytest.approx(981.0, 3)

        expected1 = t["2017-02-09"]
        assert expected1["close"] == pytest.approx(269.20, 3)
        assert expected1["high"] == pytest.approx(271.18, 3)

        expected2 = t["2017-05-24"]
        assert expected2["close"] == pytest.approx(310.22, 3)
        assert expected2["high"] == pytest.approx(311.0, 3)

    def test_batch_historical_pandas(self):

        f = get_historical_data(["AMZN", "TSLA"], self.good_start,
                                self.good_end, output_format="pandas")

        assert isinstance(f, pd.DataFrame)
        assert len(f) == 73
        assert sorted(list(f.columns.levels[0])) == ["AMZN", "TSLA"]

        a = f["AMZN"]
        t = f["TSLA"]

        assert len(a) == 73
        assert len(t) == 73

        expected1 = a.loc["2017-02-09"]
        assert expected1["close"] == pytest.approx(821.36, 3)
        assert expected1["high"] == pytest.approx(825.0, 3)

        expected2 = a.loc["2017-05-24"]
        assert expected2["close"] == pytest.approx(980.35, 3)
        assert expected2["high"] == pytest.approx(981.0, 3)

        expected1 = t.loc["2017-02-09"]
        assert expected1["close"] == pytest.approx(269.20, 3)
        assert expected1["high"] == pytest.approx(271.18, 3)

        expected2 = t.loc["2017-05-24"]
        assert expected2["close"] == pytest.approx(310.22, 3)
        assert expected2["high"] == pytest.approx(311.0, 3)

    def test_invalid_dates(self):
        start = datetime(2010, 5, 9)
        end = datetime(2017, 5, 9)
        with pytest.raises(ValueError):
            get_historical_data("AAPL", start, end)

    def test_invalid_dates_batch(self):
        start = datetime(2010, 5, 9)
        end = datetime(2017, 5, 9)
        with pytest.raises(ValueError):
            get_historical_data(["AAPL", "TSLA"], start, end)

    def test_invalid_symbol_batch(self):
        start = datetime(2017, 2, 9)
        end = datetime(2017, 5, 24)
        with pytest.raises(IEXSymbolError):
            get_historical_data(["BADSYMBOL", "TSLA"], start, end)

    def test_invalid_symbol_single(self):
        with pytest.raises(IEXSymbolError):
            get_historical_data("ZNWAA")


class TestMarketMovers(object):

    def test_market_gainers(self):
        li = get_market_gainers()
        assert len(li) == pytest.approx(10, 1)

    def test_market_losers(self):
        li = get_market_losers()
        assert len(li) == pytest.approx(10, 1)

    def test_market_most_active(self):
        li = get_market_most_active()
        assert len(li) == pytest.approx(10, 1)

    def test_market_iex_volume(self):
        li = get_market_iex_volume()
        assert len(li) == pytest.approx(10, 1)

    def test_market_iex_percent(self):
        li = get_market_iex_percent()
        assert len(li) == pytest.approx(10, 1)

    def test_market_in_focus(self):
        li = get_market_in_focus()
        assert len(li) == pytest.approx(10, 1)


@pytest.mark.legacy
class TestCrypto(object):

    def setup_class(self):
        self.ticks = ["BTCUSDT", "EOSUSDT", "ETHUSDT", "BNBUSDT", "ONTUSDT",
                      "BCCUSDT", "ADAUSDT", "XRPUSDT", "TUSDUSDT", "TRXUSDT",
                      "LTCUSDT", "ETCUSDT", "IOTAUSDT", "ICXUSDT", "NEOUSDT",
                      "VENUSDT", "XLMUSDT", "QTUMUSDT"]

    def test_listed_crypto_symbols(self):
        a = Stock(self.ticks)
        assert isinstance(a.get_quote(), dict)

    def test_get_crypto_quotes(self):
        data = get_crypto_quotes()
        assert isinstance(data, list)

    def test_get_cypto_quotes_pandas(self):
        data = get_crypto_quotes(output_format='pandas')
        assert isinstance(data, pd.DataFrame)

        assert len(data) == 43
        assert data.loc["sector"][0] == "cryptocurrency"


class TestSectorPerformance(object):

    def test_list_sector_performance(self):
        li = get_sector_performance()
        assert len(li) == pytest.approx(10, 1)


@pytest.mark.cloudbroken
class TestCollections(object):

    def test_get_collections_no_collection(self):
        with pytest.raises(TypeError):
            get_collections()

        with pytest.raises(ValueError):
            get_collections("Computer Hardware", "badcollection")

    def test_get_collections(self):
        data = get_collections("Computer Hardware")

        assert isinstance(data, list)
        assert len(data) > 100

    def test_get_collections_pandas(self):
        df = get_collections("Computer Hardware", output_format='pandas')

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 39

        assert "change" in df.index
        assert "close" in df.index

    def test_get_collections_type(self):
        df = get_collections("Industrials", "sector", output_format='pandas')
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 39
        assert len(df.columns) > 500


class TestTodaysEarnings(object):

    def test_get_todays_earnings(self):
        data = get_todays_earnings()

        assert isinstance(data, dict)
        assert "bto" in data
        assert "amc" in data


class TestIPOCalendar(object):

    def test_get_ipo_calendar_default(self):
        data = get_ipo_calendar()

        assert isinstance(data, dict)
        assert set(data) == set(["rawData", "viewData"])

        assert isinstance(data["rawData"], list)
        assert isinstance(data["viewData"], list)

    def test_get_ipo_calendar_today(self):
        data = get_ipo_calendar("today-ipos")

        assert isinstance(data, dict)
        assert len(data) == 3
        assert "lastUpdate" in data

    def test_ipo_calendar_bad_period(self):
        with pytest.raises(ValueError):
            get_ipo_calendar("BADPERIOD")


class TestHistoricalIntraday(object):

    def verify_timeframe(self, data):
        assert data.index[0].hour == 9
        assert data.index[0].minute == 30
        assert data.index[-1].hour == 15
        assert data.index[-1].minute == 59

    def test_intraday_fails_no_symbol(self):
        with pytest.raises(TypeError):
            get_historical_intraday()

    def test_intraday_default(self):
        data = get_historical_intraday("AAPL")

        assert isinstance(data, list)

    def test_intraday_pandas(self):
        data = get_historical_intraday("AAPL", output_format='pandas')

        assert isinstance(data, pd.DataFrame)
        assert isinstance(data.index, pd.DatetimeIndex)

        self.verify_timeframe(data)

    def test_intraday_pandas_pass_datetime(self):
        u_date = "20190102"
        data = get_historical_intraday("AAPL", date=u_date,
                                       output_format='pandas')

        assert isinstance(data, pd.DataFrame)
        assert data.index[0].strftime("%Y%m%d") == u_date

        self.verify_timeframe(data)

    def test_intraday_pass_date_str(self):
        data = get_historical_intraday("AAPL", date="20190102")

        assert isinstance(data, list)

    def test_intraday_pass_datetime(self):
        date = datetime(2018, 10, 27)

        data = get_historical_intraday("AAPL", date=date)

        assert isinstance(data, list)


@pytest.mark.cloud
class TestMarketVolume(object):
    pass


@pytest.mark.cloud
class TestMarketCloud(object):
    """
    Dev note: These are very rudimentary tests which check output formatting
    only.They will need to be made more robust
    """
    def setup_class(self):
        self.stock = Stock("AAPL")
        self.p_stock = Stock("AAPL", output_format='pandas')

    @pytest.mark.highweight
    def test_get_balance_sheet(self):
        # weight: 3000
        data = self.stock.get_balance_sheet()

        assert isinstance(data, dict)

    @pytest.mark.highweight
    def test_get_balance_sheet_pandas(self):
        # weight: 3000
        data = self.p_stock.get_balance_sheet()

        assert isinstance(data, pd.DataFrame)
        assert len(data) == 27
        assert data.columns == "AAPL"

    @pytest.mark.highweight
    def test_get_balance_sheet_batch(self):
        # weight: 6000
        stock = Stock(["AAPL", "TSLA"])
        data = stock.get_balance_sheet()

        assert isinstance(data, dict)
        assert "AAPL" in data
        assert "TSLA" in data

    @pytest.mark.highweight
    def test_get_balance_sheet_b_pandas(self):
        # weight: 6000
        stock = Stock(["AAPL", "TSLA"])
        data = stock.get_balance_sheet()

        assert isinstance(data, pd.DataFrame)
        assert data.shape == (27, 2)
        assert "AAPL" in data
        assert "TSLA" in data.columns

    @pytest.mark.highweight
    def test_get_cash_flow(self):
        # weight: 1000
        data = self.stock.get_cash_flow()

        assert isinstance(data, dict)
        assert len(data) == 2
        assert "symbol" in data
        assert "cashflow" in data
        assert isinstance(data["cashflow"], list)

    @pytest.mark.highweight
    def test_get_cash_flow_pandas(self):
        # weight: 1000
        data = self.p_stock.get_cash_flow()

        assert isinstance(data, pd.DataFrame)
        assert data.shape == (16, 1)
        assert "AAPL" in data

    @pytest.mark.highweight
    def test_batch_cash_flow_pandas(self):
        # weight: 2000
        stock = Stock(["AAPL", "TSLA"], output_format='pandas')
        data = stock.get_cash_flow()

        assert isinstance(data, pd.DataFrame)
        assert data.shape == (16, 2)
        assert "AAPL" in data

    @pytest.mark.highweight
    def test_get_estimates(self):
        # weight: 10000
        data = self.stock.get_estimates()

        assert isinstance(data, dict)

    def test_get_price_target(self):
        data = self.stock.get_price_target()

        assert isinstance(data, dict)

    def test_get_price_target_pandas(self):
        data = self.p_stock.get_price_target()

        assert isinstance(data, pd.DataFrame)
        assert data.shape == (6, 1)
        assert "AAPL" in data

    @pytest.mark.highweight
    def test_get_price_target_batch_pandas(self):
        # weight: 1000
        stock = Stock(["AAPL", "TSLA"], output_format='pandas')
        data = stock.get_price_target()

        assert isinstance(data, pd.DataFrame)
        assert data.shape == (6, 2)
        assert "AAPL" in data
        assert "TSLA" in data

    @pytest.mark.highweight
    def test_get_income_statement(self):
        # weight: 1000
        data = self.stock.get_income_statement()
        assert isinstance(data, dict)
        assert "symbol" in data
        assert "income" in data
        assert isinstance(data["income"], list)

    @pytest.mark.highweight
    def test_get_income_statement_pandas(self):
        # weight: 1000
        data = self.stock.get_income_statement()
        assert isinstance(data, pd.DataFrame)
        assert data.shape == (16, 1)
        assert "AAPL" in data

    @pytest.mark.highweight
    def test_batch_income_statement_pandas(self):
        # weight: 2000
        stock = Stock(["AAPL", "TSLA"], output_format='pandas')
        data = stock.get_income_statement()

        assert isinstance(data, pd.DataFrame)
        assert data.shape == (16, 2)
        assert "AAPL" in data
        assert "TSLA" in data
