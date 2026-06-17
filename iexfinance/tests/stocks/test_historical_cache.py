import logging
import os
import tempfile
import unittest
from datetime import date, datetime, timedelta

import pytest
from pandas import to_datetime

import iexfinance.stocks.cache
from iexfinance.stocks import get_historical_data
from iexfinance.stocks.cache import *


class TestHistoricalCache(unittest.TestCase):
    def setup_class(self):
        today = date.today()
        today = to_datetime(today)
        self.end = today - timedelta(days=30)
        self.start = self.end - timedelta(days=365)*5

    @pytest.fixture(autouse=True)
    def prepare_test_cache(scope="function"):
        with tempfile.TemporaryDirectory() as tempdir:
            hdf_store_path = os.path.join(tempdir, 'test_store.h5')
            cache_metadata = CacheMetadata(cache_path=hdf_store_path, cache_type=CacheType.HDF_STORE)
            prepare_cache(cache_metadata)
            yield

    def _messages_used_logs(self, caplog):
        return [log for log in caplog if 'MESSAGES USED' in log]

    def _assert_data(self, data):
        expected = data.loc["2017-02-09"]
        assert expected["close"] == pytest.approx(821.36, 3)
        assert expected["high"] == pytest.approx(825.0, 3)

    def test_get_historical_data_cached_none(self):
        with self.assertLogs(level='INFO') as cm:
            data = get_historical_data(["AMZN"], self.start, self.end)

            messages_used_logs = self._messages_used_logs(cm.output)
            assert len(messages_used_logs) == 1
            assert 'INFO:iexfinance.base:MESSAGES USED: 35330' in messages_used_logs

            self._assert_data(data)

    def test_get_historical_data_cached_full(self):
        with self.assertLogs(level='INFO') as cm:
            get_historical_data(["AMZN"], self.start, self.end)
            start = self.start + timedelta(days=1)
            end = self.end - timedelta(days=1)
            data = get_historical_data(["AMZN"], start, end)

            messages_used_logs = self._messages_used_logs(cm.output)
            assert len(messages_used_logs) == 1
            assert messages_used_logs.count('INFO:iexfinance.base:MESSAGES USED: 35330') == 1

            self._assert_data(data)

    def test_get_historical_data_cached_missing_start(self):
        with self.assertLogs(level='INFO') as cm:
            get_historical_data(["AMZN"], self.start, self.end)
            start = self.start - timedelta(days=5)
            data = get_historical_data(["AMZN"], start, self.end)

            messages_used_logs = self._messages_used_logs(cm.output)
            assert len(messages_used_logs) == 2
            assert messages_used_logs.count('INFO:iexfinance.base:MESSAGES USED: 35330') == 2

    def test_get_historical_data_cached_missing_end(self):
        with self.assertLogs(level='INFO') as cm:
            get_historical_data(["AMZN"], self.start, self.end)
            end = self.end + timedelta(days=5)
            data = get_historical_data(["AMZN"], self.start, end)

            messages_used_logs = self._messages_used_logs(cm.output)
            assert len(messages_used_logs) == 2
            assert messages_used_logs.count('INFO:iexfinance.base:MESSAGES USED: 35330') == 1
            assert messages_used_logs.count('INFO:iexfinance.base:MESSAGES USED: 620') == 1
