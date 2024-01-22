"""
Example demonstrates how to keep only 
the most important features in a dataset.
"""

from arm_preprocessing.dataset import Dataset

# Initialise dataset with filename and format
dataset = Dataset('datasets/sportydatagen', format='csv')
dataset.load()

# Feature selection
dataset.feature_selection(
    method='kendall', threshold=0.15, class_column='calories')
