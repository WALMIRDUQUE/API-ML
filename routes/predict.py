from flask import Blueprint, request, jsonify
from auth.jwt_handler import token_required
from services.iris_model import predict_species, save_prediction_to_db

predict_bp = Blueprint("predict", __name__)

@predict_bp.route("/predict", methods=["POST"])
@token_required
def predict():
    data = request.get_json(force=True)
    try:
        features = (
            float(data["sepal_length"]),
            float(data["sepal_width"]),
            float(data["petal_length"]),
            float(data["petal_width"])
        )
    except (KeyError, ValueError):
        return jsonify({"error": "Dados inválidos"}), 400

    predicted_class = predict_species(features)
    save_prediction_to_db({
        "sepal_length": features[0],
        "sepal_width": features[1],
        "petal_length": features[2],
        "petal_width": features[3]
    }, predicted_class)

    return jsonify({"predicted_class": predicted_class})

@predict_bp.route("/predictions", methods=["GET"])
@token_required
def list_predictions():
    from services.iris_model import SessionLocal
    from models.prediction import Prediction

    db = SessionLocal()
    limit = int(request.args.get("limit", 10))
    offset = int(request.args.get("offset", 0))

    rows = db.query(Prediction).order_by(Prediction.id.desc()).limit(limit).offset(offset).all()
    db.close()
    return jsonify([
        {
            "id": r.id,
            "sepal_length": r.sepal_length,
            "sepal_width": r.sepal_width,
            "petal_length": r.petal_length,
            "petal_width": r.petal_width,
            "predicted_class": r.predicted_class,
            "created_at": r.created_at.isoformat()
        } for r in rows
    ])