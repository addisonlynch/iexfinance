Welcome to iexfinance's documentation!
======================================

``iexfinance``'s documentation is organized into the following sections:

- :ref:`getting_started` - Installation instructions, basic usage information,
  migrating to IEX Cloud
- :ref:`endpoints` - 1:1 mirror of the `IEX Cloud documentation <https://iexcloud.io/api/>`__
- :ref:`package_info` - additional package information, developer/testing documentation

.. warning:: **IEX will end support for the Legacy v1 Devleoper API on June
             1st, 2019.** At that time, the use of ``iexfinance`` will require
             an IEX Cloud account_. In addition, support for all *legacy only*
             endpoints will be discontinued.

.. _account: https://iexcloud.io/pricing/

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
