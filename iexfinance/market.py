from .base import _IEXBase
from iexfinance.utils import IEXSymbolError


class Market(_IEXBase):
    """
    Base class for obtaining date from the market endpoints
    of IEX. Subclass of _IEXBase, subclassed by various.
    """
    def __init__(self, *args, **kwargs):
        if isinstance(args[0], str):
            self.symbolList = [args[0]]
        elif len(args[0]) in range(0, 10):
            self.symbolList = args[0]
        else:
            raise IEXSymbolError(self.symbolList)
        super(Market, self).__init__(*args, **kwargs)

    @property
    def params(self):
        return {"symbols": ",".join(self.symbolList)}


class TOPS(Market):
    """
    Class for obtaining data from the TOPS endpoint
    """
    @property
    def url(self):
        return "tops"


class Last(Market):
    """
    Class for obtaining data from the Last endpoint
    """
    @property
    def url(self):
        return "tops/last"


class DEEP(Market):
    """
    Class for obtaining data from the DEEP endpoint
    """
    @property
    def url(self):
        return "deep"


class Book(Market):
    """
    Class for obtaining data from the Book endpoint
    """
    @property
    def url(self):
        return "deep/book"
