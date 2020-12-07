import numpy as np
import pandas as pd
import pytest

from iexfinance.stocks import Stock
from iexfinance.utils.exceptions import IEXQueryError


class TestFieldMethod(object):
    def setup_class(self):
        self.a = Stock("AAPL")
        self.b = Stock(["AAPL", "TSLA"])
        self.c = Stock("BADSYMBOL")
        self.d = Stock(["AAPL", "BADSYMBOL"])
        self.aj = Stock("AAPL", output_format="json")

    def test_get_field_single_bad_symbol(self):
        with pytest.raises(IEXQueryError):
            self.c._get_field("company", "exchange")

    def test_get_field_batch_bad_symbol(self):
        data = self.d._get_field("company", "exchange")

        assert isinstance(data, pd.DataFrame)
        assert "AAPL" in data.index

        assert "BADSYMBOL" not in data.index

    def test_get_bad_field(self):
        with pytest.raises(KeyError):
            self.a._get_field("company", "BADFIELD")

        with pytest.raises(KeyError):
            self.b._get_field("company", "BADFIELD")

        with pytest.raises(KeyError):
            self.aj._get_field("company", "BADFIELD")

    def test_get_bad_endpoint(self):
        with pytest.raises(NotImplementedError):
            self.a._get_field("BADFIELD", "NULL")

        with pytest.raises(NotImplementedError):
            self.b._get_field("BADFIELD", "NULL")

        with pytest.raises(NotImplementedError):
            self.aj._get_field("BADFIELD", "NULL")


class TestFieldMethods(object):
    def setup_class(self):
        self.a = Stock("AAPL")
        self.b = Stock(["AAPL", "TSLA"])

    def test_company_name(self):
        data = self.a.get_company_name()

        assert isinstance(data, str)
        assert data == "Apple Inc"

    def test_primary_exchange(self):
        data = self.a.get_primary_exchange()

        assert isinstance(data, str)
        assert len(data) == 33

    def test_sector(self):
        data = self.a.get_sector()

        assert isinstance(data, str)
        assert len(data) == 13

    def test_open(self):
        data = self.a.get_open()

        assert isinstance(data, np.float64)

    def test_close(self):
        data = self.a.get_close()

        assert isinstance(data, np.float64)

    def test_years_high(self):
        data = self.a.get_years_high()

        assert isinstance(data, np.float64)

    def test_years_low(self):
        data = self.a.get_years_low()

        assert isinstance(data, np.float64)

    def test_ytd_change(self):
        data = self.a.get_ytd_change()

        assert isinstance(data, np.float64)

    def test_volume(self):
        data = self.a.get_volume()

        assert isinstance(data, np.int64)

    def test_market_cap(self):
        data = self.a.get_market_cap()

        assert isinstance(data, np.int64)

    def test_beta(self):
        data = self.a.get_beta()

        assert isinstance(data, np.float64)

    def test_shares_outstanding(self):
        data = self.a.get_shares_outstanding()

        assert isinstance(data, np.int64)

    def test_float(self):
        data = self.a.get_float()

        assert isinstance(data, np.int64)
