# Install

## Dependencies

iexfinance relies on:

- pandas
- requests
- simplejson
- mock (testing)
- nose (testing)

See requirements.txt.



## Installation

Latest stable release via pip (recommended):

```bash
$ pip install iexfinance
```

Latest development version:

```bash
$ pip install git+https://github.com/addisonlynch/iexfinance.git
```

or

```bash
 $ git clone https://github.com/addisonlynch/iexfinance.git  
 $ cd iexfinance  
 $ pip install . 
```


**Note:**

The use of [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) is recommended as below:

```bash
$ pip install virtualenv
$ virtualenv env
$ source env/bin/activate
```