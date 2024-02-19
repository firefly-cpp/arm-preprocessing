import os
import pytest
import pandas as pd
from datetime import datetime

from arm_preprocessing.dataset import Dataset


def test_load_data_csv_no_datetime():
    # Test loading CSV without datetime columns
    dataset = Dataset('datasets/nursery', format='csv')
    dataset.load()
    assert isinstance(dataset.data, pd.DataFrame)


def test_load_data_txt_datetime():
    # Test loading CSV without datetime columns
    dataset = Dataset(
        'datasets/measures2', format='txt', datetime_columns=['date', 'time']
    )
    dataset.load()
    assert isinstance(dataset.data, pd.DataFrame)
    assert dataset.data['date_time'].dtype == 'datetime64[ns]'


def test_load_data_json_no_datetime():
    # Test loading CSV without datetime columns
    dataset = Dataset('datasets/artm_test_dataset', format='json')
    dataset.load()
    assert isinstance(dataset.data, pd.DataFrame)


def test_load_data_tcx():
    # Test loading TCX data
    dataset = Dataset('datasets/tcx', format='tcx')
    dataset.load()
    assert isinstance(dataset.data, pd.DataFrame)
    assert len(dataset.data) == 2


def test_convert_data_csv():
    # Test converting data to CSV format
    dataset = Dataset('datasets/artm_test_dataset', format='json')
    dataset.load()

    # Convert data
    dataset.convert(target_format='csv', output_filename='tests/conv_data')

    try:
        # Assert output file exists
        assert os.path.exists('tests/conv_data.csv')
    finally:
        # Delete output file
        os.remove('tests/conv_data.csv')


def test_convert_data_json():
    # Test converting data to JSON format
    dataset = Dataset('datasets/nursery', format='csv')
    dataset.load()

    # Convert data
    dataset.convert(target_format='json', output_filename='tests/conv_data')

    try:
        # Assert output file exists
        assert os.path.exists('tests/conv_data.json')
    finally:
        # Delete output file
        os.remove('tests/conv_data.json')


def test_convert_invalid_format():
    # Test invalid format handling
    dataset = Dataset('datasets/nursery', format='csv')
    dataset.load()

    with pytest.raises(ValueError, match='Target format not specified'):
        # Convert data
        dataset.convert()


def test_identify_dataset_timeseries():
    # Test identifying time-series dataset
    dataset = Dataset(
        'datasets/measures2', format='txt', datetime_columns=['date', 'time']
    )
    dataset.load()
    assert dataset.information['type'] == 'time-series'


def test_identify_dataset_mixed():
    # Test identifying mixed dataset
    dataset = Dataset('datasets/artm_test_dataset', format='json')
    dataset.load()
    assert dataset.information['type'] == 'mixed'


def test_identify_dataset_numerical():
    # Test identifying numerical dataset
    dataset = Dataset('datasets/sportydatagen', format='csv')
    dataset.load()
    assert dataset.information['type'] == 'numerical'


def test_identify_dataset_categorical():
    # Test identifying categorical dataset
    dataset = Dataset('datasets/breast', format='csv')
    dataset.load()
    assert dataset.information['type'] == 'categorical'


def test_missing_values_impute():
    # Test imputing missing values
    dataset = Dataset('examples/missing_values/data', format='csv')
    dataset.load()
    dataset.missing_values(method='impute')
    assert dataset.data.isnull().sum().sum() == 0


def test_missing_values_columns():
    # Test removing columns with missing values
    dataset = Dataset('examples/missing_values/data', format='csv')
    dataset.load()
    dataset.missing_values(method='column')
    assert dataset.data.isnull().sum().sum() == 0


def test_missing_values_rows():
    # Test removing rows with missing values
    dataset = Dataset('examples/missing_values/data', format='csv')
    dataset.load()
    dataset.missing_values(method='row')
    assert dataset.data.isnull().sum().sum() == 0


def test_missing_values_invalid_method():
    # Test invalid method handling
    dataset = Dataset('examples/missing_values/data', format='csv')
    dataset.load()
    with pytest.raises(ValueError, match='Invalid method'):
        dataset.missing_values(method='invalid_method')


