from iexfinance.base import _IEXBase
import pandas as pd


class UpcomingEarningsReader(_IEXBase):
    @property
    def url(self):
        return "stock/market/upcoming-earnings"

    def _convert_output(self, out):
        df = pd.DataFrame(out)
        df["reportDate"] = pd.to_datetime(df.reportDate)
        return df
