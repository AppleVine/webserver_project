import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, create_access_token, jwt_required


ma = Marshmallow()
db = SQLAlchemy()
app = Flask(__name__)
jwt = JWTManager(app)




def create_app():


    app.config.from_object("config.app_config")

    db.init_app(app)
    ma.init_app(app)
    
    from commands.db import db_cmd
    app.register_blueprint(db_cmd)

    from controller import registerable_controllers
    for controller in registerable_controllers:
        app.register_blueprint(controller)

    return app

