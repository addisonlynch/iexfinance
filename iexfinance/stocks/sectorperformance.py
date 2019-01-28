from iexfinance.base import _IEXBase


class SectorPerformanceReader(_IEXBase):

    @property
    def url(self):
        return "stock/market/sector-performance"

    def _convert_output(self, out):
        import pandas as pd
        out = {item["name"]: item for item in out}
        return pd.DataFrame(out)
