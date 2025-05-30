import joblib
import numpy as np
from models.prediction import Prediction
from config import DB_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(DB_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
model = joblib.load("modelo_iris.pkl")
predictions_cache = {}

def predict_species(features):
    if features in predictions_cache:
        return predictions_cache[features]
    input_data = np.array([features])
    predicted_class = int(model.predict(input_data)[0])
    predictions_cache[features] = predicted_class
    return predicted_class

def save_prediction_to_db(data, predicted_class):
    db = SessionLocal()
    new_pred = Prediction(**data, predicted_class=predicted_class)
    db.add(new_pred)
    db.commit()
    db.close()