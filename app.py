# app.py
from datetime import datetime as dt
from flask import Flask, request, jsonify
from lmodel.services import run_inferece, validate_and_parse_input, validate_input
from lmodel.model import ModelHandler
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__)

model_path = "lmodel/artifacts/Iris.pkl"
class_names = ["Iris-setosa", "Iris-versicolor", "Iris-virginica"]
model = ModelHandler(model_path, class_names)


@app.route('/status', methods=['GET'])
def healthcheck():
    return {"status": "alive!", "dt": str(dt.now())}


@app.route('/inference/', methods=['POST'])
def inference():
    data = request.get_json()
    
    logger.info("validating entry")
    validation_error, data = validate_and_parse_input(data)
    if validation_error:
        logger.info(validation_error)
        return validation_error, 400
    
    features = model.get_features()
    validation_result = validate_input(data, features)
    if validation_result:
        logger.info(validation_result)
        return validation_result, 400
    
    logger.info("inferring")
    prediction = run_inferece(data, model)

    logger.info("done!")
    return jsonify({"category": prediction}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
