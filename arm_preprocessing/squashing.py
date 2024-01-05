from niaarm import Dataset, squash


class Squash:
    """
    Squash class.
    """

    def squash(dataset, threshold, similarity):
        """
        Squash the dataset using the specified threshold and similarity.

        Args:
            dataset (pd.DataFrame): Dataset to squash.
            threshold (float): Similarity threshold. Should be between 0 and 1.
            similarity (str): Similarity measure ('euclidean', 'cosine').

        Returns:
            pd.DataFrame: Squashed dataset.
        """
        # Squash data
        squashed = squash(Dataset(dataset), threshold, similarity)
        return squashed.transactions
