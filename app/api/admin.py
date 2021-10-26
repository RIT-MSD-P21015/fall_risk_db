"""Admin REST API endpoints.

These REST API endpoints are only available to users who have the admin flag
set on their account. This can only be done manually by a system administrator.
"""
from flask import jsonify, request, url_for, abort
import json
from datetime import datetime
from app import db
from app.models import User
from app.api import bp
from app.api.errors import *
from app.api.auth import token_auth


@bp.route('admin/results', methods=['PUT'])
@token_auth.login_required(role='admin')
def admin_create_results():
    """Post user results to the database. Returns a 200 status code on success
    along with some statistics in JSON form.

    ::
        
        PUT /api/admin/results

    Note that this entry is locked down via token authentication and has the
    additional requirement that the user associated with the token has the
    admin flag set on their account. The token must be provided in the HTTP
    header as a bearer token.

    Expected JSON input:

    ::
        
        [
          {
            "id" : 1234,
            "result" : ...
          },
          {
            "id" : 2345,
            "result" : ...
          },
          ...
        ]

    Note that the result value can be any JSON string.

    If any of the user id are invalid, the corresponding list entry will be
    skipped and an error will not be thrown. The failed ids will be listed
    in the returned JSON.

    Expected JSON response:

    ::
        
        {
          "error" : 3,
          "results_submitted" : 10,
          "results_updated" : 7,
          "failed_ids" : [ 1234, 2345, 3456 ]
        }

    """
    data = request.get_json()

    failed_ids = []

    for i in range(len(data)):
        user = User.query.filter_by(id=data[i]['id']).first()

        if user is None:
            failed_ids.append(data[i]['id'])
            continue

        user.result_timestamp = datetime.utcnow()
        user.result = json.dumps(data[i]['result'])
        db.session.merge(user)

    db.session.commit()

    msg = {
        'error' : len(failed_ids) > 0,
        'results_submitted' : len(data),
        'results_updated' : len(data) - len(failed_ids),
        'failed_ids' : failed_ids
    }

    response = jsonify(msg)
    response.status_code = 200

    return response


@bp.route('admin/data', methods=['GET'])
@token_auth.login_required(role='admin')
def admin_get_data():
    """Get tests and survey data from all users who need to be evaluated for
    fall risk.

    ::
        
        GET /api/admin/data/?limit=25

    Note that this entry is locked down via token authentication and has the
    additional requirement that the user associated with the token has the
    admin flag set on their account. The token must be provided in the HTTP
    header as a bearer token.

    The limit parameter is used to limit the number of user data returned.
    By default limit is set to be 25.

    Expected JSON response:

    ::
        
       [
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
        },
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
        },
        ...
      ]

    Note that the survey and result values will be JSON strings and the tests
    value will be a base64 encoded string.
    """
    limit = request.args.get('limit', type=int, default=25)

    if limit < 1:
        return bad_request('The limit must be greater than 0.')

    users = User.query.\
        filter(((User.tests_timestamp != None) &
                (User.survey_timestamp != None)) &
               ((User.result_timestamp == None) |
                (User.result_timestamp <= User.tests_timestamp))).\
        order_by(User.tests_timestamp.asc()).\
        limit(limit).\
        all()

    data = [ user.to_dict(survey=True, tests=True) for user in users ]

    response = jsonify(data)
    response.status_code = 200

    return response
