Welcome to iexfinance's documentation!
======================================

``iexfinance``'s documentation is organized into the following sections:

- :ref:`getting_started` - Installation instructions and basic usage information
- :ref:`endpoints` - (mostly) 1:1 mirror of the `IEX Cloud documentation <https://iexcloud.io/api/>`__
- :ref:`package_info` - additional package information, developer/testing documentation

.. note:: iexfinance is now a pandas-driven library. The default output format is now a pandas ``DataFrame``.

.. warning:: Support for Python 2 has ended as of ``iexfinance`` version 0.5.0.

.. _account: https://iexcloud.io/pricing/

Full Contents
-------------

.. _getting_started:

.. toctree::
   :maxdepth: 1
   :caption: Getting Started

   usage
   whatsnew
   install
   configuration
   sandbox

.. _endpoints:

.. toctree::
   :maxdepth: 2
   :caption: Core Data

   stocks
   market-info
   news
   crypto
   options
   refdata
   iexdata
   altdata
   data-apis

.. _utility:

.. toctree::
   :maxdepth: 2
   :caption: Utility endpoints

   account
   apidata

.. _package_info:

.. toctree::
   :maxdepth: 1
   :caption: Package Information

   about
   logging
   caching
   testing
   tutorial
   modules

Modules
-------

* :ref:`Modules <modules>`__
