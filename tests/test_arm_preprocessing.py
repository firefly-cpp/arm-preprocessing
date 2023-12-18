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
    data = dataset.load_data()
    assert isinstance(data, pd.DataFrame)


def test_load_data_txt_datetime():
    # Test loading CSV without datetime columns
    dataset = Dataset('datasets/measures2', format='txt',
                      datetime_columns=['date', 'time'])
    data = dataset.load_data()
    assert isinstance(data, pd.DataFrame)
    assert data['date_time'].dtype == 'datetime64[ns]'


def test_load_data_json_no_datetime():
    # Test loading CSV without datetime columns
    dataset = Dataset('datasets/artm_test_dataset', format='json')
    data = dataset.load_data()
    assert isinstance(data, pd.DataFrame)


def test_convert_data_csv():
    # Test converting data to CSV format
    dataset = Dataset('datasets/artm_test_dataset', format='json')
    data = dataset.load_data()

    # Convert data
    dataset.convert_data(
        data, target_format='csv', output_filename='tests/conv_data')

    try:
        # Assert output file exists
        assert os.path.exists('tests/conv_data.csv')
    finally:
        # Delete output file
        os.remove('tests/conv_data.csv')


def test_convert_data_json():
    # Test converting data to JSON format
    dataset = Dataset('datasets/nursery', format='csv')
    data = dataset.load_data()

    # Convert data
    dataset.convert_data(
        data, target_format='json', output_filename='tests/conv_data')

    try:
        # Assert output file exists
        assert os.path.exists('tests/conv_data.json')
    finally:
        # Delete output file
        os.remove('tests/conv_data.json')


def test_convert_invalid_format():
    # Test invalid format handling
    dataset = Dataset('datasets/nursery', format='csv')
    data = dataset.load_data()

    with pytest.raises(ValueError, match='Target format not specified'):
        # Convert data
        dataset.convert_data(data)
