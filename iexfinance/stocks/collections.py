from iexfinance.base import _IEXBase

# Data provided for free by IEX
# See https://iextrading.com/api-exhibit-a/ for additional information
# and conditions of use


class CollectionsReader(_IEXBase):
    """
    Class for retrieving data from the Collections endpoint
    """

    _COLLECTION_TYPES = ["tag", "sector", "list"]

    def __init__(self, collection_name, collection_type, **kwargs):
        self.collection_name = collection_name
        self.collection_type = collection_type
        if self.collection_type not in self._COLLECTION_TYPES:
            raise ValueError("Please select a valid collection type.")
        # deal with collection name with spaces
        super(CollectionsReader, self).__init__(**kwargs)

    @property
    def url(self):
        return "stock/market/collection/%s" % self.collection_type

    @property
    def params(self):
        return {"collectionName": self.collection_name}
