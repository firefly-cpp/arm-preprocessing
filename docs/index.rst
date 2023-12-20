arm-preprocessing
=================

About
-----

arm-preprocessing is a lightweight Python library supporting several key steps involving data preparation, manipulation, and discretization for Association Rule Mining (ARM). The design of this framework has a minimalistic design outlook in mind and is intended to be fully extensible and allow easy integration with other related ARM libraries, e.g., NiaARM.

Key features
------------

Dataset processing
~~~~~~~~~~~~~~~~~~

*   Loading various formats of datasets (CSV, JSON, TXT)
*   Converting datasets in different format
*   Loading different types of datasets (numerical dataset, discrete dataset, time-series data, text)
*   Dataset identification (which type of dataset)
*   Dataset statistics

Dataset manipulation
~~~~~~~~~~~~~~~~~~~~

*   Support for dealing with missing data in ARM datasets
*   Data squashing algoriths implementation

Time-series dataset support operations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*   Converting time attributes

Association rule text mining
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Dataset visualisation
~~~~~~~~~~~~~~~~~~~~~

Other
~~~~~

Documentation
-------------

The documentation is organised into the following sections:

*   :ref:`user`
*   :ref:`dev`
*   :ref:`about`

..  _user:

..  toctree::
    :maxdepth: 1
    :caption: User documentation

    user/usage

..  _dev:

..  toctree::
    :maxdepth: 1
    :caption: Developer documentation

    dev/installation
    dev/testing
    dev/documentation

..  _about:

..  toctree::
    :maxdepth: 2
    :caption: About
    
    about/license
