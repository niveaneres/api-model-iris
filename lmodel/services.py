import json
import pandas as pd


def run_inference(parsed_data, model):
    """
    Realiza a inferência usando o modelo e as dados especificados 
    """
    df = pd.DataFrame(parsed_data, index=[0])
    prediction = model.inference(df)
    return prediction


def validate_features(data, reference_features):
    """
    Valida se os nomes das features fornecidos correspondem ao modelo.
    """
    features_name = data.keys()
    return set(features_name) == set(reference_features)


def validate_and_parse_input(data):
    """
    Valida se o JSON fornecido é valido.
    """
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            return {"error": "Input must be a valid JSON"}, None
    return None, data


def validate_input(data, reference_features, expected_length=4):
    """
    Valida se o JSON está de acordo com o esperado.
    """
    if not isinstance(data, dict):
        return {"error": "Input must be a valid JSON"}

    if not validate_features(data, reference_features):
        return {
            "error": "The feature names should match those that were passed during fit."
        }

    if not all(isinstance(value, (float, int)) for value in data.values()):
        return {"error": "All values in the JSON must be numbers (float or int)."}
    return None
