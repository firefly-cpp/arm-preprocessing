# arm-preprocessing
![PyPI Version](https://img.shields.io/pypi/v/arm-preprocessing.svg)
[![arm-preprocessing](https://github.com/firefly-cpp/arm-preprocessing/actions/workflows/test.yml/badge.svg)](https://github.com/firefly-cpp/arm-preprocessing/actions/workflows/test.yml)
[![Documentation Status](https://readthedocs.org/projects/arm-preprocessing/badge/?version=latest)](https://arm-preprocessing.readthedocs.io/en/latest/?badge=latest)
![Repository size](https://img.shields.io/github/repo-size/firefly-cpp/arm-preprocessing)
![License](https://img.shields.io/github/license/firefly-cpp/arm-preprocessing.svg)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/firefly-cpp/arm-preprocessing.svg)
![Open issues](https://isitmaintained.com/badge/open/firefly-cpp/arm-preprocessing.svg)
[![Average time to resolve an issue](http://isitmaintained.com/badge/resolution/firefly-cpp/arm-preprocessing.svg)](http://isitmaintained.com/project/firefly-cpp/arm-preprocessing "Average time to resolve an issue")

* **Free software:** MIT license
* **Documentation**: [http://arm-preprocessing.readthedocs.io](http://arm-preprocessing.readthedocs.io)
* **Python**: 3.9.x, 3.10.x, 3.11.x, 3.12x
* **Tested OS:** Windows, Ubuntu, Fedora, Alpine, Arch, macOS. **However, that does not mean it does not work on others**

## About 📋
arm-preprocessing is a lightweight Python library supporting several key steps involving data preparation, manipulation, and discretisation for Association Rule Mining (ARM). 🧠 Embrace its minimalistic design that prioritises simplicity. 💡 The framework is intended to be fully extensible and offers seamless integration with related ARM libraries (e.g., [NiaARM](https://github.com/firefly-cpp/NiaARM)). 🔗

## Key features ✨
- Loading various formats of datasets (CSV, JSON, TXT) 📊
- Converting datasets to different formats 🔄
- Loading different types of datasets (numerical dataset, discrete dataset, time-series data, text, etc.) 📉
- Dataset identification (which type of dataset) 🔍
- Dataset statistics 📈
- Discretisation methods 📏
- Data squashing methods 🤏

## Installation 📦
### pip
To install ``arm-preprocessing`` with pip, use:
```bash
pip install arm-preprocessing
```

## Usage 🚀
### Data loading
The following example demonstrates how to load a dataset from a file (csv, json, txt). More examples can be found in the [examples/data_loading](./examples/data_loading/) directory:
- [Loading a dataset from a CSV file](./examples/data_loading/load_dataset_csv.py)
- [Loading a dataset from a JSON file](./examples/data_loading/load_dataset_json.py)
- [Loading a time-series dataset](./examples/data_loading/load_dataset_timeseries.py)

```python
from arm_preprocessing.dataset import Dataset

# Initialise dataset with filename (without format) and format (csv, json, txt)
dataset = Dataset('path/to/datasets', format='csv')

# Load dataset
dataset.load_data()
df = dataset.data
```

### Data discretisation
The following example demonstrates how to discretise a dataset using the equal width method. More examples can be found in the [examples/discretisation](./examples/discretisation) directory:
- [Discretising a dataset using the equal width method](./examples/discretisation/equal_width_discretisation.py)
- [Discretising a dataset using the equal frequency method](./examples/discretisation/equal_frequency_discretisation.py)
- [Discretising a dataset using k-means clustering](./examples/discretisation/kmeans_discretisation.py)

```python
from arm_preprocessing.dataset import Dataset

# Initialise dataset with filename (without format) and format (csv, json, txt)
dataset = Dataset('datasets/sportydatagen', format='csv')
dataset.load_data()

# Discretise dataset using equal width discretisation
dataset.discretise(method='equal_width', num_bins=5, columns=['calories'])
```

### Data squashing
The following example demonstrates how to squash a dataset using the euclidean similarity. More examples can be found in the [examples/squashing](./examples/squashing) directory:
- [Squashing a dataset using the euclidean similarity](./examples/squashing/squash_euclidean.py)
- [Squashing a dataset using the cosine similarity](./examples/squashing/squash_cosine.py)

```python
from arm_preprocessing.dataset import Dataset

# Initialise dataset with filename and format
dataset = Dataset('datasets/breast', format='csv')
dataset.load()

# Squash dataset
dataset.squash(threshold=0.75, similarity='euclidean')
```

### Missing values
The following example demonstrates how to handle missing values in a dataset using imputation. More examples can be found in the [examples/missing_values](./examples/missing_values) directory:
- [Handling missing values in a dataset using row deletion](./examples/missing_values/missing_values_rows.py)
- [Handling missing values in a dataset using column deletion](./examples/missing_values/missing_values_columns.py)
- [Handling missing values in a dataset using imputation](./examples/missing_values/missing_values_impute.py)

```python
from arm_preprocessing.dataset import Dataset

# Initialise dataset with filename and format
dataset = Dataset('examples/missing_values/data', format='csv')
dataset.load()

# Impute missing data
dataset.missing_values(method='impute')
```

## Related frameworks 🔗

[1] [NiaARM: A minimalistic framework for Numerical Association Rule Mining](https://github.com/firefly-cpp/NiaARM) 

## References 📚

[1] I. Fister, I. Fister Jr., D. Novak and D. Verber, [Data squashing as preprocessing in association rule mining](https://iztok-jr-fister.eu/static/publications/300.pdf), 2022 IEEE Symposium Series on Computational Intelligence (SSCI), Singapore, Singapore, 2022, pp. 1720-1725, doi: 10.1109/SSCI51031.2022.10022240.

[2] I. Fister Jr., I. Fister [A brief overview of swarm intelligence-based algorithms for numerical association rule mining](https://arxiv.org/abs/2010.15524). arXiv preprint arXiv:2010.15524 (2020).

## License

This package is distributed under the MIT License. This license can be found online
at <http://www.opensource.org/licenses/MIT>.

## Disclaimer

This framework is provided as-is, and there are no guarantees that it fits your purposes or that it is bug-free. Use it at your own risk!
