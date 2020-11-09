import pytest
import pandas as pd

from decimal import Decimal

from iexfinance.stocks import Stock


class TestBase(object):
    def setup_class(self):
        self.a = Stock("AAPL")
        self.aj = Stock("AAPL", output_format="json")
        self.b = Stock(["AAPL", "TSLA"])
        self.bj = Stock(["AAPL", "TSLA"], output_format="json")
        self.c = Stock("SVXY")
        self.dj = Stock(
            "AAPL",
            json_parse_int=Decimal,
            json_parse_float=Decimal,
            output_format="json",
        )
        self.e = Stock("GIG^")

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

    def test_filter(self):
        data = self.a.get_quote(filter_="ytdChange")

        assert isinstance(data, pd.DataFrame)
        assert len(data.columns) == 1
        assert "ytdChange" in data.columns

        data2 = self.aj.get_quote(filter_="ytdChange")
        assert isinstance(data2, dict)
        assert isinstance(data2["ytdChange"], (int, float))

    def test_json_parse(self):

        data = self.dj.get_quote(filter_="ytdChange")
        assert isinstance(data, dict)
        assert isinstance(data["ytdChange"], Decimal)