def test_feature_scaling_normalisation():
    # Test feature scaling using normalisation
    dataset = Dataset('datasets/Abalone', format='csv')
    dataset.load()
    dataset.scale(method='normalisation')
    for column in dataset.data.columns:
        # Skip non-numerical columns
        if dataset.data[column].dtype in ['datetime64[ns]', 'object']:
            continue
        assert dataset.data[column].min() >= 0
        assert dataset.data[column].max() <= 1


def test_feature_scaling_standardisation():
    # Test feature scaling using standardisation
    dataset = Dataset('datasets/Abalone', format='csv')
    dataset.load()
    dataset.scale(method='standardisation')
    for column in dataset.data.columns:
        # Skip non-numerical columns
        if dataset.data[column].dtype in ['datetime64[ns]', 'object']:
            continue
        assert dataset.data[column].mean() == pytest.approx(0, abs=0.01)
        assert dataset.data[column].std() == pytest.approx(1, abs=0.01)


def test_feature_scaling_invalid_method():
    # Test invalid method handling
    dataset = Dataset('datasets/Abalone', format='csv')
    dataset.load()
    with pytest.raises(ValueError, match='Invalid scaling method'):
        dataset.scale(method='invalid_method')


def test_feature_selection_numerical():
    # Test feature selection for numerical dataset
    dataset = Dataset('datasets/sportydatagen', format='csv')
    dataset.load()
    no_columns_before = len(dataset.data.columns)
    dataset.feature_selection(
        method='pearson', threshold=0.15, class_column='calories')
    no_columns_after = len(dataset.data.columns)
    assert no_columns_before > no_columns_after


def test_feature_selection_categorical():
    # Test feature selection for categorical dataset
    dataset = Dataset('datasets/Abalone', format='csv')
    dataset.load()
    with pytest.raises(ValueError, match='Column .* is not numerical'):
        dataset.feature_selection(
            method='pearson', threshold=0.15, class_column='Rings')


def test_feature_selection_invalid_method():
    # Test invalid method handling
    dataset = Dataset('datasets/sportydatagen', format='csv')
    dataset.load()
    with pytest.raises(ValueError, match='Invalid feature selection method'):
        dataset.feature_selection(
            method='invalid_method', threshold=0.15, class_column='calories')


def test_filter_between_dates():
    # Test filtering between dates
    dataset = Dataset(
        'datasets/measures2', format='txt', datetime_columns=['date', 'time']
    )
    dataset.load()

    # Filter between valid dates
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2023, 1, 1)
    df = dataset.filter_between_dates(start_date, end_date, 'date_time')
    assert len(df) == 38
    assert df['date_time'].min() >= start_date
    assert df['date_time'].max() <= end_date

    # Raise ValueError for start_date > end_date
    with pytest.raises(ValueError):
        df = dataset.filter_between_dates(
            start_date=end_date, end_date=start_date, datetime_column='date_time'
        )

    # No filtering when start_date and end_date are None
    df = dataset.filter_between_dates()
    assert df.equals(dataset.data)

    # No filtering when datetime_column is None
    df = dataset.filter_between_dates(start_date=start_date, end_date=end_date)
    assert df.equals(dataset.data)


def test_filter_by_minute():
    # Test filtering by minute
    dataset = Dataset(
        'datasets/measures2', format='txt', datetime_columns=['date', 'time']
    )
    dataset.load()

    # Filter by valid minute
    minute_to_filter = 40
    df = dataset.filter_by_minute(
        minute=minute_to_filter, datetime_column='date_time')
    assert len(df) == 8
    assert all(df['date_time'].dt.minute == minute_to_filter)

    # No filtering when minute is None
    df = dataset.filter_by_minute(datetime_column='date_time')
    assert df.equals(dataset.data)

    # No filtering when datetime_column is None
    df = dataset.filter_by_minute(minute=minute_to_filter)
    assert df.equals(dataset.data)


