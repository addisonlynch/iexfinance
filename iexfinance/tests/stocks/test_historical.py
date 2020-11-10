import pandas as pd
import pytest

from datetime import datetime

from iexfinance.stocks import get_historical_data
from iexfinance.stocks.historical import HistoricalReader


class TestHistorical(object):
    def setup_class(self):
        self.good_start = datetime(2017, 2, 9)
        self.good_end = datetime(2017, 5, 24)

    def test_single_historical(self):

        f = get_historical_data("AMZN", self.good_start, self.good_end)

        assert isinstance(f, pd.DataFrame)
        assert isinstance(f.index, pd.DatetimeIndex)
        assert len(f) == 73

        expected1 = f.loc["2017-02-09"]
        assert expected1["close"] == pytest.approx(821.36, 3)
        assert expected1["high"] == pytest.approx(825.0, 3)

        expected2 = f.loc["2017-05-24"]
        assert expected2["close"] == pytest.approx(980.35, 3)
        assert expected2["high"] == pytest.approx(981.0, 3)

    def test_batch_historical(self):

        f = get_historical_data(["AMZN", "TSLA"], self.good_start, self.good_end)

        assert isinstance(f, pd.DataFrame)
        assert len(f) == 146
        assert sorted(list(f.index.levels[0])) == ["AMZN", "TSLA"]

        a = f.loc["AMZN"]
        t = f.loc["TSLA"]

        assert len(a) == 73
        assert len(t) == 73

        expected1 = a.loc["2017-02-09"]
        assert expected1["close"] == pytest.approx(821.36, 3)
        assert expected1["high"] == pytest.approx(825.0, 3)

        expected2 = a.loc["2017-05-24"]
        assert expected2["close"] == pytest.approx(980.35, 3)
        assert expected2["high"] == pytest.approx(981.0, 3)

        expected1 = t.loc["2017-02-09"]
        assert expected1["close"] == pytest.approx(269.20, 3)
        assert expected1["high"] == pytest.approx(271.18, 3)

        expected2 = t.loc["2017-05-24"]
        assert expected2["close"] == pytest.approx(310.22, 3)
        assert expected2["high"] == pytest.approx(311.0, 3)

    def test_invalid_dates(self):
        start = datetime(2000, 5, 9)
        end = datetime(2017, 5, 9)
        with pytest.raises(ValueError):
            get_historical_data("AAPL", start, end)

    def test_invalid_dates_batch(self):
        start = datetime(2000, 5, 9)
        end = datetime(2017, 5, 9)
        with pytest.raises(ValueError):
            get_historical_data(["AAPL", "TSLA"], start, end)

    def test_invalid_symbol_batch(self):
        start = datetime(2017, 2, 9)
        end = datetime(2017, 5, 24)

        data = get_historical_data(["BADSYMBOL", "TSLA"], start, end)
        assert isinstance(data, pd.DataFrame)
        assert "TSLA" in data.index
        assert "BADSYMBOL" not in data.index

    def test_string_dates(self):
        start = "20190501"
        end = "20190601"

        data = get_historical_data("AAPL", start, end, output_format="pandas")

        assert isinstance(data, pd.DataFrame)
        assert len(data) == 22

    def test_close_only(self):
        data = get_historical_data(
            "AAPL", self.good_start, self.good_end, close_only=True
        )

        assert "open" not in data.loc["2017-02-09"]
        assert "high" not in data.loc["2017-02-09"]

    def test_reader_chart_range(self):
        from datetime import date, timedelta

        syms = ["AAPL"]

        # source: pandas datareader

        assert (
            HistoricalReader(
                symbols=syms, start=date.today() - timedelta(days=5), end=date.today()
            ).chart_range
            == "5d"
        )
        assert (
            HistoricalReader(
                symbols=syms, start=date.today() - timedelta(days=27), end=date.today()
            ).chart_range
            == "1m"
        )
        assert (
            HistoricalReader(
                symbols=syms, start=date.today() - timedelta(days=83), end=date.today()
            ).chart_range
            == "3m"
        )
        assert (
            HistoricalReader(
                symbols=syms, start=date.today() - timedelta(days=167), end=date.today()
            ).chart_range
            == "6m"
        )
        assert (
            HistoricalReader(
                symbols=syms, start=date.today() - timedelta(days=170), end=date.today()
            ).chart_range
            == "1y"
        )
        assert (
            HistoricalReader(
                symbols=syms, start=date.today() - timedelta(days=365), end=date.today()
            ).chart_range
            == "2y"
        )
        assert (
            HistoricalReader(
                symbols=syms, start=date.today() - timedelta(days=730), end=date.today()
            ).chart_range
            == "5y"
        )
        assert (
            HistoricalReader(
                symbols=syms,
                start=date.today() - timedelta(days=1826),
                end=date.today(),
            ).chart_range
            == "max"
        )
