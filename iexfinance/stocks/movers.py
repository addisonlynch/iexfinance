import pandas as pd

from iexfinance.base import _IEXBase


class MoversReader(_IEXBase):
    """
    Base class for retrieving market movers from the Stocks List endpoint

    Parameters
    ----------
    mover: str
        Desired mover
    """

    _AVAILABLE_MOVERS = [
        "mostactive",
        "gainers",
        "losers",
        "iexvolume",
        "iexpercent",
        "infocus",
    ]

    def __init__(self, mover=None, **kwargs):
        super(MoversReader, self).__init__(**kwargs)
        if mover in self._AVAILABLE_MOVERS:
            self.mover = mover
        else:
            raise ValueError("Please input a valid market mover.")

    @property
    def url(self):
        return "stock/market/list/" + self.mover

    def _convert_output(self, out):
        if out:
            return pd.DataFrame(out).set_index("symbol")
        else:
            return pd.DataFrame()
