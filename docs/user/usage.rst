Usage
=====

This section demonstrates the usage of the arm-preprocessing framework.

*   :ref:`data loading`
*   :ref:`data discretisation`
*   :ref:`data squashing`

.. _data loading:

Data loading
------------

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

..  _data discretisation:

Data discretisation
-------------------

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
--------------

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