from flask import Blueprint, request, jsonify
from auth.jwt_handler import create_token

login_bp = Blueprint("login", __name__)

TEST_USERNAME = "admin"
TEST_PASSWORD = "123456"

@login_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(force=True)
    if data.get("username") == TEST_USERNAME and data.get("password") == TEST_PASSWORD:
        token = create_token(data["username"])
        return jsonify({"token": token})
    return jsonify({"error": "Credenciais inválidas"}), 401