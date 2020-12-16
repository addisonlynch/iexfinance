import pandas as pd
import pytest

from iexfinance.altdata import get_ceo_compensation, get_social_sentiment
from iexfinance.altdata.base import SocialSentiment
from iexfinance.utils.exceptions import IEXQueryError


@pytest.mark.skip(reason="Social sentiment is a premium-only endpoint.")
class TestSocialSentiment(object):
    """
    Partially-implemented tests for social sentiment. Unstable endpoint, will
    be completed when provider repairs
    """

    def test_social_bad_period(self):
        with pytest.raises(ValueError):
            get_social_sentiment("AAPL", period_type="badperiod")

    @pytest.mark.parametrize(
        "date,period,url",
        [
            (None, None, "/stock/AAPL/sentiment/daily"),
            ("20190101", None, "/stock/AAPL/sentiment/daily/20190101"),
            ("20190101", "minute", "/stock/AAPL/sentiment/minute/20190101"),
        ],
    )
    def test_social_url(self, date, period, url):
        obj = SocialSentiment("AAPL", date=date, period_type=period)

        assert obj.url == url

    @pytest.mark.xfail(reason="Unstable endpoint.")
    def test_social_json(self):
        data = get_social_sentiment("AAPL")

        assert isinstance(data, dict)


class TestCEOCompensation(object):
    def test_ceo_compensation(self):
        data = get_ceo_compensation("AAPL")

        assert isinstance(data, pd.DataFrame)
        assert "AAPL" in data.index

    def test_ceo_compensation_bad_symbol(self):
        with pytest.raises(IEXQueryError):
            get_ceo_compensation("BADSYMBOL")
