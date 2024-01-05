import pandas as pd
from arm_preprocessing.discretisation import Discretisation


class Dataset:
    """
    Represents a dataset with various functionalities for data manipulation and analysis.

    Args:
        filename (str): Name of the file without extension.
        format (str, optional): Format of the dataset file ('csv', 'txt', 'json'). Default is 'csv'.
        target_format (str, optional): Target format for conversion. Default is None.
        datetime_columns (list, optional): List of columns containing datetime values. Default is an empty list.

    Attributes:
        filename (str): Name of the file without extension.
        format (str): Format of the dataset file ('csv', 'txt', 'json').
        target_format (str): Target format for conversion.
        datetime_columns (list): List of columns containing datetime values.
        information (dict): Information about the dataset.
        data (pd.DataFrame): Dataset.
    """

    def __init__(self, filename, format="csv", target_format=None, datetime_columns=[]):
        """
        Initialise a Dataset instance.

        Args:
            filename (str): Name of the file without extension.
            format (str, optional): Format of the dataset file ('csv', 'txt', 'json'). Default is 'csv'.
            target_format (str, optional): Target format for conversion. Default is None.
            datetime_columns (list, optional): List of columns containing datetime values. Default is an empty list.
        """
        # Validate format
        if format not in ["csv", "txt", "json"]:
            raise ValueError(f"Invalid format: {format}")

        # Initialise attributes
        self.filename = f"{filename}.{format}"
        self.format = format
        self.target_format = target_format
        self.datetime_columns = [datetime_columns]
        self.information = {}

    def load(self):
        """
        Load data from the specified file and analyse it.

        Raises:
            ValueError: Specified format is not supported.

        Returns:
            None
        """
        # Load data from file
        if self.format == "csv" or self.format == "txt":
            if len(self.datetime_columns[0]) == 0:
                data = pd.read_csv(self.filename)
            else:
                data = pd.read_csv(self.filename, parse_dates=self.datetime_columns)
        elif self.format == "json":
            if len(self.datetime_columns[0]) == 0:
                data = pd.read_json(self.filename, orient="records")
            else:
                data = pd.read_json(
                    self.filename, parse_dates=self.datetime_columns, orient="records"
                )
        self.data = data

        # Analyse data
        self.identify_dataset()

    def convert(self, target_format=None, output_filename="converted_data"):
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
            raise ValueError("Target format not specified")

        # Prepare output filepath
        output_filepath = f"{output_filename}.{target_format}"

        # Convert data
        if target_format == "csv":
            self.data.to_csv(output_filepath, index=False)
        elif target_format == "json":
            self.data.to_json(output_filepath, orient="records")

    def identify_dataset(self):
        """
        Identify the type of the dataset and store the information.

        Raises:
            ValueError: Dataset contains invalid column type.

        Returns:
            None
        """
        # Initialisation
        information = {"columns": []}
        column_types = set()

        # Identify dataset
        for column in self.data.columns:
            if self.data[column].dtype == "object":
                unique_values = self.data[column].unique()
                max_str_length = max(len(str(value)) for value in unique_values)
                column_info = {
                    "column": column,
                    "type": "categorical" if max_str_length < 25 else "text",
                }
                if max_str_length < 25:
                    column_info["categories"] = unique_values.tolist()
                information["columns"].append(column_info)
                column_types.add("categorical" if max_str_length < 25 else "text")
            elif self.data[column].dtype == "datetime64[ns]":
                information["columns"].append({"column": column, "type": "time-series"})
                column_types.add("time-series")
            else:
                information["columns"].append(
                    {
                        "column": column,
                        "type": "numerical",
                        "min": self.data[column].min(),
                        "max": self.data[column].max(),
                    }
                )
                column_types.add("numerical")

        # Determine the general type of the dataset
        if "time-series" in column_types:
            information["type"] = "time-series"
        elif "numerical" in column_types and len(column_types) == 1:
            information["type"] = "numerical"
        elif "categorical" in column_types and len(column_types) == 1:
            information["type"] = "categorical"
        elif "text" in column_types and len(column_types) == 1:
            information["type"] = "text"
        else:
            information["type"] = "mixed"

        # Store information
        self.information = information

    def dataset_statistics(self):
        """
        Print dataset statistics.

        Returns:
            None
        """
        print(f"Number of attributes: {len(self.data.columns)}")
        print(f'Dataset type: {self.information["type"]}')

        for column in self.information["columns"]:
            if column["type"] == "categorical":
                print(f'{column["column"]}: {column["categories"]}')
            if column["type"] == "numerical":
                print(f'{column["column"]}: {column["min"]}-{column["max"]}')
            if column["type"] == "text":
                print(f'{column["column"]}: long text')

    def discretise(self, method, num_bins, columns):
        """
        Discretise the dataset using the specified method.

        Args:
            data (pd.DataFrame): Dataset.
            method (str): Discretisation method ('equal_width', 'equal_frequency', 'kmeans').
            num_bins (int): Number of bins.
            columns (list): List of columns to discretise.
        """
        Discretisation.discretise(
            data=self.data,
            method=method,
            num_bins=num_bins,
            columns=columns,
            information=self.information,
        )

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
                    f"Start date ({start_date}) is greater than end date ({end_date})"
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
