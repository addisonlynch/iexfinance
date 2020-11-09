from iexfinance.stocks import get_earnings_today


class TestEarningsToday(object):
    def test_earnings_today(self):
        data = get_earnings_today()

        assert isinstance(data, dict)
