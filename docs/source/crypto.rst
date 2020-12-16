.. _crypto:

Cryptocurrency
==============

.. _crypto.contents:

.. contents::
    :depth: 2

.. _crypto.book:

Cryptocurrency Book
-------------------

.. autofunction:: iexfinance.crypto.get_crypto_book

.. _crypto.price:

Cryptocurrency Price
--------------------

.. autofunction:: iexfinance.crypto.get_crypto_price


.. _crypto.quote:

Cryptocurrency Quote
--------------------

To retrieve quotes for all available cryptocurrencies, create a ``Stock`` object
using a cryptocurrency ticker.

.. autofunction:: iexfinance.crypto.get_crypto_quote


.. _crypto.quote.examples:

Examples
~~~~~~~~

.. code-block:: python

    from iexfinance.stocks import Stock

    btc = Stock("BTCUSDT")
    btc.get_quote()
