import pandas as pd


class Dataset:
    def __init__(self, filename, format='csv', target_format=None, datetime_columns=[]):
        # Validate format
        if format not in ['csv', 'txt', 'json']:
            raise ValueError(f'Invalid format: {format}')

        # Initialise attributes
        self.filename = f'{filename}.{format}'
        self.format = format
        self.target_format = target_format
        self.datetime_columns = [datetime_columns]
        self.information = {}

    def load(self):
        # Load data from file
        if self.format == 'csv' or self.format == 'txt':
            if len(self.datetime_columns[0]) == 0:
                data = pd.read_csv(self.filename)
            else:
                data = pd.read_csv(
                    self.filename, parse_dates=self.datetime_columns)
        elif self.format == 'json':
            if len(self.datetime_columns[0]) == 0:
                data = pd.read_json(self.filename, orient='records')
            else:
                data = pd.read_json(
                    self.filename, parse_dates=self.datetime_columns, orient='records')
        self.data = data

        # Analyse data
        self.identify_dataset()

    def convert(self, target_format=None, output_filename='converted_data'):
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
        # Initialisation
        information = {'columns': []}
        column_types = set()

        # Identify dataset
        for column in self.data.columns:
            if self.data[column].dtype == 'object':
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
            elif self.data[column].dtype == 'datetime64[ns]':
                information['columns'].append({
                    'column': column,
                    'type': 'time-series'
                })
                column_types.add('time-series')
            else:
                information['columns'].append({
                    'column': column,
                    'type': 'numerical',
                    'min': self.data[column].min(),
                    'max': self.data[column].max()
                })
                column_types.add('numerical')

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
        print(f'Number of attributes: {len(self.data.columns)}')
        print(f'Dataset type: {self.information["type"]}')

        for column in self.information['columns']:
            if column['type'] == 'categorical':
                print(f'{column["column"]}: {column["categories"]}')
            if column['type'] == 'numerical':
                print(
                    f'{column["column"]}: {column["min"]}-{column["max"]}')
            if column['type'] == 'text':
                print(f'{column["column"]}: long text')

    def discretise(self, method='equal_width', num_bins=10, columns=[]):
        # Validate method
        if method not in ['equal_width', 'equal_frequency']:
            raise ValueError(f'Invalid discretisation method: {method}')

        # Validate columns
        if len(columns) == 0:
            raise ValueError('Columns not specified')

        # Validate column type
        for column in columns:
            for column_info in self.information['columns']:
                if column_info['column'] == column and column_info['type'] != 'numerical':
                    raise ValueError(f'Column {column} is not numerical')

        # Discretise data
        for column in columns:
            if method == 'equal_width':
                self.data[column] = pd.cut(
                    self.data[column], bins=num_bins, labels=None)
            elif method == 'equal_frequency':
                self.data[column] = pd.qcut(
                    self.data[column], q=num_bins, labels=None)

    def filter_between_dates(self, start_date=None, end_date=None, datetime_column=None):
        if start_date is not None and end_date is not None:
            if start_date > end_date:
                raise ValueError(
                    f'start_date ({start_date}) is greater than end_date ({end_date})')

            if datetime_column is not None:
                # Sort dataset based on time-series
                df = self.data.sort_values(by=datetime_column)

                # Filter dataset based on start date and end date
                return df[(self.data[datetime_column] >= start_date) & (self.data[datetime_column] <= end_date)]

    def filter_by_minute(self, minute=None, datetime_column=None):
        if minute is not None:
            if datetime_column is not None:
                # Sort dataset based on time-series
                df = self.data.sort_values(by=datetime_column)

                # Filter dataset based on minute
                return df[df[datetime_column].dt.minute == minute]

    def filter_by_hour(self, hour=None, datetime_column=None):
        if hour is not None:
            if datetime_column is not None:
                # Sort dataset based on time-series
                df = self.data.sort_values(by=datetime_column)

                # Filter dataset based on hour
                return df[df[datetime_column].dt.hour == hour]

    def filter_by_day(self, day=None, datetime_column=None):
        if day is not None:
            if datetime_column is not None:
                # Sort dataset based on time-series
                df = self.data.sort_values(by=datetime_column)

                # Filter dataset based on day
                return df[df[datetime_column].dt.day == day]

    def filter_by_weekday(self, weekday=None, datetime_column=None):
        if weekday is not None:
            if datetime_column is not None:
                # Sort dataset based on time-series
                df = self.data.sort_values(by=datetime_column)

                # Filter dataset based on weekday
                return df[df[datetime_column].dt.weekday == weekday]

    def filter_by_week(self, week=None, datetime_column=None):
        if week is not None:
            if datetime_column is not None:
                # Sort dataset based on time-series
                df = self.data.sort_values(by=datetime_column)

                # Filter dataset based on week
                return df[df[datetime_column].dt.isocalendar().week == week]

    def filter_by_month(self, month=None, datetime_column=None):
        if month is not None:
            if datetime_column is not None:
                # Sort dataset based on time-series
                df = self.data.sort_values(by=datetime_column)

                # Filter dataset based on month
                return df[df[datetime_column].dt.month == month]

    def filter_by_year(self, year=None, datetime_column=None):
        if year is not None:
            if datetime_column is not None:
                # Sort dataset based on time-series
                df = self.data.sort_values(by=datetime_column)

                # Filter dataset based on year
                return df[df[datetime_column].dt.year == year]
