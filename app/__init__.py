import logging
import logging.handlers
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    with app.app_context():
       db.create_all()

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app

from app.models import *
