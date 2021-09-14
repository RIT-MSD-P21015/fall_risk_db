from flask import jsonify, request, url_for, abort
from app import db
from app.models import *
from app.api import bp
from app.api.errors import *
from app.api.auth import token_auth

@bp.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()

    for field in ['username', 'email', 'password']:
        if field not in data:
            return bad_request('The field \'{}\' must be included.'.format(key))
    if User.query.filter_by(username=data['username']).first():
        return bad_request('The username \'{}\' already exists. Please choose another username.'.format(data['username']))
    if User.query.filter_by(email=data['email']).first():
        return bad_request('The email address \'{}\' already exists. Please choose another email address.'.format(data['email']))

    user = User()
    user.from_dict(data, new_user=True)

    db.session.add(user)
    db.session.commit()

    response = jsonify(user.to_dict(string_dates=True))
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user')
    
    return response

@bp.route('/user', methods=['GET'])
@token_auth.login_required
def get_user():
    return jsonify(token_auth.current_user().to_dict(string_dates=True))

@bp.route('/user', methods=['PUT'])
@token_auth.login_required
def modify_user():
    data = request.get_json()

    if 'username' in data and User.query.filter_by(username=data['username']).first() is not None:
        return bad_request('The username \'{}\' already exists. Please choose another username.'.format(data['username']))
    if 'email' in data and User.query.filter_by(email=data['email']).first() is not None:
        return bad_request('The email address \'{}\' already exists. Please choose another email address.'.format(data['email']))

    token_auth.current_user().from_dict(data)

    db.session.merge(token_auth.current_user())
    db.session.commit()

    response = jsonify(token_auth.current_user().to_dict(string_dates=True))
    response.status_code = 200

    return response

@bp.route('/user/surveys', methods=['PUT'])
@token_auth.login_required
def create_user_survey():
    pass

@bp.route('/user/surveys/latest', methods=['GET'])
@token_auth.login_required
def get_latest_user_survey():
    pass

@bp.route('/user/tests', methods=['PUT'])
@token_auth.login_required
def create_user_test():
    pass

@bp.route('/user/tests/latest', methods=['GET'])
@token_auth.login_required
def get_latest_user_test():
    pass

@bp.route('/user/results/latest', methods=['GET'])
@token_auth.login_required
def get_latest_user_result():
    pass
