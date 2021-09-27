from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import click


db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    @app.cli.command("create-admin")
    @click.argument("username", default='admin')
    @click.argument("password", default='secret')
    @click.argument("email", default='admin@rit.edu')
    def create_admin(username, password, email):
        admin = User()
        admin.username = username
        admin.set_password(password)
        admin.email = email
        admin.admin = True
        db.session.merge(admin)
        db.session.commit()

    @app.cli.command("create-tables")
    def create_tables():
        db.create_all()

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app


from app.models import User
