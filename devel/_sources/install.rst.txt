.. _install:


Installation
============

Dependencies
------------

iexfinance relies on:

-  `pandas <http://pandas.pydata.org>`__
-  `requests <http://docs.python-requests.org>`__

For testing requirements, see :ref:`testing.dependencies`.

Installation
------------

Latest stable release via pip (recommended):

.. code:: bash

    $ pip install iexfinance

Latest development version:

.. code:: bash

    $ pip install git+https://github.com/addisonlynch/iexfinance.git

or

.. code:: bash

     $ git clone https://github.com/addisonlynch/iexfinance.git
     $ cd iexfinance
     $ pip install .

**Note:**

The use of
`virtualenv <http://docs.python-guide.org/en/latest/dev/virtualenvs/>`__
is recommended as below:

.. code:: bash

    $ pip install virtualenv
    $ virtualenv env
    $ source env/bin/activate
