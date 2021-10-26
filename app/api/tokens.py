"""Token REST API endpoints.

These endpoints facilitate the creation and revoking of temporary access
tokens needed for users to access and modify their data. Admin accounts
also need a token to use their respective endpoints.
"""
from flask import jsonify
from app import db
from app.api import bp
from app.api.auth import basic_auth, token_auth


@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    """Get a tempory access token from an existing account. By default, the
    token will expire after one hour.

    ::
        
        POST /api/tokens

    Expected JSON response:

    ::
        
        {
          "token" : "alsjen282j3nbau3o83nak837ck83h7x34",
          "expiration" : "YYYY-MM-DDTHH:MM:SS.SSSS"
        }

    Note that you must include an email and password for the associated
    user account in the HTTP header.
    """
    token = basic_auth.current_user().get_token()
    expiration = basic_auth.current_user().token_expiration.isoformat()
    db.session.commit()
    return jsonify({'token': token, 'expiration' : expiration})


@bp.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    """Revoke a user token.

    ::

        DELETE /api/tokens

    Note that this endpoint is locked down via token authentication. The
    token associated with the user account must be provided as a bearer
    token in the HTTP header.
    """
    token_auth.current_user().revoke_token()
    db.session.commit()
    return '', 204
