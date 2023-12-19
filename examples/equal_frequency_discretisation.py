"""
Example demonstrates how to discretise
a dataset using the equal frequency method
"""

from arm_preprocessing.dataset import Dataset

# Initialise dataset with filename and format
dataset = Dataset('datasets/measures2', format='txt',
                  datetime_columns=['date', 'time'])

# Load dataset
dataset.load_data()

# Discretise dataset using equal width discretisation
dataset.discretise(method='equal_frequency',
                   num_bins=3, columns=['temperature'])

# Number of values in each bin
print(dataset.data['temperature'].value_counts())
