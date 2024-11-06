import pickle
import logging

logger = logging.getLogger(__name__)


class ModelHandler:
    """
    Classe usada para manipular modelos de machine learning.
    """
    def __init__(self, model_path, class_names=None):
        self.model_path = model_path
        self.class_names = class_names
        self.model = self.load_model()

    def load_model(self):
        """
        Carrega o modelo a partir do caminho especificado em model_path.
        """
        try:
            with open(self.model_path, "rb") as file:
                return pickle.load(file)
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise

    def get_label(self, prediction):
        """
        Recupera o nome da classe correspondente a previsão.
        """
        return self.class_names[prediction]

    def inference(self, data):
        """
        Realiza a inferência nos dados fornecidos e retorna a previsão.
        """
        prediction = self.model.predict(data)
        if self.class_names:
            return self.get_label(prediction[0])
        return str(prediction[0])

    def get_features(self):
        """
        Recupera a lista de features usadas ao treinar o modelo.
        """
        features = self.model.feature_names_in_
        return features.tolist()
