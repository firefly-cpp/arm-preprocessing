"""
Example demonstrates how to scale
the using normalisation
"""

from arm_preprocessing.dataset import Dataset

# Initialise dataset with filename and format
dataset = Dataset('datasets/Abalone', format='csv')
dataset.load()

# Scale dataset using normalisation
dataset.scale(method='normalisation')
