<p align="center">
  <img alt="logo" width="300" src=".github/images/logo_black.png">
</p>

<h1 align="center">
  arm-preprocessing
</h1>

<p align="center">
  <img alt="PyPI Version" src="https://img.shields.io/pypi/v/arm-preprocessing.svg">
  <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/arm-preprocessing.svg">
  <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/arm-preprocessing.svg" href="https://pepy.tech/project/arm-preprocessing">
  <a href="https://repology.org/project/python:arm-preprocessing/versions">
    <img alt="Packaging status" src="https://repology.org/badge/tiny-repos/python:arm-preprocessing.svg">
  </a>
  <a href="https://pepy.tech/project/arm-preprocessing">
    <img alt="Downloads" src="https://static.pepy.tech/badge/arm-preprocessing">
  </a>
  <img alt="License" src="https://img.shields.io/github/license/firefly-cpp/arm-preprocessing.svg">
  <a href="https://github.com/firefly-cpp/arm-preprocessing/actions/workflows/test.yml">
    <img alt="arm-preprocessing" src="https://github.com/firefly-cpp/arm-preprocessing/actions/workflows/test.yml/badge.svg">
  </a>
  <a href="https://arm-preprocessing.readthedocs.io/en/latest/?badge=latest">
    <img alt="Documentation Status" src="https://readthedocs.org/projects/arm-preprocessing/badge/?version=latest">
  </a>
</p>

<p align="center">
  <img alt="Repository size" src="https://img.shields.io/github/repo-size/firefly-cpp/arm-preprocessing">
  <img alt="Open issues" src="https://isitmaintained.com/badge/open/firefly-cpp/arm-preprocessing.svg">
  <a href='http://isitmaintained.com/project/firefly-cpp/arm-preprocessing "Average time to resolve an issue"'>
    <img alt="Average time to resolve an issue" src="http://isitmaintained.com/badge/resolution/firefly-cpp/arm-preprocessing.svg">
  </a>
  <img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/w/firefly-cpp/arm-preprocessing.svg">
  <img alt="GitHub contributors" src="https://img.shields.io/github/contributors/firefly-cpp/arm-preprocessing.svg">
</p>

<p align="center">
  <a href="#-why-arm-preprocessing">💡 Why arm-preprocessing?</a> •
  <a href="#-key-features">✨ Key features</a> •
  <a href="#-installation">📦 Installation</a> •
  <a href="#-usage">🚀 Usage</a> •
  <a href="#-related-frameworks">🔗 Related frameworks</a> •
  <a href="#-references">📚 References</a> •
  <a href="#-license">🔑 License</a>
</p>

arm-preprocessing is a lightweight Python library supporting several key steps involving data preparation, manipulation, and discretisation for Association Rule Mining (ARM). 🧠 Embrace its minimalistic design that prioritises simplicity. 💡 The framework is intended to be fully extensible and offers seamless integration with related ARM libraries (e.g., [NiaARM](https://github.com/firefly-cpp/NiaARM)). 🔗

* **Free software:** MIT license
* **Documentation**: [http://arm-preprocessing.readthedocs.io](http://arm-preprocessing.readthedocs.io)
* **Python**: 3.9.x, 3.10.x, 3.11.x, 3.12x
* **Tested OS:** Windows, Ubuntu, Fedora, Alpine, Arch, macOS. **However, that does not mean it does not work on others**

## 💡 Why arm-preprocessing?

While numerous libraries facilitate data mining preprocessing tasks, this library is designed to integrate seamlessly with association rule mining. It harmonises well with the NiaARM library, a robust numerical association rule mining framework. The primary aim is to bridge the gap between preprocessing and rule mining, simplifying the workflow/pipeline. Additionally, its design allows for the effortless incorporation of new preprocessing methods and fast benchmarking.

## ✨ Key features

- Loading various formats of datasets (CSV, JSON, TXT, TCX) 📊
- Converting datasets to different formats 🔄
- Loading different types of datasets (numerical dataset, discrete dataset, time-series data, text, etc.) 📉
- Dataset identification (which type of dataset) 🔍
- Dataset statistics 📈
- Discretisation methods 📏
- Data squashing methods 🤏
- Feature scaling methods ⚖️
- Feature selection methods 🎯

## 📦 Installation

### pip

To install ``arm-preprocessing`` with pip, use:
```bash
pip install arm-preprocessing
```

To install ``arm-preprocessing`` on Alpine Linux, please use:
```sh
$ apk add py3-arm-preprocessing
```

To install ``arm-preprocessing`` on Arch Linux, please use an [AUR helper](https://wiki.archlinux.org/title/AUR_helpers):
```sh
$ yay -Syyu python-arm-preprocessing
```

## 🚀 Usage

### Data loading

The following example demonstrates how to load a dataset from a file (csv, json, txt). More examples can be found in the [examples/data_loading](./examples/data_loading/) directory:
- [Loading a dataset from a CSV file](./examples/data_loading/load_dataset_csv.py)
- [Loading a dataset from a JSON file](./examples/data_loading/load_dataset_json.py)
- [Loading a dataset from a TCX file](./examples/data_loading/load_dataset_tcx.py)
- [Loading a time-series dataset](./examples/data_loading/load_dataset_timeseries.py)

```python
from arm_preprocessing.dataset import Dataset

# Initialise dataset with filename (without format) and format (csv, json, txt)
dataset = Dataset('path/to/datasets', format='csv')

# Load dataset
dataset.load_data()
df = dataset.data
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

### Feature scaling

The following example demonstrates how to scale the dataset's features. More examples can be found in the [examples/scaling](./examples/scaling) directory:
- [Scale features using normalisation](./examples/scaling/normalisation.py)
- [Scale features using standardisation](./examples/scaling/standardisation.py)

```python
from arm_preprocessing.dataset import Dataset

# Initialise dataset with filename and format
dataset = Dataset('datasets/Abalone', format='csv')
dataset.load()

# Scale dataset using normalisation
dataset.scale(method='normalisation')
```

### Feature selection

The following example demonstrates how to select features from a dataset. More examples can be found in the [examples/feature_selection](./examples/feature_selection) directory:
- [Select features using the Kendall Tau correlation coefficient](./examples/feature_selection/feature_selection.py)

```python
from arm_preprocessing.dataset import Dataset

# Initialise dataset with filename and format
dataset = Dataset('datasets/sportydatagen', format='csv')
dataset.load()

# Feature selection
dataset.feature_selection(
    method='kendall', threshold=0.15, class_column='calories')
```

## 🔗 Related frameworks

[1] [NiaARM: A minimalistic framework for Numerical Association Rule Mining](https://github.com/firefly-cpp/NiaARM)

[2] [uARMSolver: universal Association Rule Mining Solver](https://github.com/firefly-cpp/uARMSolver)

## 📚 References

[1] I. Fister, I. Fister Jr., D. Novak and D. Verber, [Data squashing as preprocessing in association rule mining](https://iztok-jr-fister.eu/static/publications/300.pdf), 2022 IEEE Symposium Series on Computational Intelligence (SSCI), Singapore, Singapore, 2022, pp. 1720-1725, doi: 10.1109/SSCI51031.2022.10022240.

[2] I. Fister Jr., I. Fister [A brief overview of swarm intelligence-based algorithms for numerical association rule mining](https://arxiv.org/abs/2010.15524). arXiv preprint arXiv:2010.15524 (2020).

## 🔑 License

This package is distributed under the MIT License. This license can be found online
at <http://www.opensource.org/licenses/MIT>.

## Disclaimer

This framework is provided as-is, and there are no guarantees that it fits your purposes or that it is bug-free. Use it at your own risk!
