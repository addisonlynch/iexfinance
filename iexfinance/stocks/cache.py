import os
from enum import Enum
from typing import NamedTuple, Union

import pandas as pd

_IEXFINANCE_CACHE_ = None

class CacheType(Enum):
    NO_CACHE = 1
    HDF_STORE = 2

class CacheMetadata(NamedTuple):
    """
    cache_type: Enum, default CacheType.NO_CACHE
        The type of cache (i.e. data store) to use to store previously requested
        data.
    cache_path: string, default None
         Required if `cache_type` is specified.
         A path to a file that stores the cached data.
    """
    cache_path: str
    cache_type: CacheType = CacheType.NO_CACHE

def prepare_cache(cache: Union[CacheMetadata, pd.HDFStore]):
    global _IEXFINANCE_CACHE_

    if isinstance(cache, pd.HDFStore):
        _IEXFINANCE_CACHE_ = cache
        return

    cache_type = cache.cache_type
    cache_path = cache.cache_path

    if not isinstance(cache_type, CacheType):
        raise TypeError('`cache_type` must be an instance of CacheType Enum')
    if cache_path is None:
        raise ArgumentError('`cache_path` must not be none.')
    if cache_type == CacheType.HDF_STORE:
        _IEXFINANCE_CACHE_ = pd.HDFStore(cache_path)
    else:
        raise InternalError('Cannot initialize cache.')
