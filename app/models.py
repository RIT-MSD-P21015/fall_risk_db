from datetime import datetime, timedelta
from app import db
import os
import base64
import json
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model):
    """A table entry that contains user data.

    :cvar id: The unique integer id of a user.

    :cvar firstname: The string first name of a user.

    :cvar lastname: The string last name of a user.

    :cvar email: The unique string email address of a user.

    :cvar admin: A boolean flag indicating if a user has admin privileges or not.

    :cvar creation_timestamp: A datetime object containing the creation date of the user account.

    :cvar modification_timestamp: A datetime object containing the date that the user account was last modified. Defaults to the creation_timestamp value.

    :cvar survey: A JSON string containing a the survey data of a user.

    :cvar survey_timestamp: A datetime object containing the date of the last survey that the user took. This value can be None.

    :cvar tests: A binary blob containing the serialized Java class that should contain the tests data of a user. This value can be None.

    :cvar tests_timestamp: A datetime object containing the date of the last tests that the user took. This value can be None.

    :cvar result: A JSON string containing the fall risk result. This value can be None.

    :cvar result_timestamp: A datetime object containing the date of the last result that was posted.

    :cvar password_hash: A string containing the user hashed password.

    :cvar token: A string that contains a user temporary access token.

    :cvar token_expiration: A datetime object that contains the expiration date of a user token.
    """
    id = db.Column(db.Integer, index=True, primary_key=True)
    firstname = db.Column(db.String(128), nullable=False)
    lastname = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), index=True, unique=True, nullable=False)
    admin = db.Column(db.Boolean, default=False)
    creation_timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    modification_timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    survey = db.Column(db.String(1024), default=None)
    survey_timestamp = db.Column(db.DateTime, default=None)
    tests = db.Column(db.LargeBinary, default=None)
    tests_timestamp = db.Column(db.DateTime, default=None)
    result = db.Column(db.String(512), default=None)
    result_timestamp = db.Column(db.DateTime, default=None)
    password_hash = db.Column(db.String(128), default=None)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime, default=None)


    def __repr__(self):
        return '<User {}>'.format(self.id)


    def set_password(self, password):
        """Set a user password. But only store the hashed password in the
        member variable password_hash.

        :param password: The string representation of the user password.
        """
        self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        """Check a user password.

        :param password: The string representation of the user password.

        :return: Returns true if the password matches, otherwise, it returns false.
        """

        return check_password_hash(self.password_hash, password)
    

    def get_token(self, expires_in=3600):
        """Get a new temporary access token.

        :param expires_in: The number of minutues before the token expires.

        :return: Returns the new string token.
        """
        now = datetime.utcnow()

        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token

        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')

        self.token_expiration = now + timedelta(seconds=expires_in)

        db.session.add(self)

        return self.token


    def revoke_token(self):
        """Revoke the current access token."""
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)


    @staticmethod
    def check_token(token):
        """Check to see if a token links back to a user table entry.

        :param token: The string token to be compared against.

        :return: Returns the user object whose token matches the token given. Otherwise, this will return None.
        
        :rtype: app.models.User
        """
        user = User.query.filter_by(token=token).first()

        if user is None or user.token_expiration < datetime.utcnow():
            return None

        return user


    def to_dict(self, survey=False, tests=False):
        """Represent a user table entry as a dictionary.

        :param survey: A boolean value indicating whether or not to include the user survey results.

        :param tests: A boolean value indicating whether or not to include the user tests data.

        :return: A dictionary representation of the user table entry.
        """
        data = {
            'id' : self.id,
            'firstname' : self.firstname,
            'lastname' : self.lastname,
            'email' : self.email,
            'creation_timestamp' : self.creation_timestamp.isoformat(),
            'modification_timestamp' : None if self.modification_timestamp is None else self.modification_timestamp.isoformat(),
            'survey_timestamp' : None if self.survey_timestamp is None else self.survey_timestamp.isoformat(),
            'tests_timestamp' : None if self.tests_timestamp is None else self.tests_timestamp.isoformat(),
            'result' : self.result,
            'result_timestamp' : None if self.result_timestamp is None else self.result_timestamp.isoformat()
        }

        if survey:
            data['survey'] = self.survey

        if tests:
            data['tests'] = None if self.tests is None else base64.b64encode(self.tests).decode('utf-8')

        return data


    def from_dict(self, data, new_user=False):
        """Update a user table entry from a dictionary.

        :param data: The dictionary containing key value pairs to update user attributes.

        :param new_user: Allow for the password key to be used to change a user password.
        """
        for field in ['firstname', 'lastname', 'email']:
            if field in data:
                setattr(self, field, data[field])

        if 'tests' in data:
            self.tests_timestamp = datetime.utcnow()
            self.tests = base64.b64decode(data['tests'])

        if 'survey' in data:
            self.survey_timestamp = datetime.utcnow()
            self.survey = json.dumps(data['survey'])

        if 'result' in data:
            self.result_timestamp = datetime.utcnow()
            self.result = json.dumps(data['result'])

        if new_user and 'password' in data:
            self.set_password(data['password'])