def test_filter_by_hour():
    # Test filtering by hour
    dataset = Dataset(
        'datasets/measures2', format='txt', datetime_columns=['date', 'time']
    )
    dataset.load()

    # Filter by valid hour
    hour_to_filter = 16
    df = dataset.filter_by_hour(
        hour=hour_to_filter, datetime_column='date_time')
    assert len(df) == 38
    assert all(df['date_time'].dt.hour == hour_to_filter)

    # No filtering when hour is None
    dataset.filter_by_hour(datetime_column='date_time')
    assert df.equals(dataset.data)

    # No filtering when datetime_column is None
    dataset.filter_by_hour(hour=hour_to_filter)
    assert df.equals(dataset.data)


def test_filter_by_day():
    # Test filtering by day
    dataset = Dataset(
        'datasets/measures2', format='txt', datetime_columns=['date', 'time']
    )
    dataset.load()

    # Filter by valid day
    day_to_filter = 14
    df = dataset.filter_by_day(day=day_to_filter, datetime_column='date_time')
    assert len(df) == 38
    assert all(df['date_time'].dt.day == day_to_filter)

    # No filtering when day is None
    dataset.filter_by_day(datetime_column='date_time')
    assert df.equals(dataset.data)

    # No filtering when datetime_column is None
    dataset.filter_by_day(day=day_to_filter)
    assert df.equals(dataset.data)


def test_filter_by_weekday():
    # Test filtering by weekday
    dataset = Dataset(
        'datasets/measures2', format='txt', datetime_columns=['date', 'time']
    )
    dataset.load()

    # Filter by valid weekday (e.g., Monday, represented as 0)
    weekday_to_filter = 2
    df = dataset.filter_by_weekday(
        weekday=weekday_to_filter, datetime_column='date_time'
    )
    assert len(df) == 38
    assert all(df['date_time'].dt.weekday == weekday_to_filter)

    # No filtering when weekday is None
    dataset.filter_by_weekday(datetime_column='date_time')
    assert df.equals(dataset.data)

    # No filtering when datetime_column is None
    dataset.filter_by_weekday(weekday=weekday_to_filter)
    assert df.equals(dataset.data)


def test_filter_by_week():
    # Test filtering by week
    dataset = Dataset(
        'datasets/measures2', format='txt', datetime_columns=['date', 'time']
    )
    dataset.load()

    # Filter by valid week
    week_to_filter = 37
    df = dataset.filter_by_week(
        week=week_to_filter, datetime_column='date_time')
    assert len(df) == 38
    assert all(df['date_time'].dt.isocalendar().week == week_to_filter)

    # No filtering when week is None
    dataset.filter_by_week(datetime_column='date_time')
    assert df.equals(dataset.data)

    # No filtering when datetime_column is None
    dataset.filter_by_week(week=week_to_filter)
    assert df.equals(dataset.data)


def test_filter_by_month():
    # Test filtering by month
    dataset = Dataset(
        'datasets/measures2', format='txt', datetime_columns=['date', 'time']
    )
    dataset.load()

    # Filter by valid month
    month_to_filter = 9
    df = dataset.filter_by_month(
        month=month_to_filter, datetime_column='date_time')
    assert len(df) == 38
    assert all(df['date_time'].dt.month == month_to_filter)

    # No filtering when month is None
    dataset.filter_by_month(datetime_column='date_time')
    assert df.equals(dataset.data)

    # No filtering when datetime_column is None
    dataset.filter_by_month(month=month_to_filter)
    assert df.equals(dataset.data)


def test_filter_by_year():
    # Test filtering by year
    dataset = Dataset(
        'datasets/measures2', format='txt', datetime_columns=['date', 'time']
    )
    dataset.load()

    # Filter by valid year
    year_to_filter = 2022
    df = dataset.filter_by_year(
        year=year_to_filter, datetime_column='date_time')
    assert len(df) == 38
    assert all(df['date_time'].dt.year == year_to_filter)

    # No filtering when year is None
    dataset.filter_by_year(datetime_column='date_time')
    assert df.equals(dataset.data)

    # No filtering when datetime_column is None
    dataset.filter_by_year(year=year_to_filter)
    assert df.equals(dataset.data)
