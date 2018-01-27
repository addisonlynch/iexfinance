from iexfinance import (get_TOPS, get_Last, get_DEEP, get_Book)

import pytest
from pandas import DataFrame


class TestMarket(object):

    def test_last_json_default(self):
        ls = get_Last()

        assert isinstance(ls, list)

    def test_last_json_syms(self):
        ls = get_Last("AAPL")
        ls2 = get_Last(["AAPL", "TSLA"])

        assert isinstance(ls, list)
        assert isinstance(ls2, list)

    def test_last_pandas(self):
        df = get_Last(outputFormat='pandas')
        df2 = get_Last("AAPL", outputFormat='pandas')
        df3 = get_Last(["AAPL", "TSLA"], outputFormat='pandas')

        assert isinstance(df, DataFrame)
        assert isinstance(df2, DataFrame)
        assert isinstance(df3, DataFrame)

    def test_TOPS_json_default(self):
        ls = get_TOPS()

        assert isinstance(ls, list)

    def test_TOPS_json_syms(self):
        ls = get_TOPS("AAPL")
        ls2 = get_TOPS(["AAPL", "TSLA"])

        assert isinstance(ls, list)
        assert isinstance(ls2, list)
        assert len(ls) == 1
        assert len(ls2) == 2

    def test_TOPS_pandas(self):
        df = get_TOPS("AAPL", outputFormat='pandas')
        df2 = get_TOPS(["AAPL", "TSLA"], outputFormat='pandas')

        assert isinstance(df, DataFrame)
        assert isinstance(df2, DataFrame)

    def test_DEEP_json_default(self):
        with pytest.raises(ValueError):
            get_DEEP()

    def test_DEEP_json_syms(self):
        js = get_DEEP("AAPL")
        js2 = get_DEEP(["AAPL", "TSLA"])

        assert isinstance(js, dict)
        assert isinstance(js2, dict)

    def test_DEEP_pandas(self):
        with pytest.raises(ValueError):
            get_DEEP("AAPL", outputFormat='pandas')
        with pytest.raises(ValueError):
            get_DEEP(["AAPL", "TSLA"], outputFormat='pandas')

    def test_Book_json_default(self):
        with pytest.raises(ValueError):
            get_Book()

    def test_Book_json_syms(self):
        js = get_Book("AAPL")
        js2 = get_Book(["AAPL", "TSLA"])

        assert isinstance(js, dict)
        assert isinstance(js2, dict)

    def test_Book_pandas(self):
        df = get_Book("AAPL", outputFormat='pandas')
        df2 = get_Book(["AAPL", "TSLA"], outputFormat='pandas')

        assert isinstance(df, DataFrame)
        assert isinstance(df2, DataFrame)
