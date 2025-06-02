from flask import Flask
from routes.login import login_bp
from routes.predict import predict_bp
from models.prediction import Base
from services.iris_model import engine

app = Flask(__name__)
app.register_blueprint(login_bp)
app.register_blueprint(predict_bp)

Base.metadata.create_all(engine)

if __name__ == "__main__":
    app.run()