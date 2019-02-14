Welcome to iexfinance's documentation!
======================================

``iexfinance``'s documentation is organized into the following sections:

- :ref:`getting_started` - Installation instructions, basic usage information,
  migrating to IEX Cloud
- :ref:`endpoints` - 1:1 mirror of the `IEX Cloud documentation <https://iexcloud.io/api/>`__
- :ref:`package_info` - additional package information, developer/testing documentation

.. note:: ``iexfinance`` version 0.4.0 introduces a number of new endpoint groups, including :ref:`altdata`, :ref:`account`, and :ref:`apidata`. Certain modules are also refactored or renamed, including :ref:`refdata` and :ref:`iexdata` (formerly IEX Stats and IEX Market Data). For more information, see :ref:`migrating`.

Full Contents
-------------

.. _getting_started:

.. toctree::
   :maxdepth: 1
   :caption: Getting Started

   whatsnew
   migrating
   install
   configuration
   usage

.. _endpoints:

.. toctree::
   :maxdepth: 2
   :caption: Endpoints

   account
   stocks
   altdata
   refdata
   iexdata
   apidata

.. _package_info:

.. toctree::
   :maxdepth: 1
   :caption: Package Information

   about
   caching
   testing
   tutorial
   modules

Modules
-------

* `Modules <modules.html>`__
