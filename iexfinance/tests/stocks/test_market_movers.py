import pandas as pd
import pytest

from iexfinance.stocks import (
    get_market_gainers,
    get_market_iex_percent,
    get_market_iex_volume,
    get_market_losers,
    get_market_most_active,
)


class TestMarketMovers(object):
    def test_market_gainers(self):
        li = get_market_gainers()

        assert isinstance(li, pd.DataFrame)
        assert len(li) == pytest.approx(10, 1)

    def test_market_losers(self):
        li = get_market_losers()

        assert isinstance(li, pd.DataFrame)
        assert len(li) == pytest.approx(10, 1)

    def test_market_most_active(self):
        li = get_market_most_active()

        assert isinstance(li, pd.DataFrame)
        assert len(li) == pytest.approx(10, 1)

    def test_market_iex_volume(self):
        li = get_market_iex_volume()

        assert isinstance(li, pd.DataFrame)
        assert len(li) == pytest.approx(10, 1)

    def test_market_iex_percent(self):
        li = get_market_iex_percent()

        assert isinstance(li, pd.DataFrame)
        assert len(li) == pytest.approx(10, 1)
