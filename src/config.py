import os
from app import app
class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        db_url = os.environ.get("DATABASE_URL")
        if not db_url:
            raise ValueError("DATABASE_URL is not set")
        return db_url
    

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['JWT_SECRET_KEY'] = os.getenv("ACCESS_TOKEN_SECRET_KEY")
app_environment = os.environ.get("FLASK)DEBUG")

class ProductionConfig(Config):
    DEBUG = True


class DevelopmentConfig(Config):
    pass 


class TestingConfig(Config):
    TESTING = True


if app_environment:
    app_config = DevelopmentConfig()
else:
    app_config = ProductionConfig()