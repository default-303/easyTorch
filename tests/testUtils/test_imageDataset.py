import os
import pytest
import torch
from utils.imageDataset import CustomDataset
import pandas as pd
from tests.pytest_helpers.nn import simple_augmentation
from typing import Callable

# noinspection PyUnresolvedReferences
from tests.pytest_helpers.data import image


@pytest.fixture()
def dataframe() -> Callable:
    def get_dataframe(rel_path: str) -> pd.DataFrame:
        filepath = os.path.join(os.path.dirname(__file__), rel_path)
        df = pd.read_csv(filepath)
        return df

    return get_dataframe


def test_random_on_error_and_exit_on_error_same_value(dataframe):
    df = dataframe('../sampleData/paths.csv')
    with pytest.raises(ValueError):
        CustomDataset(df, exit_on_error=True, random_on_error=True)


def test_dataframe_size(dataframe):
    # invalid dataframe check
    df_invalid_dataset_size = pd.DataFrame(
        {
            'path': [1, 2],
            'label': [2, 3],
            'xyz': [4, 5]
        }
    )

    with pytest.raises(ValueError):
        CustomDataset(df_invalid_dataset_size)

    # valid dataframe check
    valid_df = dataframe('../sampleData/paths.csv')
    try:
        CustomDataset(valid_df)
    except Exception:
        assert False


def test_invalid_column_dtypes(dataframe):
    df_invalid_label_dtype = dataframe('../sampleData/paths.csv')
    df_invalid_label_dtype['label'] = df_invalid_label_dtype['label'].astype(str)
    with pytest.raises(ValueError):
        CustomDataset(df_invalid_label_dtype)

    df_invalid_path_dtype = pd.DataFrame(
        {
            'path': [1, 2],
            'label': [2, 3]
        }
    )

    with pytest.raises(ValueError):
        CustomDataset(df_invalid_path_dtype)


def test_exit_on_error_raises_exception(dataframe):
    df = dataframe('../sampleData/invalidset.csv')
    cd = CustomDataset(df, exit_on_error=True, random_on_error=False)
    with pytest.raises(Exception):
        for _, _ in cd:
            pass


def test_datataset_len(dataframe):
    df = dataframe('../sampleData/paths.csv')
    cd = CustomDataset(df)
    assert len(cd) == df.shape[0]


@pytest.mark.parametrize('augmentations', [None, simple_augmentation])
def test_dataset_getitem(augmentations):
    filepath = os.path.join(os.path.dirname(__file__), '../sampleData/paths.csv')
    paths_df = pd.read_csv(filepath)
    cd = CustomDataset(paths_df, augmentations)
    image, target = next(iter(cd))
    assert isinstance(image, torch.Tensor)
    assert isinstance(target, torch.Tensor)
    assert image.dtype == torch.float
    assert target.dtype == torch.long

    if augmentations is not None:
        assert list(image.size()) == [3, 40, 40]


def test_read_grayscale_img_and_convert():
    df = pd.DataFrame(
        {
            'path': [os.path.join(os.path.dirname(__file__), '../sampleData/images/mau.jpg')],
            'label': 0
        }
    )
    cd = CustomDataset(df)
    img, _ = next(iter(cd))
    assert img.ndim == 3
