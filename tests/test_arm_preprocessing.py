import os
import pytest
import pandas as pd

from arm_preprocessing import __version__
from arm_preprocessing.dataset import Dataset


def test_version():
    assert __version__ == '0.1.0'


def test_load_data_csv_no_datetime():
    # Test loading CSV without datetime columns
    dataset = Dataset('datasets/nursery', format='csv')
    dataset.load_data()
    assert isinstance(dataset.data, pd.DataFrame)


def test_load_data_txt_datetime():
    # Test loading CSV without datetime columns
    dataset = Dataset('datasets/measures2', format='txt',
                      datetime_columns=['date', 'time'])
    dataset.load_data()
    assert isinstance(dataset.data, pd.DataFrame)
    assert dataset.data['date_time'].dtype == 'datetime64[ns]'


def test_load_data_json_no_datetime():
    # Test loading CSV without datetime columns
    dataset = Dataset('datasets/artm_test_dataset', format='json')
    dataset.load_data()
    assert isinstance(dataset.data, pd.DataFrame)


def test_convert_data_csv():
    # Test converting data to CSV format
    dataset = Dataset('datasets/artm_test_dataset', format='json')
    dataset.load_data()

    # Convert data
    dataset.convert_data(target_format='csv',
                         output_filename='tests/conv_data')

    try:
        # Assert output file exists
        assert os.path.exists('tests/conv_data.csv')
    finally:
        # Delete output file
        os.remove('tests/conv_data.csv')


def test_convert_data_json():
    # Test converting data to JSON format
    dataset = Dataset('datasets/nursery', format='csv')
    dataset.load_data()

    # Convert data
    dataset.convert_data(target_format='json',
                         output_filename='tests/conv_data')

    try:
        # Assert output file exists
        assert os.path.exists('tests/conv_data.json')
    finally:
        # Delete output file
        os.remove('tests/conv_data.json')


def test_convert_invalid_format():
    # Test invalid format handling
    dataset = Dataset('datasets/nursery', format='csv')
    dataset.load_data()

    with pytest.raises(ValueError, match='Target format not specified'):
        # Convert data
        dataset.convert_data()


def test_identify_dataset_timeseries():
    # Test identifying time-series dataset
    dataset = Dataset('datasets/measures2', format='txt',
                      datetime_columns=['date', 'time'])
    dataset.load_data()
    assert dataset.information['type'] == 'time-series'


def test_identify_dataset_mixed():
    # Test identifying mixed dataset
    dataset = Dataset('datasets/artm_test_dataset', format='json')
    dataset.load_data()
    assert dataset.information['type'] == 'mixed'


def test_identify_dataset_numerical():
    # Test identifying numerical dataset
    dataset = Dataset('datasets/sportydatagen', format='csv')
    dataset.load_data()
    assert dataset.information['type'] == 'numerical'


def test_identify_dataset_categorical():
    # Test identifying categorical dataset
    dataset = Dataset('datasets/breast', format='csv')
    dataset.load_data()
    assert dataset.information['type'] == 'categorical'


def test_discretise_equal_width():
    # Test equal width discretisation
    dataset = Dataset('datasets/sportydatagen', format='csv')
    dataset.load_data()
    dataset.discretise(method='equal_width', num_bins=5, columns=['calories'])
    assert dataset.data['calories'].value_counts().shape[0] == 5
    assert dataset.data['calories'].dtype == 'category'


def test_discretise_equal_frequency():
    # Test equal width discretisation
    dataset = Dataset('datasets/measures2', format='txt')
    dataset.load_data()
    dataset.discretise(method='equal_frequency',
                       num_bins=5, columns=['temperature'])
    assert dataset.data['temperature'].value_counts().shape[0] == 5
    assert dataset.data['temperature'].dtype == 'category'
