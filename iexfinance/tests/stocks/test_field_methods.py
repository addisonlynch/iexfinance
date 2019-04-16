import pytest
import pandas as pd
from pandas.util.testing import assert_index_equal

from decimal import Decimal

from iexfinance.stocks import Stock


class TestFieldMethodsShare(object):

    def setup_class(self):
        self.share = Stock("AAPL")
        self.share2 = Stock("AAPL", output_format='pandas')
        self.share4 = Stock("AAPL",
                            json_parse_int=Decimal,
                            json_parse_float=Decimal)
        self.share5 = Stock("TSLA")

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
