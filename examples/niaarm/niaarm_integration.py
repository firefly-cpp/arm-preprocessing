from arm_preprocessing.dataset import Dataset
import niaarm
from niapy.algorithms.basic import DifferentialEvolution

# Load dataset
dataset = Dataset('datasets/Abalone', format='csv')
dataset.load()

# Squash dataset
dataset.squash(threshold=0.85, similarity='euclidean')

# Impute missing values
dataset.missing_values(method='impute')

# Drop 'Sex' column
dataset.data.drop('Sex', axis=1, inplace=True)

# Scale dataset
dataset.scale(method='normalisation')

# Feature selection
dataset.feature_selection(
    method='kendall', threshold=0.25, class_column='Rings')

# Discretise dataset using equal width, equal frequency, and k-means
dataset.discretise(method='equal_width', num_bins=10, columns=['Height'])
dataset.discretise(method='equal_frequency', num_bins=5, columns=['Diameter'])
dataset.discretise(method='kmeans', num_bins=5, columns=[
                   'Whole weight', 'Shell weight'])

# Identify dataset and output dataset statistics
dataset.identify_dataset()
dataset.dataset_statistics()

# Association rule mining
algo = DifferentialEvolution(
    population_size=50, differential_weight=0.5, crossover_probability=0.9)
metrics = ('support', 'confidence')
rules, run_time = niaarm.get_rules(
    niaarm.Dataset(dataset.data), algo, metrics, max_iters=30, logging=True)

# Results
print(rules)
print(f'Run Time: {run_time}')
rules.to_csv('output.csv')
