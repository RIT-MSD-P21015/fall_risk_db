from flask import jsonify, request, url_for, abort
from datetime import datetime
import base64
from app import db
from app.models import User
from app.api import bp
from app.api.errors import *
from app.api.auth import token_auth


@bp.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()

    for field in ['email', 'password']:
        if field not in data:
            return bad_request('The field \'{}\' must be included.'.format(key))

    if User.query.filter_by(email=data['email']).first():
        return bad_request('The email address \'{}\' already exists. '
                           'Please choose another email address.'.format(data['email']))

    user = User()
    user.from_dict(data, new_user=True)

    db.session.add(user)
    db.session.commit()

    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user')
    
    return response


@bp.route('/user', methods=['GET'])
@token_auth.login_required
def get_user():
    response = jsonify(token_auth.current_user().to_dict())
    response.status_code = 200
    return response


@bp.route('/user', methods=['PUT'])
@token_auth.login_required
def modify_user():
    data = request.get_json()

    if 'email' in data and User.query.filter_by(email=data['email']).first() is not None:
        return bad_request('The email address \'{}\' already exists. '
                           'Please choose another email address.'.format(data['email']))

    token_auth.current_user().modification_timestamp = datetime.utcnow()
    token_auth.current_user().from_dict(data)

    db.session.merge(token_auth.current_user())
    db.session.commit()

    response = jsonify(token_auth.current_user().to_dict())
    response.status_code = 200

    return response
