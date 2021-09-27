from datetime import datetime, timedelta
from app import db
import os
import base64
import json
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    email = db.Column(db.String(128), index=True, unique=True)
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
        self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()

        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token

        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')

        self.token_expiration = now + timedelta(seconds=expires_in)

        db.session.add(self)

        return self.token


    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)


    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()

        if user is None or user.token_expiration < datetime.utcnow():
            return None

        return user


    def to_dict(self):
        data = {
            'id' : self.id,
            'email' : self.email,
            'creation_timestamp' : self.creation_timestamp.isoformat(),
            'modification_timestamp' : None if self.modification_timestamp is None else self.modification_timestamp.isoformat(),
            'survey' : self.survey,
            'survey_timestamp' : None if self.survey_timestamp is None else self.survey_timestamp.isoformat(),
            'tests' : None if self.tests is None else base64.b64encode(self.tests).decode('utf-8'),
            'tests_timestamp' : None if self.tests_timestamp is None else self.tests_timestamp.isoformat(),
            'result' : self.result,
            'result_timestamp' : None if self.result_timestamp is None else self.result_timestamp.isoformat()
        }

        return data

    def from_dict(self, data, new_user=False):
        for field in ['email']:
            if field in data:
                setattr(self, field, data[field])

        if 'tests' in data:
            self.tests_timestamp = datetime.utcnow()
            self.tests = base64.b64decode(data['tests'].encode('utf-8'))

        if 'survey' in data:
            self.survey_timestamp = datetime.utcnow()
            self.survey = json.dumps(data['survey'])

        if 'result' in data:
            self.result_timestamp = datetime.utcnow()
            self.result = json.dumps(data['result'])

        if new_user and 'password' in data:
            self.set_password(data['password'])
