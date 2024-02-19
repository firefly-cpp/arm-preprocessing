"""
Example demonstrates how to load
a dataset from a TCX directory
"""

from arm_preprocessing.dataset import Dataset

# Initialise dataset with path to TCX directory and format
dataset = Dataset('datasets/tcx', format='tcx')

# Load dataset
dataset.load()

# Print dataset information (columns, categories, min/max values, etc.)
dataset.dataset_statistics()
