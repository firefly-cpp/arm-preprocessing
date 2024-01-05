"""
Example of squashing a dataset using 
euclidean similarity.
"""

from arm_preprocessing.dataset import Dataset

# Initialise dataset with filename and format
dataset = Dataset('datasets/breast', format='csv')

# Load dataset
dataset.load()

# Print dataset size before squashing
print(len(dataset.data))

# Squash dataset
dataset.squash(threshold=0.75, similarity='euclidean')

# Print dataset size after squashing
print(len(dataset.data))
