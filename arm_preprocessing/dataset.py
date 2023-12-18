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

    def load_data(self):
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
        return data

    def convert_data(self, data, target_format=None, output_filename='converted_data'):
        # Validate target format
        if target_format is None:
            raise ValueError('Target format not specified')

        # Prepare output filepath
        output_filepath = f'{output_filename}.{target_format}'

        # Convert data
        if target_format == 'csv':
            data.to_csv(output_filepath, index=False)
        elif target_format == 'json':
            data.to_json(output_filepath, orient='records')
