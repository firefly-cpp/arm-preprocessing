Usage
=====

This section demonstrates the usage of the arm-preprocessing framework.

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