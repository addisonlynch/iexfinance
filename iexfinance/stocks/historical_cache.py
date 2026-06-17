import logging
import datetime

import iexfinance.stocks.cache as cache
from iexfinance.stocks.historical import HistoricalReader

logger = logging.getLogger(__name__)

class HistoricalReaderCache(HistoricalReader):
    """
    Base class to download historical data from the chart endpoint that is
    also cached.

    Reference: https://iextrading.com/developer/docs/#chart
    """

    def __init__(self, symbols, start=None, end=None, close_only=False, **kwargs):
        if cache._IEXFINANCE_CACHE_ is None:
            raise InternalError("Must called `prepare_cache` first.")
        self.kwargs = kwargs
        super(HistoricalReaderCache, self).__init__(symbols, start=start, end=end, close_only=close_only, **kwargs)

    def _execute_iex_query(self, url):
        if len(self.symbols) > 1:
            raise InternalError("Not supported yet")
        return self._get_historical_data_cached(self.symbols[0])

    def _format_output(self, out, format=None):
        if self.output_format == "json":
            raise InternalError("Need to convert dataframe to json")
        if len(self.symbols) > 1:
            raise InternalError("Need to concanatanate cached data.")
        else:
            result = out
            result = result.loc[self.start : self.end, :]
        if self.close_only is True:
            result = result.loc[:, ["close", "volume"]]
        return result

    def _get_historical_data(self, symbol, start, end):
        return HistoricalReader(
            symbol, start=start, end=end, close_only=self.close_only, **self.kwargs
        ).fetch()

    def _get_historical_data_cached(self, symbol):
        logger.info(f"{symbol}: `get_historical_data_cached` request between {self.start} and {self.end}.")

        if symbol not in cache._IEXFINANCE_CACHE_:
            logger.info(f"{symbol}: No data is cached.")
            df = self._get_historical_data(symbol, self.start, self.end)
            metadata = {'min_date': self.start, 'max_date': self.end}
        else:
            metadata = cache._IEXFINANCE_CACHE_.get_storer(symbol).attrs.metadata
            logger.info(f"{symbol}: Data is catched between {metadata['min_date']} and {metadata['max_date']}.")

            df = cache._IEXFINANCE_CACHE_[symbol]
            if self.start < metadata['min_date']:
                logger.info(f"{symbol}: Requesting data between {self.start} and {metadata['min_date']}.")
                df = df.append(self._get_historical_data(symbol, self.start, metadata['max_date']))
                metadata['min_date'] = self.start

            if self.end > metadata['max_date']:
                logger.info(f"{symbol}: Requesting data between {metadata['max_date']} and {self.end}.")
                df = df.append(self._get_historical_data(symbol, metadata['max_date'], self.end))
                metadata['max_date'] = self.end

            # Not using HDFStore.append() because of the need to de-duplicate
            df = df[~df.index.duplicated(keep='first')]

        cache._IEXFINANCE_CACHE_[symbol] = df
        cache._IEXFINANCE_CACHE_.get_storer(symbol).attrs.metadata = metadata

        return df
