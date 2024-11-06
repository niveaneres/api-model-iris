import pytest
import numpy as np
import pickle
from lmodel.model import ModelHandler


def test_load_model(mocker):
    mock_open = mocker.patch("builtins.open", mocker.mock_open(read_data=b"binary_model_data"))
    mock_pickle_load = mocker.patch("pickle.load")
    mock_pickle_load.return_value = "mock_model"
    handler = ModelHandler("lmodel/artifacts/Iris.pkl", ["Iris-setosa", "Iris-versicolor", "Iris-virginica"])
    assert handler.model == "mock_model"
    mock_open.assert_called_once_with("lmodel/artifacts/Iris.pkl", "rb")
    mock_pickle_load.assert_called_once()


def test_get_label():
    handler = ModelHandler("lmodel/artifacts/Iris.pkl", ["Iris-setosa", "Iris-versicolor", "Iris-virginica"])
    assert handler.get_label(0) == "Iris-setosa"
    assert handler.get_label(1) == "Iris-versicolor"
    assert handler.get_label(2) == "Iris-virginica"


def test_inference(mocker):
    mock_model = mocker.Mock()
    mock_model.predict.return_value = [0]
    handler = ModelHandler("lmodel/artifacts/Iris.pkl", ["Iris-setosa", "Iris-versicolor", "Iris-virginica"])
    handler.model = mock_model
    data = {
        "SepalLengthCm": 4.6,
        "SepalWidthCm": 3.1,
        "PetalLengthCm": 1.3,
        "PetalWidthCm": 0.2
    }
    result = handler.inference(data)
    assert result == "Iris-setosa"
    mock_model.predict.assert_called_once_with(data)


def test_get_features(mocker):
    mock_model = mocker.Mock()
    mock_model.feature_names_in_ = np.array(['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm'])
    handler = ModelHandler("lmodel/artifacts/Iris.pkl")
    handler.model = mock_model
    features = handler.get_features()
    assert features == ["SepalLengthCm", "SepalWidthCm", "PetalLengthCm", "PetalWidthCm"]
