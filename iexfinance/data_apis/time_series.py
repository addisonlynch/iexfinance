import os
import pandas as pd

from iexfinance.base import _IEXBase


class TimeSeries(_IEXBase):
    def __init__(self, id_=None, key=None, subkey=None, **kwargs):
        self.id_ = id_
        self.key = key
        self.subkey = subkey

        # Base class parameters. Pop from kwargs stored in _params
        # Need to do this since arbitrary number of params allowed in call
        retry_count = kwargs.pop("retry_count", 3)
        pause = kwargs.pop("pause", 0.5)
        session = kwargs.pop("session", None)
        json_parse_int = kwargs.pop("json_parse_int", None)
        json_parse_float = kwargs.pop("json_parse_float", None)
        output_format = kwargs.pop(
            "output_format", os.getenv("IEX_OUTPUT_FORMAT", "pandas")
        )
        token = kwargs.pop("token", None)

        self._params = kwargs
        super(TimeSeries, self).__init__(
            retry_count=retry_count,
            pause=pause,
            session=session,
            json_parse_int=json_parse_int,
            json_parse_float=json_parse_float,
            output_format=output_format,
            token=token,
        )

    @property
    def url(self):
        if self.id_ is None:
            return "time-series"
        else:
            if self.key:
                if self.subkey:
                    return "time-series/%s/%s/%s" % (self.id_, self.key, self.subkey)
                return "time-series/%s/%s" % (self.id_, self.key)
            return "time-series/%s" % self.id_

    @property
    def params(self):
        return self._params

    def _convert_output(self, out):
        if self.id_ is None:
            return pd.DataFrame({item["id"]: item for item in out})
        df = pd.DataFrame({item["dateFiled"]: item for item in out})
        df.columns = pd.to_datetime(df.columns)
        return df
