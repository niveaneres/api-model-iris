import pickle
import logging

logger = logging.getLogger(__name__)

class ModelHandler:
    def __init__(self, model_path, class_names=None):
        self.model_path = model_path
        self.class_names = class_names
        self.model = self.load_model()
        
    def load_model(self):
        try:
            with open(self.model_path, "rb") as file:
                return pickle.load(file)
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise

    def get_label(self, prediction):
        return self.class_names[prediction]

    def inference(self, data):
        prediction = self.model.predict(data)
        if self.class_names:
            return self.get_label(prediction[0])
        return str(prediction[0])
    
    def get_features(self):
        features = self.model.feature_names_in_
        return features.tolist()
    