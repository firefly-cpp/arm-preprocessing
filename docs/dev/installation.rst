Installation
============

Development environment
-----------------------

Requirements
~~~~~~~~~~~~

- Python: https://www.python.org
- Poetry: https://python-poetry.org/docs

After installing Poetry and cloning the project from GitHub, execute the following command in the root directory of the cloned project:

.. code:: sh

    poetry install

All of the project's dependencies should be installed and the project should be ready for further development. Note that Poetry creates a separate virtual environment for the project.

Development dependencies
~~~~~~~~~~~~~~~~~~~~~~~~

List of arm-preprocessing's dependencies:

+---------------------------+----------------------+
| Package                   | Version              |
+===========================+======================+
| pandas                    | ^1.5.0               |
+---------------------------+----------------------+
| sphinx                    | ^5.0                 |
+---------------------------+----------------------+
| sphinx-rtd-theme          | ^1.0.0               |
+---------------------------+----------------------+
| scikit/learn              | ^1.3.2               |
+---------------------------+----------------------+
| niaarm                    | ^0.3.5               |
+---------------------------+----------------------+
| sport-activities-features | ^0.3.18              |
+---------------------------+----------------------+

List of arm-preprocessing's development dependencies:

+----------------------+----------------------+
| Package              | Version              |
+======================+======================+
| pytest               | ^7.4.4               |
+----------------------+----------------------+