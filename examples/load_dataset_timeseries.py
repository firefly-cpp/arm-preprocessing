"""
Example demonstrates how to load
a dataset with time series data
"""

from arm_preprocessing.dataset import Dataset

# Initialise dataset with filename, format, and datetime columns
dataset = Dataset('datasets/measures2', format='txt',
                  datetime_columns=['date', 'time'])

# Load dataset
dataset.load_data()

# Print dataset information (columns, categories, min/max values, etc.)
dataset.dataset_statistics()
