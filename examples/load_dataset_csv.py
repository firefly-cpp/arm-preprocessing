"""
Example demonstrates how to load
a dataset from a CSV file
"""

from arm_preprocessing.dataset import Dataset

# Initialise dataset with filename and format
dataset = Dataset('datasets/breast', format='csv')

# Load dataset
dataset.load()

# Print dataset information (columns, categories, min/max values, etc.)
dataset.dataset_statistics()
