import re
import pytest

from arm_preprocessing import __version__
from arm_preprocessing.dataset import Dataset


def test_discretise_equal_width():
    # Test equal width discretisation
    dataset = Dataset("datasets/sportydatagen", format="csv")
    dataset.load()
    dataset.discretise(method="equal_width", num_bins=5, columns=["calories"])
    assert dataset.data["calories"].value_counts().shape[0] == 5
    assert dataset.data["calories"].dtype == "category"


def test_discretise_equal_frequency():
    # Test equal width discretisation
    dataset = Dataset("datasets/measures2", format="txt")
    dataset.load()
    dataset.discretise(method="equal_frequency", num_bins=5, columns=["temperature"])
    assert dataset.data["temperature"].value_counts().shape[0] == 5
    assert dataset.data["temperature"].dtype == "category"


def test_discretise_kmeans():
    # Test k-means discretisation
    dataset = Dataset("datasets/measures2", format="txt")
    dataset.load()
    dataset.discretise(method="kmeans", num_bins=5, columns=["temperature"])
    assert dataset.data["temperature"].value_counts().shape[0] == 5
    assert all(dataset.data["temperature"].str.match(re.compile(r"^Cluster \d+$")))


def test_discretise_invalid_method():
    # Test invalid discretisation method
    dataset = Dataset("datasets/measures2", format="txt")
    dataset.load()
    with pytest.raises(ValueError, match="Invalid discretisation method"):
        dataset.discretise(method="invalid_method", num_bins=5, columns=["temperature"])
