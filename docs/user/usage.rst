Installation
============

To install ``arm-preprocessing`` with pip, use:

..  code:: bash

    pip install arm-preprocessing

Usage
=====

This section demonstrates the usage of the arm-preprocessing framework.

*   :ref:`data loading`
*   :ref:`missing values`
*   :ref:`data discretisation`
*   :ref:`data squashing`
*   :ref:`feature scaling`
*   :ref:`feature selection`

.. _data loading:

Data loading
~~~~~~~~~~~~

The following examples demonstrate how to load a dataset from a file (csv, json, txt).

..  code:: python

    from arm_preprocessing.dataset import Dataset

    # Initialise dataset with filename and format
    dataset = Dataset('datasets/breast', format='csv')

    # Load dataset
    dataset.load()

    # Print dataset information (columns, categories, min/max values, etc.)
    dataset.dataset_statistics()

..  code:: python

    from arm_preprocessing.dataset import Dataset

    # Initialise dataset with filename and format
    dataset = Dataset('datasets/artm_test_dataset', format='json')

    # Load dataset
    dataset.load()

    # Print dataset information (columns, categories, min/max values, etc.)
    dataset.dataset_statistics()

..  code:: python

    from arm_preprocessing.dataset import Dataset

    # Initialise dataset with filename, format, and datetime columns
    dataset = Dataset('datasets/measures2', format='txt',
                    datetime_columns=['date', 'time'])

    # Load dataset
    dataset.load()

    # Print dataset information (columns, categories, min/max values, etc.)
    dataset.dataset_statistics()

    ..  _missing values:

.. _missing values:

Missing values
~~~~~~~~~~~~~~

The following examples demonstrate how to handle missing values in a dataset.

..  code:: python

    from arm_preprocessing.dataset import Dataset

    # Initialise dataset with filename and format
    dataset = Dataset('examples/missing_values/data', format='csv')

    # Load dataset
    dataset.load()

    # Remove columns with missing data
    dataset.missing_values(method='column')

..  code:: python

    from arm_preprocessing.dataset import Dataset

    # Initialise dataset with filename and format
    dataset = Dataset('examples/missing_values/data', format='csv')

    # Load dataset
    dataset.load()

    # Remove rows with missing data
    dataset.missing_values(method='row')

..  code:: python

    from arm_preprocessing.dataset import Dataset

    # Initialise dataset with filename and format
    dataset = Dataset('examples/missing_values/data', format='csv')

    # Load dataset
    dataset.load()

    # Impute missing data
    dataset.missing_values(method='impute')

..  _data discretisation:

Data discretisation
~~~~~~~~~~~~~~~~~~~

The following examples demonstrate how to discretise a dataset.

..  code:: python

    from arm_preprocessing.dataset import Dataset

    # Initialise dataset with filename and format
    dataset = Dataset('datasets/sportydatagen', format='csv')

    # Load dataset
    dataset.load()

    # Discretise dataset using equal width discretisation
    dataset.discretise(method='equal_width', num_bins=5, columns=['calories'])

..  code:: python

    from arm_preprocessing.dataset import Dataset

    # Initialise dataset with filename and format
    dataset = Dataset('datasets/measures2', format='txt',
                    datetime_columns=['date', 'time'])

    # Load dataset
    dataset.load()

    # Discretise dataset using equal width discretisation
    dataset.discretise(method='equal_frequency',
                    num_bins=3, columns=['temperature'])

..  code:: python

    from arm_preprocessing.dataset import Dataset

    # Initialise dataset with filename and format
    dataset = Dataset('datasets/measures2', format='txt',
                    datetime_columns=['date', 'time'])

    # Load dataset
    dataset.load()

    # Discretise dataset using equal width discretisation
    dataset.discretise(method='kmeans',
                    num_bins=5, columns=['temperature'])

..  _data squashing:

Data squashing
~~~~~~~~~~~~~~

The following examples demonstrate how to squash a dataset.

..  code:: python

    from arm_preprocessing.dataset import Dataset

    # Initialise dataset with filename and format
    dataset = Dataset('datasets/breast', format='csv')

    # Load dataset
    dataset.load()

    # Squash dataset
    dataset.squash(threshold=0.75, similarity='euclidean')

..  code:: python

    from arm_preprocessing.dataset import Dataset

    # Initialise dataset with filename and format
    dataset = Dataset('datasets/Abalone', format='csv')

    # Load dataset
    dataset.load()

    # Drop "Sex" column from dataset.data
    dataset.data.drop('Sex', axis=1, inplace=True)

    # Squash dataset
    dataset.squash(threshold=0.99, similarity='cosine')

..  _feature scaling:

Feature scaling
~~~~~~~~~~~~~~~

The following examples demonstrate how to scale a dataset.

..  code:: python

    from arm_preprocessing.dataset import Dataset

    # Initialise dataset with filename and format
    dataset = Dataset('datasets/Abalone', format='csv')
    dataset.load()

    # Scale dataset using normalisation
    dataset.scale(method='normalisation')

..  code:: python

    from arm_preprocessing.dataset import Dataset

    # Initialise dataset with filename and format
    dataset = Dataset('datasets/Abalone', format='csv')
    dataset.load()

    # Scale dataset using standardisation
    dataset.scale(method='standardisation')

..  _feature selection:

Feature selection
~~~~~~~~~~~~~~~~~

The following examples demonstrate how to select features from a dataset.

..  code:: python

    from arm_preprocessing.dataset import Dataset

    # Initialise dataset with filename and format
    dataset = Dataset('datasets/sportydatagen', format='csv')
    dataset.load()

    # Feature selection
    dataset.feature_selection(
        method='kendall', threshold=0.15, class_column='calories')