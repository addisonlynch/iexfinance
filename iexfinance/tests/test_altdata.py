import datetime
import pandas as pd
import pytest

from iexfinance.altdata import (get_crypto_quote, get_social_sentiment,
                                get_ceo_compensation)
from iexfinance.altdata.base import SocialSentiment


@pytest.fixture
def valid_date():
    return datetime.datetime.today()


class TestAltData(object):

    def test_crypto_quote_no_sym(self):
        with pytest.raises(TypeError):
            get_crypto_quote()

    def test_crypto_quote_list(self):
        with pytest.raises(ValueError):
            get_crypto_quote(["BTCUSDT", "BAD"])

    def test_crypto_quote_json(self):
        data = get_crypto_quote("BTCUSDT")

        assert isinstance(data, dict)
        assert len(data) == 15

        assert data["symbol"] == "BTCUSDT"

    def test_crypto_quote_pandas(self):
        data = get_crypto_quote("BTCUSDT", output_format='pandas')

        assert isinstance(data, pd.DataFrame)
        assert len(data) == 15


class TestSocialSentiment(object):
    """
    Partially-implemented tests for social sentiment. Unstable endpoint, will
    be completed when provider repairs
    """
    def test_social_bad_period(self):
        with pytest.raises(ValueError):
            get_social_sentiment('AAPL', period_type='badperiod')

    @pytest.mark.parametrize('date,period,url', [
            (None, None, '/stock/AAPL/sentiment/daily'),
            ('20190101', None, '/stock/AAPL/sentiment/daily/20190101'),
            ('20190101', 'minute', '/stock/AAPL/sentiment/minute/20190101'),
        ])
    def test_social_url(self, date, period, url):
        obj = SocialSentiment("AAPL", date=date, period_type=period)

        assert obj.url == url

    @pytest.mark.xfail(reason="Unstable endpoint.")
    def test_social_json(self):
        data = get_social_sentiment("AAPL")

        assert isinstance(data, dict)


class TestCEOCompensation(object):

    def test_ceo_compensation_json(self):
        data = get_ceo_compensation("AAPL")

        assert isinstance(data, dict)
        assert data["symbol"] == "AAPL"

    def test_ceo_compensation_pandas(self):
        data = get_ceo_compensation("AAPL", output_format='pandas')

        assert isinstance(data, pd.DataFrame)
        assert "AAPL" in data
