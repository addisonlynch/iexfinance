import pytest
from pandas import DataFrame

from iexfinance import (get_market_tops, get_market_last, get_market_deep,
                        get_market_book)


class TestMarket(object):

    @pytest.mark.xfail(reason="Market data only available during market open")
    def test_last_json_default(self):
        ls = get_market_last()

        assert isinstance(ls, list)

    @pytest.mark.xfail(reason="Market data only available during market open")
    def test_last_json_syms(self):
        ls = get_market_last("AAPL")
        ls2 = get_market_last(["AAPL", "TSLA"])

        assert isinstance(ls, list)
        assert isinstance(ls2, list)

    @pytest.mark.xfail(reason="Market data only available during market open")
    def test_last_pandas(self):
        df = get_market_last(output_format='pandas')
        df2 = get_market_last("AAPL", output_format='pandas')
        df3 = get_market_last(["AAPL", "TSLA"], output_format='pandas')

        assert isinstance(df, DataFrame)
        assert isinstance(df2, DataFrame)
        assert isinstance(df3, DataFrame)

    @pytest.mark.xfail(reason="Market data only available during market open")
    def test_TOPS_json_default(self):
        ls = get_market_tops()

        assert isinstance(ls, list)

    @pytest.mark.xfail(reason="Market data only available during market open")
    def test_TOPS_json_syms(self):
        ls = get_market_tops("AAPL")
        ls2 = get_market_tops(["AAPL", "TSLA"])

        assert isinstance(ls, list)
        assert isinstance(ls2, list)
        assert len(ls) == 1
        assert len(ls2) == 2

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
        js2 = get_market_deep(["AAPL", "TSLA"])

        assert isinstance(js, dict)
        assert isinstance(js2, dict)

    @pytest.mark.xfail(reason="Market data only available during market open")
    def test_DEEP_pandas(self):
        with pytest.raises(ValueError):
            get_market_deep("AAPL", output_format='pandas')
        with pytest.raises(ValueError):
            get_market_deep(["AAPL", "TSLA"], output_format='pandas')

    @pytest.mark.xfail(reason="Market data only available during market open")
    def test_Book_json_default(self):
        with pytest.raises(ValueError):
            get_market_book()

    @pytest.mark.xfail(reason="Market data only available during market open")
    def test_Book_json_syms(self):
        js = get_market_book("AAPL")
        js2 = get_market_book(["AAPL", "TSLA"])

        assert isinstance(js, dict)
        assert isinstance(js2, dict)

    @pytest.mark.xfail(reason="Market data only available during market open")
    def test_Book_pandas(self):
        df = get_market_book("AAPL", output_format='pandas')
        df2 = get_market_book(["AAPL", "TSLA"], output_format='pandas')

        assert isinstance(df, DataFrame)
        assert isinstance(df2, DataFrame)
