from datetime import datetime

import pytest
import mock

import json

import pandas as pd

from iexfinance import Share, Batch, get_available_symbols, get_historical_data
from iexfinance import IexFinance as iex
from iexfinance.utils.exceptions import (IEXSymbolError, IEXQueryError)


class mocker(object):

    @classmethod
    def get_sample_share_data(cls):
        with open("tests/sample_data_share.json") as json_data:
            x = json.load(json_data)
            if not x:
                raise ValueError("sample_data_share.json is not properly "
                                 "formatted or is empty")
            return x

    @classmethod
    def get_sample_batch_data(cls):
        with open("tests/sample_data_batch.json") as json_data:
            x = json.load(json_data)
            if not x:
                raise ValueError("sample_data_batch.json is not properly "
                                 "formatted or is empty")
            return x

    @classmethod
    @mock.patch.object(Share, 'refresh')
    def get_mock_share(cls, mock_method):
        mock_method.return_value = cls.get_sample_share_data()
        inst = Share("luv")
        return inst

    @classmethod
    @mock.patch.object(Batch, 'refresh')
    def get_mock_batch(cls, mock_method):
        mock_method.return_value = cls.get_sample_batch_data()
        inst = Batch(["lol"])
        return inst


class TestBase(object):

    def test_wrong_iex_input_type(self):
        with pytest.raises(TypeError):
            iex(34)
        with pytest.raises(ValueError):
            iex("")
        with pytest.raises(ValueError):
            ls = []
            iex(ls)

    def test_symbol_list_too_long(self):
        with pytest.raises(ValueError):
            x = ["tsla"] * 102
            iex(x)

    def test_wrong_option_values(self):
        with pytest.raises(ValueError):
            iex("aapl", last=555)

        with pytest.raises(TypeError):
            iex("aapl", displayPercent=4)

        with pytest.raises(ValueError):
            iex("aapl", _range='1yy')

    # def test_invalid_option_values(self):
    #   with pytest.raises(TypeError):
    #       iex("aapl", displayPercent=4)
    #   with pytest.raises(ValueError):
    #       iex("aapl", last=68)
    #   with pytest.raises(ValueError):
    #       iex("aapl", chartRange='6y')
    #   with pytest.raises(ValueError):
    #       iex("aapl", )


# class ShareIntegrityTester(object):

#   def setup_class(self):
#       self.mshare = mocker.get_mock_share()
#       self.cshare = Share(self.mshare.get_symbol())

#   def test_endpoints(self):
#       mendpoints = list(self.mshare.get_all().keys())
#       cendpoints = list(self.cshare.get_all().keys())
#       mendpoints.sort()
#       cendpoints.sort()
#       self.assertListEqual(mendpoints, cendpoints)


#   def test_datapoints(self):
#       table = self.mshare.get_all()
#       for endpoint in table.keys():
#           mmod = self.mshare.get_select_endpoints(endpoint)
#           cmod = self.cshare.get_select_endpoints(endpoint)
#           assert type(mmod), type(cmod))
#           if type(mmod) is dict:
#               mdatapoints = list(mmod.keys())
#               cdatapoints = list(cmod.keys())
#               mdatapoints.sort()
#               cdatapoints.sort()
#               self.assertListEqual(mdatapoints, cdatapoints)
#           else:
#               print("Skipping endpoint " + endpoint)
#       self.assertListEqual(mdatapoints, cdatapoints)

class TestShare(object):

    def setup_class(self):
        self.cshare = Share("aapl")

    def test_get_all_format(self):
        data = self.cshare.get_all()
        assert isinstance(data, dict,)

    def test_get_chart_format(self):
        data = self.cshare.get_chart()
        assert isinstance(data, list)

    def test_get_book_format(self):
        data = self.cshare.get_book()
        assert isinstance(data, dict)

    def test_get_open_close_format(self):
        data = self.cshare.get_open_close()
        assert isinstance(data, dict)

    def test_get_previous_format(self):
        data = self.cshare.get_previous()
        assert isinstance(data, dict)

    def test_get_company_format(self):
        data = self.cshare.get_company()
        assert isinstance(data, dict)

    def test_get_key_stats_format(self):
        data = self.cshare.get_key_stats()
        assert isinstance(data, dict)

    def test_get_relevant_format(self):
        data = self.cshare.get_relevant()
        assert isinstance(data, dict)

    def test_get_news_format(self):
        data = self.cshare.get_news()
        assert isinstance(data, list)

    def test_get_financials_format(self):
        data = self.cshare.get_financials()
        assert isinstance(data, dict)

    def test_get_earnings_format(self):
        data = self.cshare.get_earnings()
        assert isinstance(data, dict)

    def test_get_logo_format(self):
        data = self.cshare.get_logo()
        assert isinstance(data, dict)

    def test_get_price_format(self):
        data = self.cshare.get_price()
        assert isinstance(data, float)

    def test_get_delayed_quote_format(self):
        data = self.cshare.get_delayed_quote()
        assert isinstance(data, dict)

    def test_get_effective_spread_format(self):
        data = self.cshare.get_effective_spread()
        assert isinstance(data, list)

    def test_get_volume_by_venue_format(self):
        data = self.cshare.get_volume_by_venue()
        assert isinstance(data, list)


