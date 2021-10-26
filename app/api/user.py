"""User REST API endpoints.

These are the REST API endpoints that are available to users to create, modify,
and delete their data.
"""
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
    """Create a user account. Returns a 201 status code if successful.

    ::
        
        POST /api/user

    Expected JSON input:

    ::

        {
          "firstname" : "john",
          "lastname" : "doe",
          "email" : "jdoe@gmail.com",
          "password" : "secret"
        }

    The above JSON fields are required. If the email already exists from
    another account an error is raised.
    """
    data = request.get_json()

    for field in ['firstname', 'lastname', 'email', 'password']:
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
    """Get user data. Returns a 200 status code if successful.

    ::
        
        GET /api/user/?survey=0&tests=0

    This endpoint is locked down via token authentication and will require a
    bearer token to be included in the HTTP header. Since each token is unique
    and linked back to a single user, this endpoint will return the user data
    associated with the user attached to the provided token.

    Setting the survey and/or tests parameters to 1 will include the survey
    and/or tests data associated with the user in the response. Including the
    tests data will greatly slow down the response time.

    Expected JSON response:

    ::

        {
          "id" : 1234,
          "firstname" : "john",
          "lastname" : "doe",
          "email" : "jdoe@gmail.com",
          "creation_timestamp" : "YYYY-MM-DDTHH:MM:SS.SSSS",
          "modification_timestamp" : "YYYY-MM-DDTHH:MM:SS.SSSS",
          "survey_timestamp" : "YYYY-MM-DDTHH:MM:SS.SSSS",
          "tests_timestamp" : "YYYY-MM-DDTHH:MM:SS.SSSS",
          "result" : ...,
          "result_timestamp" : "YYYY-MM-DDTHH:MM:SS.SSSS",
          "survey" : ...,
          "tests" : ...
        }

    The survey and result value will typically be a JSON string and the tests
    value will be a base64 encoded string. Some of these dates are allowed to
    be NULL.
    """
    survey = request.args.get('survey', type=int, default=False)
    tests = request.args.get('tests', type=int, default=False)
    response = jsonify(token_auth.current_user().to_dict(survey=survey, tests=tests))
    response.status_code = 200
    return response


@bp.route('/user', methods=['PUT'])
@token_auth.login_required
def modify_user():
    """Modify user profile and optionally add survey or tests data. Will
    return a 200 status code on success.

    ::
        
        PUT /api/user

    This endpoint is locked down via token authentication and will require a
    bearer token to be included in the HTTP header. Since each token is unique
    and linked back to a single user, this endpoint will update the fields
    associated with the user attached to the provided token.

    Expected JSON input:

    ::

        {
          "firstname" : "john",
          "lastname" : "doe",
          "email" : "jdoe@gmail.com",
          "survey" : ...,
          "tests" : ...,
          "password" : "secret"
        }

    All of the above JSON fields are optional. Note that the survey value
    should be a JSON string and the tests value should be a base64 string.
    """
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


@bp.route('/user', methods=['DELETE'])
@token_auth.login_required
def delete_user():
    """Delete a user account and all user data. Returns a 204 status code on
    success.

    ::
        
        DELETE /api/user

    This endpoint is locked down via token authentication and will require a
    bearer token to be included in the HTTP header. Since each token is unique
    and linked back to a single user, this endpoint will delete all user data
    associated with the user attached to the provided token.
    """
    db.session.delete(token_auth.current_user())
    return ('', 204)
