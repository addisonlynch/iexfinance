import pandas as pd
import pytest

from iexfinance.stocks import Stock
from iexfinance.utils.exceptions import IEXQueryError


class TestStockPrices(object):

    def setup_class(self):
        a = Stock("AAPL")
        b = Stock(["AAPL", "TSLA"])
        c = Stock("SVXY")
        d = Stock(["AAPL", "SVXY"])
        e = Stock("BADSYMBOL")

    def test_bad_symbol(self):
        with pytest.raises(IEXQueryError):
            e.get_book()


    def test_book(self):
        data = a.get_book()
        
        assert isinstance(data, dict)
    
    