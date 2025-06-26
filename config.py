import os

class Config:
    basedir = os.path.abspath(os.path.dirname(__file__))
    DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(basedir, 'parking.db')}")
    SQLALCHEMY_DATABASE_URI = DATABASE_URL.replace("postgres://", "postgresql://") if DATABASE_URL.startswith("postgres://") else DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-key")