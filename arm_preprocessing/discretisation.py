import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


class Discretisation:
    """
    Discretisation class.
    """

    def discretise(
        data, method="equal_width", num_bins=10, columns=[], information=None
    ):
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
            pd.DataFrame: Discretised dataset.
        """
        # Validate data
        if not isinstance(data, pd.DataFrame):
            raise ValueError('Invalid data type')

        # Validate method
        if method not in ['equal_width', 'equal_frequency', 'kmeans']:
            raise ValueError(f'Invalid discretisation method: {method}')

        # Validate columns
        if len(columns) == 0:
            raise ValueError('Columns not specified')

        # Validate column type
        for column in columns:
            for column_info in information['columns']:
                if (
                    column_info['column'] == column
                    and column_info['type'] != 'numerical'
                ):
                    raise ValueError(f'Column {column} is not numerical')

        # Discretise data
        for column in columns:
            if method == 'equal_width':
                data[column] = pd.cut(data[column], bins=num_bins, labels=None)
            elif method == 'equal_frequency':
                data[column] = pd.qcut(data[column], q=num_bins, labels=None)
            elif method == 'kmeans':
                # Standardise data
                scaler = StandardScaler()
                data[column] = scaler.fit_transform(
                    data[column].values.reshape(-1, 1))

                # Perform k-means clustering
                kmeans = KMeans(n_clusters=num_bins, n_init='auto')
                kmeans.fit(data[column].values.reshape(-1, 1))

                # Assign cluster labels
                labels = [f'Cluster {label}' for label in kmeans.labels_]
                data[column] = labels

        return data
