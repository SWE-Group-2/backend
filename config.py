import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Application configuration."""

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
