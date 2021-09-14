from datetime import datetime, timedelta
from app import db

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    fall_risk = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Result {}>'.format(self.id)

    def to_dict(self, string_dates=False):
        data = {
            'id' : self.id,
            'user_id' : self.user_id,
            'fall_risk' : self.fall_risk
        }

        if not string_dates:
            data['timestamp'] = self.timestamp
        else:
            data['timestamp'] = self.timestamp.isoformat()

        return data

    def from_dict(self, data):
        for field in ['user_id', 'fall_risk']:
            if field in data:
                setattr(self, field, data[field])
