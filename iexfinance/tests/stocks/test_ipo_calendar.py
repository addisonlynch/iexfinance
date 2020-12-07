import pytest

from iexfinance.stocks import get_ipo_calendar


class TestIPOCalendar(object):
    @pytest.mark.xfail(reason="Endpoint temporarily disabled by provider.", strict=True)
    def test_ipo_calendar(self):
        data = get_ipo_calendar()

        assert isinstance(data, list)

    def test_ipo_calendar_bad_period(self):
        with pytest.raises(ValueError):
            get_ipo_calendar("BADPERIOD")
