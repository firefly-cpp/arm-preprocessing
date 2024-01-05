"""
Example demonstrates how to remove
columns with missing values
"""

from arm_preprocessing.dataset import Dataset

# Initialise dataset with filename and format
dataset = Dataset('examples/missing_values/data', format='csv')

# Load dataset
dataset.load()

# Print number of missing values
print(dataset.data.isnull().sum())
print(dataset.data.shape)

# Remove columns with missing data
dataset.missing_values(method='column')

# Print number of missing values
print(dataset.data.isnull().sum())
print(dataset.data.shape)
