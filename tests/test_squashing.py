from arm_preprocessing.dataset import Dataset


def test_squash_cosine():
    # Test squashing using cosine similarity
    dataset = Dataset('datasets/Abalone', format='csv')
    dataset.load()
    dataset.data.drop('Sex', axis=1, inplace=True)
    original_size = len(dataset.data)
    dataset.squash(threshold=0.99, similarity='cosine')
    assert len(dataset.data) < original_size


def test_squash_euclidean():
    # Test squashing using euclidean similarity
    dataset = Dataset('datasets/breast', format='csv')
    dataset.load()
    original_size = len(dataset.data)
    dataset.squash(threshold=0.75, similarity='euclidean')
    assert len(dataset.data) < original_size
