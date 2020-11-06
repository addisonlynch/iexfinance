from datetime import datetime

import pandas as pd

from iexfinance.refdata import (
    get_symbols,
    get_iex_symbols,
    get_us_trading_dates_holidays,
)


IEX_MSG = (
    "These functions return data for IEX listed symbols only. There is "
    "only 1 listed IEX symbol."
)


class TestRef(object):
    def setup_class(self):
        self.keys = {"RecordID", "DailyListTimestamp", "CompanyName"}
        self.start = datetime(2017, 5, 4)

    def test_get_symbols(self):
        d = get_symbols()
        assert isinstance(d, pd.DataFrame)

    def test_get_iex_symbols(self):
        d = get_iex_symbols()

        assert isinstance(d, pd.DataFrame)

    def test_get_us_trading_dates_holidays(self):
        assert isinstance(get_us_trading_dates_holidays("trade", "last"), pd.DataFrame)
        assert isinstance(get_us_trading_dates_holidays("trade", "last", last=5), pd.DataFrame)
        assert isinstance(
            get_us_trading_dates_holidays("trade", "last", startDate="20200502"), pd.DataFrame
        )
        assert isinstance(
            get_us_trading_dates_holidays(
                "trade", "last", last=2, startDate="20191201"
            ),
            pd.DataFrame,
        )
        assert isinstance(get_us_trading_dates_holidays("holiday", "next"), pd.DataFrame)
