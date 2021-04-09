from os import environ, path, urandom
from dotenv import load_dotenv
import yaml

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Set Flask configuration from .env file."""

    # General Config
    SECRET_KEY = urandom(24)
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')
    DESIGN_NAME = environ.get("DESIGN_NAME")
    PROCESSOR_NAME = environ.get("PROCESSOR_NAME")

    # Read covariate mapping
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python dictionary format
    COVARIATE_MAP = yaml.load(open(r'covariates.yml'), Loader=yaml.FullLoader)

    # Database
    SQLALCHEMY_DATABASE_URI = (
        environ.get('DATABASE_URL').replace('postgres:', 'postgresql:')
    )
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Redis
    REDIS_URL = environ.get('REDIS_URL')
