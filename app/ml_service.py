import joblib
from datetime import datetime
import pandas as pd
from get_data import get_current_features1
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MLService:
    def __init__(self):
        try:
            self.model = joblib.load('catboost_lr 0.38121, mae 0.1857300913901133 , mape 0.009344126631801567, rmse 0.10354896606489733.joblib')
            self.last_prediction = None
            self.last_prediction_time = None
            logger.info("ML model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load ML model: {e}")
            raise

    def get_prediction(self):
        try:
            logger.info("Fetching features for prediction...")
            features = get_current_features1()
            
            if features is None:
                logger.error("Failed to get features: get_current_features1 returned None")
                return None, None
                
            if features.empty:
                logger.error("Failed to get features: empty DataFrame")
                return None, None
                
            # Проверяем наличие NaN значений
            nan_cols = features.isna().sum()
            if nan_cols.any():
                logger.warning(f"Features contain NaN values in columns: {nan_cols[nan_cols > 0].index.tolist()}")
            
            logger.info(f"Features shape: {features.shape}")
            logger.info("Making prediction...")
            
            prediction = self.model.predict(features)[0]
            self.last_prediction = prediction
            self.last_prediction_time = datetime.utcnow()
            logger.info(f"Prediction successful: {prediction}")
            return prediction, self.last_prediction_time
        except Exception as e:
            logger.error(f"Error in prediction: {str(e)}")
            logger.error(f"Error type: {type(e).__name__}")
            return None, None

ml_service = MLService() 

prediction_history = []