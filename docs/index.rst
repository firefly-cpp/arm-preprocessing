arm-preprocessing
=================

About
-----

arm-preprocessing is a lightweight Python library supporting several key steps involving data preparation, manipulation, and discretisation for Association Rule Mining (ARM). 🧠 Embrace its minimalistic design that prioritises simplicity. 💡 The framework is intended to be fully extensible and offers seamless integration with related ARM libraries, e.g., NiaARM. 🔗

Key features
------------

*   Loading various formats of datasets (CSV, JSON, TXT, TCX) 📊
*   Converting datasets to different formats 🔄
*   Loading different types of datasets (numerical dataset, discrete dataset, time-series data, text, etc.) 📉
*   Dataset identification (which type of dataset) 🔍
*   Dataset statistics 📈
*   Discretisation methods 📏
*   Data squashing methods 🤏

Documentation
-------------

The documentation is organised into the following sections:

*   :ref:`user`
*   :ref:`dev`
*   :ref:`arm_preprocessing`
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

..  _arm_preprocessing:

..  toctree::
    :maxdepth: 2
    :caption: ARM Preprocessing

    arm_preprocessing/index

..  _about:

..  toctree::
    :maxdepth: 2
    :caption: About
    
    about/license
