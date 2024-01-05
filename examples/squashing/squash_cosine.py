"""
Example of squashing a dataset using 
cosine similarity.
"""

from arm_preprocessing.dataset import Dataset

# Initialise dataset with filename and format
dataset = Dataset('datasets/Abalone', format='csv')

# Load dataset
dataset.load()

# Drop 'Sex' column from dataset.data
dataset.data.drop('Sex', axis=1, inplace=True)

# Print dataset size before squashing
print(len(dataset.data))

# Squash dataset
dataset.squash(threshold=0.99, similarity='cosine')

# Print dataset size after squashing
print(len(dataset.data))
