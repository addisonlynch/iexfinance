import pytest
from pandas import DataFrame

from iexfinance.iexdata import (get_market_tops, get_market_last,
                                get_market_deep, get_market_book)


class TestMarket(object):

    def setup_class(self):
        self.bad = ["AAPL", "TSLA", "MSFT", "F", "GOOGL", "STM", "DAL",
                    "UVXY", "SPY", "DIA", "SVXY", "CMG", "LUV"]

    @pytest.mark.xfail(reason="Market data only available during market open")
    def test_last_json_default(self):
        ls = get_market_last()

        assert isinstance(ls, list) and len(ls) > 7500

    @pytest.mark.xfail(reason="Market data only available during market open")
    def test_last_json_syms(self):
        ls = get_market_last("AAPL")
        ls2 = get_market_last(["AAPL", "TSLA"])

        assert isinstance(ls, list) and len(ls) == 1
        assert isinstance(ls2, list) and len(ls2) == 2

    @pytest.mark.xfail(reason="Market data only available during market open")
    def test_last_pandas(self):
        df = get_market_last(output_format='pandas')
        df2 = get_market_last("AAPL", output_format='pandas')
        df3 = get_market_last(["AAPL", "TSLA"], output_format='pandas')

        assert isinstance(df, DataFrame)
        assert isinstance(df2, DataFrame)
        assert isinstance(df3, DataFrame)

    def test_last_too_many_symbols(self):
        with pytest.raises(ValueError):
            get_market_last(self.bad)

    @pytest.mark.xfail(reason="Market data only available during market open")
    def test_TOPS_json_default(self):
        ls = get_market_tops()

        assert isinstance(ls, list) and len(ls) > 7500

    @pytest.mark.xfail(reason="Market data only available during market open")
    def test_TOPS_json_syms(self):
        ls = get_market_tops("AAPL")
        ls2 = get_market_tops(["AAPL", "TSLA"])

        assert isinstance(ls, list) and len(ls) == 1
        assert isinstance(ls2, list) and len(ls2) == 2

    def test_TOPS_too_many_symbols(self):
        with pytest.raises(ValueError):
            get_market_tops(self.bad)

    @pytest.mark.xfail(reason="Market data only available during market open")
    def test_TOPS_pandas(self):
        df = get_market_tops("AAPL", output_format='pandas')
        df2 = get_market_tops(["AAPL", "TSLA"], output_format='pandas')

        assert isinstance(df, DataFrame)
        assert isinstance(df2, DataFrame)

    @pytest.mark.xfail(reason="Market data only available during market open")
    def test_DEEP_json_default(self):
        with pytest.raises(ValueError):
            get_market_deep()

    @pytest.mark.xfail(reason="Market data only available during market open")
    def test_DEEP_json_syms(self):
        js = get_market_deep("AAPL")

        assert isinstance(js, dict)

    @pytest.mark.xfail(reason="Market data only available during market open")
    def test_DEEP_pandas(self):
        with pytest.raises(ValueError):
            get_market_deep("AAPL", output_format='pandas')

    def test_DEEP_too_many_syms(self):
        with pytest.raises(ValueError):
            get_market_deep(["AAPL", "TSLA"])

    @pytest.mark.xfail(reason="Market data only available during market open")
    def test_Book_json_default(self):
        with pytest.raises(ValueError):
            get_market_book()

    @pytest.mark.xfail(reason="Market data only available during market open")
    def test_Book_json_syms(self):
        js = get_market_book("AAPL")
        js2 = get_market_book(["AAPL", "TSLA"])

        assert isinstance(js, dict) and len(js) == 1
        assert isinstance(js2, dict) and len(js2) == 2

    def test_Book_too_many_symbols(self):
        with pytest.raises(ValueError):
            get_market_book(self.bad)
