# Historical Date






## Plotting

With Pandas output formatting, we are able to plot historical price movements using matplotlib.

```python

from iexfinance import get_historical_data
from datetime import datetime
import matplotlib.pyplot as plt
start = datetime(2017, 2, 9)
end = datetime(2017, 5, 24)

f = get_historical_data("AAPL", start, end, outputFormat='pandas')
plt.plot(f["close"])
plt.title('Time series chart for AAPL')
plt.show()

```

