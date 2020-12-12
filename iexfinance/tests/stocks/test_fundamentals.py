import pandas as pd
import pytest

from iexfinance.stocks import Stock
from iexfinance.utils.exceptions import IEXQueryError


class TestStockFundamentals(object):
    def setup_class(self):
        self.a = Stock("AAPL")
        self.b = Stock(["AAPL", "TSLA"])
        self.c = Stock("SVXY")
        self.d = Stock(["AAPL", "SVXY"])
        self.e = Stock("BADSYMBOL", retry_count=0, pause=0)
        self.f = Stock(["AAPL", "BADSYMBOL"])

    def test_single_bad_symbol(self):
        with pytest.raises(IEXQueryError):
            self.e.get_balance_sheet()

        with pytest.raises(IEXQueryError):
            self.e.get_cash_flow()

        with pytest.raises(IEXQueryError):
            self.e.get_dividends()

        with pytest.raises(IEXQueryError):
            self.e.get_earnings()

        with pytest.raises(IEXQueryError):
            self.e.get_income_statement()

        with pytest.raises(IEXQueryError):
            self.e.get_splits()

    def test_bad_symbols(self):
        data = self.f.get_balance_sheet()

        assert len(data) == 1
        assert "AAPL" in data
        assert "BADSYMBOL" not in data

    def test_balance_sheet(self):
        data = self.d.get_balance_sheet()
        assert isinstance(data, dict)
        assert isinstance(data["AAPL"], pd.DataFrame) and not data["AAPL"].empty
        assert isinstance(data["SVXY"], pd.DataFrame) and data["SVXY"].empty

    def test_balance_sheet_params(self):
        data = self.a.get_balance_sheet(last=4)
        assert len(data.index) == 4

    def test_cash_flow(self):
        data = self.d.get_cash_flow()
        assert isinstance(data, dict)
        assert isinstance(data["AAPL"], pd.DataFrame) and not data["AAPL"].empty
        assert isinstance(data["SVXY"], pd.DataFrame) and data["SVXY"].empty

    def test_cash_flow_params(self):
        data = self.a.get_cash_flow(last=4)
        assert len(data.index) == 4

    def test_dividends(self):
        data = self.d.get_dividends(range="5y")

        assert isinstance(data, dict)
        assert isinstance(data["AAPL"], pd.DataFrame) and not data["AAPL"].empty
        assert isinstance(data["SVXY"], pd.DataFrame) and not data["SVXY"].empty

    def test_earnings(self):
        data = self.d.get_earnings()
        assert isinstance(data, dict)
        assert isinstance(data["AAPL"], pd.DataFrame) and not data["AAPL"].empty
        assert isinstance(data["SVXY"], pd.DataFrame) and data["SVXY"].empty

    def test_earnings_params(self):
        data = self.a.get_earnings(last=4)
        assert len(data.index) == 4

    def test_financials(self):
        data = self.d.get_earnings()
        assert isinstance(data, dict)
        assert isinstance(data["AAPL"], pd.DataFrame) and not data["AAPL"].empty
        assert isinstance(data["SVXY"], pd.DataFrame) and data["SVXY"].empty

    def test_financials_params(self):
        data = self.a.get_earnings(last=4)
        assert len(data.index) == 4

    def test_income_statement(self):
        data = self.d.get_income_statement()
        assert isinstance(data, dict)
        assert isinstance(data["AAPL"], pd.DataFrame) and not data["AAPL"].empty
        assert isinstance(data["SVXY"], pd.DataFrame) and data["SVXY"].empty

    def test_income_statement_params(self):
        data = self.a.get_income_statement(last=4)
        assert len(data.index) == 4

    def test_splits(self):
        data = self.d.get_splits(range="5y")

        assert isinstance(data, dict)
        assert isinstance(data["AAPL"], pd.DataFrame) and not data["AAPL"].empty
        assert isinstance(data["SVXY"], pd.DataFrame) and not data["SVXY"].empty
