import pandas as pd

from iexfinance.base import _IEXBase


class SectorPerformanceReader(_IEXBase):
    @property
    def url(self):
        return "stock/market/sector-performance"

    def _convert_output(self, out):
        if out:
            out = {item["name"]: item for item in out}
            return pd.DataFrame(out).T
        return pd.DataFrame()
