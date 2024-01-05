"""
Example demonstrates how to remove
rows with missing values
"""

from arm_preprocessing.dataset import Dataset

# Initialise dataset with filename and format
dataset = Dataset('examples/missing_values/data', format='csv')

# Load dataset
dataset.load()

# Print number of missing values
print(dataset.data.isnull().sum())
print(dataset.data.shape)

# Remove rows with missing data
dataset.missing_values(method='row')

# Print number of missing values
print(dataset.data.isnull().sum())
print(dataset.data.shape)
