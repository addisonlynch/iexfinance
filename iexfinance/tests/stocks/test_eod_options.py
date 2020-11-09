import pandas as pd
import pytest

from iexfinance.stocks import get_eod_options


class TestEODOptions(object):
    def test_eod_options_no_symbol(self):
        with pytest.raises(TypeError):
            get_eod_options()

    def test_eod(self):
        data = get_eod_options("AAPL")

        assert isinstance(data, pd.DataFrame)

    @pytest.mark.xfail(
        reason="Provider scrambles expiration dates but does "
        "not accept scrambled dates for calls"
    )
    def test_single_date(self):
        # obtain list of expiration dates (often changes)
        expiries = get_eod_options("AAPL")

        # use first date
        data = get_eod_options("AAPL", expiries[0])

        assert isinstance(data, list)
        assert isinstance(data[0], dict)
        assert data[0]["symbol"] == "AAPL"

        data2 = get_eod_options("AAPL", expiries[0], output_format="pandas")
        assert isinstance(data2, pd.DataFrame)
