from flask import jsonify, request, url_for, abort
from app import db
from app.models import *
from app.api import bp
from app.api.errors import *
from app.api.auth import token_auth

@bp.route('admin/results', methods=['PUT'])
@token_auth.login_required(role='admin')
def admin_create_results():
    pass

@bp.route('admin/evaldata', methods=['GET'])
@token_auth.login_required(role='admin')
def admin_get_evaldata():
    pass
