from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.models import User
from app.api.errors import error_response


token_auth = HTTPTokenAuth()
basic_auth = HTTPBasicAuth()


@basic_auth.verify_password
def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return user


@basic_auth.error_handler
def basic_auth_error(status):
    return error_response(status)


@token_auth.verify_token
def verify_token(token):
    return User.check_token(token) if token else None


@token_auth.error_handler
def token_auth_error(status):
    return error_response(status)


@token_auth.get_user_roles
def get_user_roles(self):
    return ['admin'] if self.admin else ['user']


@basic_auth.get_user_roles
def get_user_roles(self):
    return ['admin'] if self.admin else ['user']
