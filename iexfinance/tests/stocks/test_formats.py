import pandas as pd
import pytest


NUMBER = [float, int]


_ALL_METHODS = [
        ("get_balance_sheet", dict, pd.DataFrame, 27),
        ("get_book", dict, 5),
        ("get_cash_flow", dict, 16),
        ("get_company", dict, 12),
        ("get_delayed_quote", dict, 8),
        ("get_dividends", list, 'varies'),
        ("get_earnings", list, 'varies'),
        ("get_estimates", dict, 6),
        ("get_financials", list, 'varies'),
        ("get_fund_ownership", list, 6),
        ("get_historical_prices", list, 'varies'),
        ("get_income_statement", list, 16),
        ("get_institutional_ownership", list, 5),
        ("get_insider_roster", list, 3),
        ("get_insider_summary", list, 5),
        ("get_insider_transactions", list, 6),
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


_FIELD_METHODS = [
    ("get_company_name", str),
    ("get_primary_exchange", str),
    ("get_sector", str),
    # ("get_open", float),  # fails on weekends
    ("get_close", float),
    ("get_years_high", float),
    ("get_years_low", (float, int)),
    ("get_ytd_change", float),
    ("get_volume", int),
    ("get_market_cap", int),
    ("get_beta", float),
    # ("get_short_interest", int),  # changed
    # ("get_short_ratio", float),  # changed
    # ("get_latest_eps", float),  # changed
    ("get_shares_outstanding", int),
    ("get_float", int),
    # ("get_eps_consensus", float)  # changed
]


@pytest.fixture(params=_ALL_METHODS, scope='module', ids=[i[0] for i in
                                                          _ALL_METHODS])
def stock_method(request):
    return request.param


@pytest.fixture(params=_FIELD_METHODS, scope='module', ids=[i[0] for i in
                                                            _FIELD_METHODS])
def field_method(request):
    return request.param


def _format_helper(obj, meta, r_type=None):
    method = getattr(obj, meta[0])
    data = method()
    if r_type is not None:
        assert isinstance(data, r_type)
    else:
        assert isinstance(data, (meta[1], dict))


class TestStocksJson(object):

    def test_format_single_json(self, stock_single, stock_method):
        _format_helper(stock_single, stock_method)

    def test_format_multiple_json(self, stock_multiple, stock_method):
        _format_helper(stock_multiple, stock_method)


class TestStocksPandas(object):

    def test_format_single_pandas(self, stock_single, stock_method):
        stock_single.output_format = 'pandas'
        _format_helper(stock_single, stock_method, r_type=pd.DataFrame)

    def test_format_multiple_pandas(self, stock_multiple, stock_method):
        stock_multiple.output_format = 'pandas'
        _format_helper(stock_multiple, stock_method, r_type=pd.DataFrame)


class TestFieldMethods(object):

    def test_format_single(self, stock_single, field_method):
        _format_helper(stock_single, field_method)

    def test_format_multiple(self, stock_multiple, field_method):
        _format_helper(stock_multiple, field_method)
