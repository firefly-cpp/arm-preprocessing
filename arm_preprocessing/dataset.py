import pandas as pd
from pandas.api.types import (
    is_bool_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
    is_string_dtype,
)
from sport_activities_features.tcx_manipulation import TCXFile
from arm_preprocessing.discretisation import Discretisation
from arm_preprocessing.squashing import Squash


class Dataset:
    """
    Represents a dataset with various functionalities for data manipulation and analysis.

    Args:
        filename (str): Name of the file without extension.
        format (str, optional): Format of the dataset file ('csv', 'txt', 'json', 'tcx'). Default is 'csv'.
        target_format (str, optional): Target format for conversion. Default is None.
        datetime_columns (list, optional): List of columns containing datetime values. Default is an empty list.

    Attributes:
        filename (str): Name of the file without extension.
        format (str): Format of the dataset file ('csv', 'txt', 'json', 'tcx').
        target_format (str): Target format for conversion.
        datetime_columns (list): List of columns containing datetime values.
        information (dict): Information about the dataset.
        data (pd.DataFrame): Dataset.
    """

    def __init__(
        self, filename=None, format='csv', target_format=None, datetime_columns=None
    ):
        """
        Initialise a Dataset instance.

        Args:
            filename (str): Name of the file without extension.
            format (str, optional): Format of the dataset file ('csv', 'txt', 'json', 'tcx'). Default is 'csv'.
            target_format (str, optional): Target format for conversion. Default is None.
            datetime_columns (list, optional): List of columns containing datetime values. Default is an empty list.
        """
        # Validate format
        if format not in ['csv', 'txt', 'json', 'tcx']:
            raise ValueError(f'Invalid format: {format}')

        # Initialise attributes
        self.filename = filename
        self.format = format
        self.target_format = target_format
        self.datetime_columns = datetime_columns or []
        self.information = {}

    def _is_categorical_like(self, series):
        return (
            is_string_dtype(series)
            or is_object_dtype(series)
            or isinstance(series.dtype, pd.CategoricalDtype)
            or is_bool_dtype(series)
        )

    def _normalise_dtypes(self, data):
        """
        Normalize dtypes for compatibility with the project's pandas 2 API.

        Returns:
            pd.DataFrame
        """
        for column in data.columns:
            series = data[column]
            if is_string_dtype(series):
                data[column] = series.astype(object)
            elif is_datetime64_any_dtype(series):
                data[column] = series.astype('datetime64[ns]')

        return data

    def _apply_datetime_columns(self, data):
        """
        Parse configured datetime columns after loading.

        Returns:
            pd.DataFrame
        """
        if not self.datetime_columns:
            return data

        if len(self.datetime_columns) == 1:
            column = self.datetime_columns[0]
            data[column] = pd.to_datetime(data[column]).astype('datetime64[ns]')
            return data

        combined_column = '_'.join(self.datetime_columns)
        data[combined_column] = pd.to_datetime(
            data[self.datetime_columns].astype(str).agg(' '.join, axis=1)
        ).astype('datetime64[ns]')
        return data

    def load(self):
        """
        Load data from the specified file and analyse it.

        Raises:
            ValueError: Specified format is not supported.

        Returns:
            None
        """
        # Load data from file
        filename = f'{self.filename}.{self.format}'
        if self.format == 'csv' or self.format == 'txt':
            data = pd.read_csv(filename)
        elif self.format == 'json':
            data = pd.read_json(filename, orient='records')
        elif self.format == 'tcx':
            tcx_file = TCXFile()
            all_files = tcx_file.read_directory(self.filename)
            data = pd.DataFrame(
                [tcx_file.extract_integral_metrics(file) for file in all_files])
        data = self._apply_datetime_columns(data)
        data = self._normalise_dtypes(data)
        self.data = data

        # Analyse data
        self.identify_dataset()

    def convert(self, target_format=None, output_filename='converted_data'):
        """
        Convert the dataset to the specified target format.

        Args:
            target_format (str): Target format for conversion.
            output_filename (str): Name of the output file without extension.

        Raises:
            ValueError: Target format is not specified.

        Returns:
            None
        """
        # Validate target format
        if target_format is None:
            raise ValueError('Target format not specified')

        # Prepare output filepath
        output_filepath = f'{output_filename}.{target_format}'

        # Convert data
        if target_format == 'csv':
            self.data.to_csv(output_filepath, index=False)
        elif target_format == 'json':
            self.data.to_json(output_filepath, orient='records')

    def identify_dataset(self):
        """
        Identify the type of the dataset and store the information.

        Raises:
            ValueError: Dataset contains invalid column type.

        Returns:
            None
        """
        # Initialisation
        information = {'columns': []}
        column_types = set()

        # Identify dataset
        for column in self.data.columns:
            series = self.data[column]
            if self._is_categorical_like(series):
                unique_values = self.data[column].unique()
                max_str_length = max(len(str(value))
                                     for value in unique_values)
                column_info = {
                    'column': column,
                    'type': 'categorical' if max_str_length < 25 else 'text',
                }
                if max_str_length < 25:
                    column_info['categories'] = unique_values.tolist()
                information['columns'].append(column_info)
                column_types.add(
                    'categorical' if max_str_length < 25 else 'text')
            elif is_datetime64_any_dtype(series):
                information['columns'].append(
                    {'column': column, 'type': 'time-series'})
                column_types.add('time-series')
            elif is_numeric_dtype(series):
                information['columns'].append(
                    {
                        'column': column,
                        'type': 'numerical',
                        'min': series.min(),
                        'max': series.max(),
                    }
                )
                column_types.add('numerical')
            else:
                raise ValueError(f'Invalid column type: {series.dtype}')

        # Determine the general type of the dataset
        if 'time-series' in column_types:
            information['type'] = 'time-series'
        elif 'numerical' in column_types and len(column_types) == 1:
            information['type'] = 'numerical'
        elif 'categorical' in column_types and len(column_types) == 1:
            information['type'] = 'categorical'
        elif 'text' in column_types and len(column_types) == 1:
            information['type'] = 'text'
        else:
            information['type'] = 'mixed'

        # Store information
        self.information = information

    def dataset_statistics(self):
        """
        Print dataset statistics.

        Returns:
            None
        """
        print(f'Number of attributes: {len(self.data.columns)}')
        print(f'Dataset type: {self.information["type"]}')

        for column in self.information['columns']:
            if column['type'] == 'categorical':
                print(f'{column["column"]}: {column["categories"]}')
            if column['type'] == 'numerical':
                print(f'{column["column"]}: {column["min"]}-{column["max"]}')
            if column['type'] == 'text':
                print(f'{column["column"]}: long text')

    def missing_values(self, method):
        """
        Handle missing values using the specified method.

        Args:
            method (str): Method for handling missing values ('row', 'column', 'impute').

        Raises:
            ValueError: Invalid method.

        Returns:
            None
        """
        # Validate method
        if method not in ['row', 'column', 'impute']:
            raise ValueError(f'Invalid method: {method}')

        # Handle missing values
        if method == 'column':
            self.data.dropna(axis=1, inplace=True)
        elif method == 'row':
            self.data.dropna(axis=0, inplace=True)
        elif method == 'impute':
            for column in self.data.columns:
                series = self.data[column]
                if is_numeric_dtype(series):
                    self.data[column] = series.fillna(series.mean())
                elif self._is_categorical_like(series) or is_datetime64_any_dtype(series):
                    mode = series.mode(dropna=True)
                    fill_value = mode.iloc[0] if not mode.empty else None
                    self.data[column] = series.fillna(fill_value)
                else:
                    raise ValueError(f'Invalid column type: {series.dtype}')

    def discretise(self, method, num_bins, columns):
        """
        Discretise the dataset using the specified method.

        Args:
            data (pd.DataFrame): Dataset.
            method (str): Discretisation method ('equal_width', 'equal_frequency', 'kmeans').
            num_bins (int): Number of bins.
            columns (list): List of columns to discretise.

        Raises:
            ValueError: Invalid data type.
            ValueError: Invalid discretisation method.
            ValueError: Columns not specified.
            ValueError: Column type is not numerical.

        Returns:
            None
        """
        Discretisation.discretise(
            data=self.data,
            method=method,
            num_bins=num_bins,
            columns=columns,
            information=self.information,
        )

    def squash(self, threshold, similarity='euclidean'):
        """
        Squash the dataset using the specified threshold and similarity.

        Args:
            threshold (float): Threshold.
            similarity (str): Similarity measure ('euclidean', 'cosine').

        Raises:
            ValueError: Invalid similarity measure.

        Returns:
            None
        """
        # Validate similarity
        if similarity not in ['euclidean', 'cosine']:
            raise ValueError(f'Invalid similarity measure: {similarity}')

        # Squash data
        self.data = Squash.squash(self.data, threshold, similarity)

    def scale(self, method):
        """
        Scale the dataset using the specified method.

        Args:
            method (str): Scaling method ('normalisation', 'standardisation').

        Raises:
            ValueError: Invalid scaling method.
        """
        # Validate method
        if method not in ['normalisation', 'standardisation']:
            raise ValueError(f'Invalid scaling method: {method}')

        # Scale data
        for column in self.data.columns:
            series = self.data[column]
            if not is_numeric_dtype(series):
                continue

            if method == 'normalisation':
                minimum = series.min()
                maximum = series.max()
                if minimum == maximum:
                    self.data[column] = 0.0
                else:
                    self.data[column] = (series - minimum) / (maximum - minimum)
            elif method == 'standardisation':
                std = series.std()
                if std == 0:
                    self.data[column] = 0.0
                else:
                    self.data[column] = (series - series.mean()) / std

    def feature_selection(self, method, threshold, class_column):
        """
        Select features based on the specified threshold.

        Args:
            method (str): Feature selection method ('pearson', 'spearman', 'kendall').
            threshold (float): Threshold.
            class_column (str): Name of the column containing class labels.

        Raises:
            ValueError: Invalid feature selection method.
            ValueError: Column is not numerical.

        Returns:
            None
        """
        # Validate method
        if method not in ['pearson', 'spearman', 'kendall']:
            raise ValueError(f'Invalid feature selection method: {method}')

        # Raise ValueError if column in self.data is not numerical
        for column in self.data.columns:
            if self.data[column].dtype not in ['int64', 'float64']:
                raise ValueError(f'Column {column} is not numerical')

        # Calculate feature importance
        feature_importance = self.data.corr(method=method)[class_column]

        # Select features
        self.data = self.data[feature_importance[feature_importance >= threshold].index]

    def filter_between_dates(
        self, start_date=None, end_date=None, datetime_column=None
    ):
        """
        Filter the dataset based on the specified start date and end date.

        Args:
            start_date (str): Start date.
            end_date (str): End date.
            datetime_column (str): Name of the column containing datetime values.

        Raises:
            ValueError: Start date is greater than end date.

        Returns:
            None
        """
        if start_date is not None and end_date is not None:
            if start_date > end_date:
                raise ValueError(
                    f'Start date ({start_date}) is greater than end date ({end_date})'
                )

            if datetime_column is not None:
                # Sort dataset based on time-series
                df = self.data.sort_values(by=datetime_column)

                # Filter dataset based on start date and end date
                return df[
                    (self.data[datetime_column] >= start_date)
                    & (self.data[datetime_column] <= end_date)
                ]

        return self.data

    def filter_by_minute(self, minute=None, datetime_column=None):
        """
        Filter the dataset based on the specified minute.

        Args:
            minute (int): Minute.
            datetime_column (str): Name of the column containing datetime values.

        Returns:
            None
        """
        if minute is not None:
            if datetime_column is not None:
                # Sort dataset based on time-series
                df = self.data.sort_values(by=datetime_column)

                # Filter dataset based on minute
                return df[df[datetime_column].dt.minute == minute]

        return self.data

    def filter_by_hour(self, hour=None, datetime_column=None):
        """
        Filter the dataset based on the specified hour.

        Args:
            hour (int): Hour.
            datetime_column (str): Name of the column containing datetime values.

        Returns:
            None
        """
        if hour is not None:
            if datetime_column is not None:
                # Sort dataset based on time-series
                df = self.data.sort_values(by=datetime_column)

                # Filter dataset based on hour
                return df[df[datetime_column].dt.hour == hour]

        return self.data

    def filter_by_day(self, day=None, datetime_column=None):
        """
        Filter the dataset based on the specified day.

        Args:
            day (int): Day.
            datetime_column (str): Name of the column containing datetime values.

        Returns:
            None
        """
        if day is not None:
            if datetime_column is not None:
                # Sort dataset based on time-series
                df = self.data.sort_values(by=datetime_column)

                # Filter dataset based on day
                return df[df[datetime_column].dt.day == day]

        return self.data

    def filter_by_weekday(self, weekday=None, datetime_column=None):
        """
        Filter the dataset based on the specified weekday.

        Args:
            weekday (int): Weekday.
            datetime_column (str): Name of the column containing datetime values.

        Returns:
            None
        """
        if weekday is not None:
            if datetime_column is not None:
                # Sort dataset based on time-series
                df = self.data.sort_values(by=datetime_column)

                # Filter dataset based on weekday
                return df[df[datetime_column].dt.weekday == weekday]

        return self.data

    def filter_by_week(self, week=None, datetime_column=None):
        """
        Filter the dataset based on the specified week.

        Args:
            week (int): Week.
            datetime_column (str): Name of the column containing datetime values.

        Returns:
            None
        """
        if week is not None:
            if datetime_column is not None:
                # Sort dataset based on time-series
                df = self.data.sort_values(by=datetime_column)

                # Filter dataset based on week
                return df[df[datetime_column].dt.isocalendar().week == week]

        return self.data

    def filter_by_month(self, month=None, datetime_column=None):
        """
        Filter the dataset based on the specified month.

        Args:
            month (int): Month.
            datetime_column (str): Name of the column containing datetime values.

        Returns:
            None
        """
        if month is not None:
            if datetime_column is not None:
                # Sort dataset based on time-series
                df = self.data.sort_values(by=datetime_column)

                # Filter dataset based on month
                return df[df[datetime_column].dt.month == month]

        return self.data

    def filter_by_year(self, year=None, datetime_column=None):
        """
        Filter the dataset based on the specified year.

        Args:
            year (int): Year.
            datetime_column (str): Name of the column containing datetime values.

        Returns:
            None
        """
        if year is not None:
            if datetime_column is not None:
                # Sort dataset based on time-series
                df = self.data.sort_values(by=datetime_column)

                # Filter dataset based on year
                return df[df[datetime_column].dt.year == year]

        return self.data
