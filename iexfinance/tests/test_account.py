import pandas as pd
import pytest

from iexfinance.account import get_usage, get_metadata


@pytest.mark.skip
class TestAccount(object):
    def test_usage_json_default(self):
        # This function is defaulting to "messages" type due to bug
        # in provider platform
        data = get_usage()
        assert isinstance(data, dict)
        assert len(data) == 5

    def test_usage_pandas(self):
        data = get_usage(output_format="pandas")
        assert isinstance(data, pd.DataFrame)

    @pytest.mark.xfail(
        reason="This endpoint incorrectly causes an error for " "accounts without rules"
    )
    def test_usage_param(self):
        data = get_usage(quota_type="rules")
        assert isinstance(data, dict)

    def test_usage_fails_bad_param(self):
        with pytest.raises(ValueError):
            get_usage(quota_type="BADTYPE")

    def test_metadata_json(self):
        data = get_metadata()
        assert isinstance(data, dict)
        assert len(data) == 7

    def test_metadata_pandas(self):
        data = get_metadata(output_format="pandas")
        assert isinstance(data, pd.DataFrame)
        assert data.shape == (7, 1)

    @pytest.mark.skip(reason="Not yet implemented by IEX")
    def test_allow_pay_as_you_go(self):
        pass

    @pytest.mark.skip(reason="Not yet implemented by IEX")
    def test_disallow_pay_as_you_go(self):
        pass
