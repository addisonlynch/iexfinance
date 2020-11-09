import pandas as pd
import pytest

from iexfinance.stocks import get_collections


class TestCollections(object):
    def test_collections(self):
        data = get_collections("Technology", "sector")

        assert isinstance(data, pd.DataFrame)
        assert "companyName" in data.columns

    def test_collections_bad_type(self):
        with pytest.raises(TypeError):
            get_collections()

        with pytest.raises(ValueError):
            get_collections("Technology", "BADTYPE")

    def test_collections_empty_name(self):
        data = get_collections("BADNAME", "sector")

        assert data.empty
