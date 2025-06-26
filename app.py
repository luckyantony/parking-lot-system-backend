from flask import Flask
from dotenv import load_dotenv
load_dotenv()

from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from extensions import db, migrate
from models import User, Vehicle, ParkingLot, ParkingSpot, Ticket

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)

    from routes import api
    app.register_blueprint(api, url_prefix="/api")  # <-- Add prefix

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
