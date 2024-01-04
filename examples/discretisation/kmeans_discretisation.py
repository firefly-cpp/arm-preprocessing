"""
Example demonstrates how to discretise
a dataset using k-means clustering
"""

from arm_preprocessing.dataset import Dataset

# Initialise dataset with filename and format
dataset = Dataset('datasets/measures2', format='txt',
                  datetime_columns=['date', 'time'])

# Load dataset
dataset.load()

# Discretise dataset using equal width discretisation
dataset.discretise(method='kmeans',
                   num_bins=5, columns=['temperature'])

# Number of values in each bin
print(dataset.data['temperature'].value_counts())
