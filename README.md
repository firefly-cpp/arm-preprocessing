# About

arm-preprocessing is a lightweight Python library supporting several key steps involving data preparation, manipulation, and discretization for Association Rule Mining (ARM). The design of this framework has a minimalistic design outlook in mind and is intended to be fully extensible and allow easy integration with other related ARM libraries, e.g., NiaARM.

## Key features

### Dataset processing

- Loading various formats of datasets (CSV, JSON, TXT)
- Converting datasets in different formats
- Loading different types of datasets (numerical dataset, discrete dataset, time-series data, text)
- Dataset identification (which type of dataset)
- Dataset statistics

### Dataset manipulation

- Support for dealing with missing data in ARM datasets
- Data squashing algorithms Implementation
-

### Time-series dataset support operations

- Converting time attributes
-

### Association rule text mining

### Dataset visualization

### Other

-

## Usage
### Data loading
The following example demonstrates how to load a dataset from a file (csv, json, txt). More examples can be found in the [examples](./examples) directory:
- [Loading a dataset from a CSV file](./examples/load_dataset_csv.py)
- [Loading a dataset from a JSON file](./examples/load_dataset_json.py)
- [Loading a time-series dataset](./examples/load_dataset_timeseries.py)

```python
from arm_preprocessing.dataset import Dataset

# Initialise dataset with filename (without format) and format (csv, json, txt)
dataset = Dataset('path/to/datasets', format='csv')

# Load dataset
dataset.load_data()
df = dataset.data
```


## Related frameworks

[1] [NiaARM: A minimalistic framework for Numerical Association Rule Mining](https://github.com/firefly-cpp/NiaARM) 

## References

[1] I. Fister, I. Fister Jr., D. Novak and D. Verber, [Data squashing as preprocessing in association rule mining](https://iztok-jr-fister.eu/static/publications/300.pdf), 2022 IEEE Symposium Series on Computational Intelligence (SSCI), Singapore, Singapore, 2022, pp. 1720-1725, doi: 10.1109/SSCI51031.2022.10022240.

## License

This package is distributed under the MIT License. This license can be found online
at <http://www.opensource.org/licenses/MIT>.

## Disclaimer

This framework is provided as-is, and there are no guarantees that it fits your purposes or that it is bug-free. Use it at your own risk!
