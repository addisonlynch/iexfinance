import pytest
from iexfinance.stocks import (get_market_losers, get_market_most_active,
                               get_market_iex_volume, get_market_iex_percent,
                               get_market_in_focus, get_market_gainers)


class TestMarketMovers(object):

    def test_market_gainers(self):
        li = get_market_gainers()
        assert len(li) == pytest.approx(21, 1)

    def test_market_losers(self):
        li = get_market_losers()
        assert len(li) == pytest.approx(21, 1)

    def test_market_most_active(self):
        li = get_market_most_active()
        assert len(li) == pytest.approx(21, 1)

    def test_market_iex_volume(self):
        li = get_market_iex_volume()
        assert len(li) == pytest.approx(21, 1)

    def test_market_iex_percent(self):
        li = get_market_iex_percent()
        assert len(li) == pytest.approx(21, 1)

    def test_market_in_focus(self):
        li = get_market_in_focus()
        assert len(li) == pytest.approx(21, 1)
