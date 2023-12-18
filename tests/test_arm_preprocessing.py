import pytest
import pandas as pd

from arm_preprocessing import __version__
from arm_preprocessing.dataset import Dataset


def test_version():
    assert __version__ == '0.1.0'


def test_load_data_csv_no_datetime():
    # Test loading CSV without datetime columns
    dataset = Dataset('datasets/nursery.csv', format='csv')
    data = dataset.load_data()
    assert isinstance(data, pd.DataFrame)


def test_load_data_txt_datetime():
    # Test loading CSV without datetime columns
    dataset = Dataset('datasets/measures2.txt', format='txt',
                      datetime_columns=['date', 'time'])
    data = dataset.load_data()
    assert isinstance(data, pd.DataFrame)
    assert data['date_time'].dtype == 'datetime64[ns]'


def test_load_data_json_no_datetime():
    # Test loading CSV without datetime columns
    dataset = Dataset('datasets/artm_test_dataset.json', format='json')
    data = dataset.load_data()
    assert isinstance(data, pd.DataFrame)
