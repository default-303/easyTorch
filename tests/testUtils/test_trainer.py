import os.path

from sklearn import metrics
from torch import nn, optim
# noinspection PyUnresolvedReferences
from tests.pytest_helpers.data import dataloaders, image
# noinspection PyUnresolvedReferences
from tests.pytest_helpers.nn import sample_model


def test_fit(sample_model, dataloaders):
    try:
        model = sample_model(
            nn.CrossEntropyLoss,
            optim.Adam,
            [(metrics.accuracy_score, {})]
        )
        model.fit(dataloaders)
    except:
        assert False


def test_prediction(sample_model, image):
    _image = image('../sampleData/images/cat1.jpeg')
    model = sample_model(nn.CrossEntropyLoss, optim.Adam, [(metrics.recall_score, {'average': 'macro'})])
    predictions = model.predict(_image)
    assert list(predictions.size()) == [1, 2]


def test_save(sample_model, dataloaders):
    model = sample_model(
        nn.CrossEntropyLoss,
        optim.Adam,
        [(metrics.accuracy_score, {})]
    )

    model.fit(dataloaders)
    assert os.path.exists('./bestModel.pkl.tar')