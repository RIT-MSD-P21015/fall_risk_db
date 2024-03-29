from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
import os
import click


db = SQLAlchemy()
migrate = Migrate()
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.getenv('APP_CONFIG', 'config.Config'))

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    @app.cli.command("create-admin")
    @click.argument("firstname", default='admin')
    @click.argument("lastname", default='admin')
    @click.argument("email", default='admin@rit.edu')
    @click.argument("password", default='secret')
    def create_admin(firstname, lastname, email, password):
        admin = User()
        admin.firstname = firstname
        admin.lastname = lastname
        admin.email = email
        admin.set_password(password)
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
