"""
Example demonstrates how to impute
missing values
"""

from arm_preprocessing.dataset import Dataset

# Initialise dataset with filename and format
dataset = Dataset('examples/missing_values/data', format='csv')

# Load dataset
dataset.load()

# Print number of missing values
print(dataset.data.isnull().sum())
print(dataset.data.shape)

# Impute missing data
dataset.missing_values(method='impute')

# Print number of missing values
print(dataset.data.isnull().sum())
print(dataset.data.shape)
