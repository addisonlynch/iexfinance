import pytest

from iexfinance.stocks import get_ipo_calendar


class TestIPOCalendar(object):
    def test_ipo_calendar(self):
        data = get_ipo_calendar()

        assert isinstance(data, list)

    def test_ipo_calendar_bad_period(self):
        with pytest.raises(ValueError):
            get_ipo_calendar("BADPERIOD")