class TestBatch(object):

    def setup_class(self):
        self.cbatch = Batch(["aapl", "tsla"])

    def test_invalid_symbol_or_symbols(self):
        with pytest.raises(IEXSymbolError):
            iex(["TSLA", "AAAPLPL", "fwoeiwf"])

    def test_get_all_format(self):
        data = self.cbatch.get_all()
        assert isinstance(data, dict)

    def test_get_chart_format(self):
        data = self.cbatch.get_chart()
        assert isinstance(data, dict)

    def test_get_book_format(self):
        data = self.cbatch.get_book()
        assert isinstance(data, dict)

    def test_get_open_close_format(self):
        data = self.cbatch.get_open_close()
        assert isinstance(data, dict)

    def test_get_previous_format(self):
        data = self.cbatch.get_previous()
        assert isinstance(data, dict)

    def test_get_company_format(self):
        data = self.cbatch.get_company()
        assert isinstance(data, dict)

    def test_get_key_stats_format(self):
        data = self.cbatch.get_key_stats()
        assert isinstance(data, dict)

    def test_get_relevant_format(self):
        data = self.cbatch.get_relevant()
        assert isinstance(data, dict)

    def test_get_news_format(self):
        data = self.cbatch.get_news()
        assert isinstance(data, dict)

    def test_get_financials_format(self):
        data = self.cbatch.get_financials()
        assert isinstance(data, dict)

    def test_get_earnings_format(self):
        data = self.cbatch.get_earnings()
        assert isinstance(data, dict)

    def test_get_logo_format(self):
        data = self.cbatch.get_logo()
        assert isinstance(data, dict)

    def test_get_price_format(self):
        data = self.cbatch.get_price()
        assert isinstance(data, dict)

    def test_get_delayed_quote_format(self):
        data = self.cbatch.get_delayed_quote()
        assert isinstance(data, dict)

    def test_get_effective_spread_format(self):
        data = self.cbatch.get_effective_spread()
        assert isinstance(data, dict)

    def test_get_volume_by_venue_format(self):
        data = self.cbatch.get_volume_by_venue()
        assert isinstance(data, dict)


class TestHistorical(object):

    def setup_class(self):
        self.good_start = datetime(2017, 2, 9)
        self.good_end = datetime(2017, 5, 24)

    def test_single_historical_json(self):

        f = get_historical_data("AAPL", self.good_start, self.good_end)
        assert isinstance(f, dict)
        assert len(f["AAPL"]) == 73

        expected1 = f["AAPL"]["2017-02-09"]
        assert expected1["close"] == 132.42
        assert expected1["high"] == 132.445

        expected2 = f["AAPL"]["2017-05-24"]
        assert expected2["close"] == 153.34
        assert expected2["high"] == 154.17

    def test_single_historical_pandas(self):

        f = get_historical_data("AAPL", self.good_start, self.good_end,
                                outputFormat="pandas")

        assert isinstance(f, pd.DataFrame)
        assert len(f) == 73

        expected1 = f.loc["2017-02-09"]
        assert expected1["close"] == 132.42
        assert expected1["high"] == 132.445

        expected2 = f.loc["2017-05-24"]
        assert expected2["close"] == 153.34
        assert expected2["high"] == 154.17

    def test_batch_historical_json(self):

        f = get_historical_data(["AAPL", "TSLA"], self.good_start,
                                self.good_end, outputFormat="json")

        assert isinstance(f, dict)
        assert len(f) == 2
        assert sorted(list(f)) == ["AAPL", "TSLA"]

        a = f["AAPL"]
        t = f["TSLA"]

        assert len(a) == 73
        assert len(t) == 73

        expected1 = a["2017-02-09"]
        assert expected1["close"] == 132.42
        assert expected1["high"] == 132.445

        expected2 = a["2017-05-24"]
        assert expected2["close"] == 153.34
        assert expected2["high"] == 154.17

        expected1 = t["2017-02-09"]
        assert expected1["close"] == 269.20
        assert expected1["high"] == 271.18

        expected2 = t["2017-05-24"]
        assert expected2["close"] == 310.22
        assert expected2["high"] == 311.0

    def test_batch_historical_pandas(self):

        f = get_historical_data(["AAPL", "TSLA"], self.good_start,
                                self.good_end, outputFormat="pandas")

        assert isinstance(f, dict)
        assert len(f) == 2
        assert sorted(list(f)) == ["AAPL", "TSLA"]

        a = f["AAPL"]
        t = f["TSLA"]

        assert len(a) == 73
        assert len(t) == 73

        expected1 = a.loc["2017-02-09"]
        assert expected1["close"] == 132.42
        assert expected1["high"] == 132.445

        expected2 = a.loc["2017-05-24"]
        assert expected2["close"] == 153.34
        assert expected2["high"] == 154.17

        expected1 = t.loc["2017-02-09"]
        assert expected1["close"] == 269.20
        assert expected1["high"] == 271.18

        expected2 = t.loc["2017-05-24"]
        assert expected2["close"] == 310.22
        assert expected2["high"] == 311.0

    def test_invalid_dates(self):
        start = datetime(2010, 5, 9)
        end = datetime(2017, 5, 9)
        with pytest.raises(ValueError):
            get_historical_data("AAPL", start, end)

    def test_invalid_dates_batch(self):
        start = datetime(2010, 5, 9)
        end = datetime(2017, 5, 9)
        with pytest.raises(ValueError):
            get_historical_data(["AAPL", "TSLA"], start, end)

    def test_invalid_symbol_single(self):
        start = datetime(2017, 2, 9)
        end = datetime(2017, 5, 24)
        with pytest.raises(IEXQueryError):
            get_historical_data("BADSYMBOL", start, end)

    def test_invalid_symbol_batch(self):
        start = datetime(2017, 2, 9)
        end = datetime(2017, 5, 24)
        with pytest.raises(IEXSymbolError):
            get_historical_data(["BADSYMBOL", "TSLA"], start, end)


class UtilsTester(object):

    def test_available_symbols(self):
        f = True
        if not get_available_symbols():
            f = False
        assert f is True
