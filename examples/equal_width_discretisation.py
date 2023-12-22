"""
Example demonstrates how to discretise
a dataset using the equal width method
"""

from arm_preprocessing.dataset import Dataset

# Initialise dataset with filename and format
dataset = Dataset('datasets/sportydatagen', format='csv')

# Load dataset
dataset.load()

# Discretise dataset using equal width discretisation
dataset.discretise(method='equal_width', num_bins=5, columns=['calories'])

# Number of values in each bin
print(dataset.data['calories'].value_counts())
