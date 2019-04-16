import pandas as pd
import pytest


_ALL_METHODS = [
        ("get_balance_sheet", dict, pd.DataFrame, 27),
        ("get_book", dict, 5),
        ("get_cash_flow", dict, 16),
        ("get_company", dict, 12),
        ("get_delayed_quote", dict, 8),
        ("get_dividends", list, 'varies'),
        ("get_earnings", list, 'varies'),
        ("get_effective_spread", list, 'varies'),
        ("get_estimates", dict, 6),
        ("get_financials", list, 'varies'),
        ("get_historical_prices", list, 'varies'),
        ("get_income_statement", list, 16),
        ("get_key_stats", dict, 30),
        ("get_largest_trades", list, 10),
        ("get_logo", dict, 1),
        #  ("get_news"),
        ("get_ohlc", dict, 5),
        ("get_open_close", dict, 5),
        #  ("get_peers", list, 5),
        ("get_previous_day_prices", dict, 15),
        ("get_price", float, 1),  # this isn't going to work
        ("get_price_target", dict, 6),
        ("get_quote", dict, 38),
        ("get_relevant_stocks", dict, 2),
        #  ("get_splits", list, 'varies') # no pandas for this
        #  ("get_time_series", list, 'varies') # duplicate of historical
        ("get_volume_by_venue", list, 14)
]


@pytest.fixture(params=_ALL_METHODS, scope='module', ids=[i[0] for i in
                                                          _ALL_METHODS])
def stock_method(request):
    return request.param


# @pytest.mark.usefixtures("stock_method")
class TestStocksJson(object):

    def test_format_single_json(self, stock_single, stock_method):
        method = getattr(stock_single, stock_method[0])
        data = method()
        assert isinstance(data, stock_method[1])

    def test_format_multiple_json(self, stock_multiple, stock_method):
        method = getattr(stock_multiple, stock_method[0])
        data = method()
        assert isinstance(data, (stock_method[1], dict))


class TestStocksPandas(object):

    def test_format_single_pandas(self, stock_single, stock_method):
        stock_single.output_format = 'pandas'
        method = getattr(stock_single, stock_method[0])
        data = method()
        assert isinstance(data, pd.DataFrame)

    def test_format_multiple_pandas(self, stock_multiple, stock_method):
        stock_multiple.output_format = 'pandas'
        method = getattr(stock_multiple, stock_method[0])
        data = method()
        assert isinstance(data, pd.DataFrame)
