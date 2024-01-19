"""
Example demonstrates how to scale
the using standardisation
"""

from arm_preprocessing.dataset import Dataset

# Initialise dataset with filename and format
dataset = Dataset('datasets/Abalone', format='csv')
dataset.load()

# Scale dataset using standardisation
dataset.scale(method='standardisation')
