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
