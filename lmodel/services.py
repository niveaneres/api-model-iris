import json
import pandas as pd


def run_inferece(parsed_data, model):
    df = pd.DataFrame(parsed_data, index=[0])
    prediction = model.inference(df)
    return prediction


def validate_features(data, reference_features):
    features_name = data.keys()
    return set(features_name) == set(reference_features)


def validate_and_parse_input(data):
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            return {"error": "Input must be a valid JSON"}, None
    return None, data


def validate_input(data, reference_features, expected_length=4):
    if not isinstance(data, dict):
        return {"error": "Input must be a valid JSON"}
    
    if not validate_features(data, reference_features):
        return {"error": f"The JSON must contain {expected_length} items."}

    if not all(isinstance(value, (float, int)) for value in data.values()):
        return {"error": "All values in the JSON must be numbers (float or int)."}
    return None



    
        
    
    