# app.py
from datetime import datetime as dt
from flask import Flask, request, jsonify
from lmodel.services import (
    run_inference,
    validate_and_parse_input,
    validate_input)
from lmodel.model import ModelHandler
import logging
import pytz

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__)

model_path = "lmodel/artifacts/Iris.pkl"
class_names = ["Iris-setosa", "Iris-versicolor", "Iris-virginica"]
model = ModelHandler(model_path, class_names)


@app.route("/status", methods=["GET"])
def healthcheck():
    tz = pytz.timezone('America/Sao_Paulo') 
    current_time = dt.now(tz)
    return {"status": "alive!", "dt": str(current_time)}


@app.route("/inference/", methods=["POST"])
def inference():
    data = request.get_json()

    if not isinstance(data, list):
        data = [data]

    predictions = []
    for item in data:
        logger.info("validating entry")
        validation_error, parsed_data = validate_and_parse_input(item)
        if validation_error:
            logger.info(validation_error)
            return validation_error, 400

        features = model.get_features()
        validation_result = validate_input(parsed_data, features)
        if validation_result:
            logger.info(validation_result)
            return validation_result, 400

        logger.info("inferring")
        prediction = run_inference(parsed_data, model)
        predictions.append(prediction)
    
    predictions = predictions[0] if len(predictions) == 1 else predictions
    logger.info("done!")
    return jsonify({"category": predictions}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
